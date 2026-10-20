import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart' show debugPrint, kIsWeb;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_timezone/flutter_timezone.dart';
import 'package:shared_preferences/shared_preferences.dart';
// Mirrors the plugin's own example: the database lives in the data library
// since timezone 0.10; both libraries share the `tz` prefix.
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

import 'background_handler.dart';
import 'parsers.dart';
import 'scheduling.dart';
import 'utils/notification_details.dart';

class LocalNotificationsService extends FletService {
  LocalNotificationsService({required super.control});

  static const String _defaultWindowsGuid =
      "9F4B0E2A-1C3D-4E5F-8A9B-0C1D2E3F4A5B";

  fln.FlutterLocalNotificationsPlugin? _plugin;
  bool _initialized = false;
  bool _replaying = false;
  Future<void>? _initFuture;
  // Accumulated Darwin action categories, keyed by notification id. iOS
  // replaces the whole category set on every setNotificationCategories call,
  // so all registered categories are re-applied together — otherwise a later
  // notification's actions would clobber an earlier one's.
  final Map<int, List<fln.DarwinNotificationCategory>> _darwinCategories = {};

  @override
  void init() {
    super.init();
    control.addInvokeMethodListener(invokeMethod);
    unawaited(_ensureInitialized());
  }

  @override
  void dispose() {
    control.removeInvokeMethodListener(invokeMethod);
    super.dispose();
  }

  // ── Initialization ──────────────────────────────────────────────────

  /// Idempotent initialization. Concurrent callers await the same future, so
  /// invokes issued before initialization completes wait for it instead of
  /// silently no-oping.
  Future<void> _ensureInitialized({bool force = false}) {
    if (force || _initFuture == null) {
      _initFuture = _doInitialize();
    }
    return _initFuture!;
  }

  Future<void> _doInitialize() async {
    try {
      // The timezone database is only needed for scheduling; if it fails to
      // load, notifications still show.
      try {
        tz.initializeTimeZones();
        final info = await FlutterTimezone.getLocalTimezone();
        tz.setLocalLocation(tz.getLocation(info.identifier));
      } catch (_) {
        // Device timezone lookup failed; scheduled times fall back to UTC.
      }

      _plugin ??= fln.FlutterLocalNotificationsPlugin();
      await _plugin!.initialize(
        settings: _buildInitializationSettings(),
        onDidReceiveNotificationResponse: _handleResponse,
        onDidReceiveBackgroundNotificationResponse: notificationTapBackground,
      );
      _initialized = true;
      await _replayQueuedTaps();
      await _replayLaunchDetails();
    } catch (e) {
      // Initialization failed (e.g. invalid platform settings). Allow a
      // retry on the next invoke and surface the failure to the caller.
      debugPrint("flet_notifications: initialization failed: $e");
      _initialized = false;
      _initFuture = null;
    }
  }

  fln.InitializationSettings _buildInitializationSettings() {
    final defaultIcon =
        control.getString("default_icon", "@mipmap/ic_launcher")!;
    final darwin = fln.DarwinInitializationSettings(
      requestAlertPermission:
          control.getBool("request_alert_permission", true)!,
      requestSoundPermission:
          control.getBool("request_sound_permission", true)!,
      requestBadgePermission:
          control.getBool("request_badge_permission", true)!,
      requestCriticalPermission:
          control.getBool("request_critical_permission", false)!,
      notificationCategories:
          _darwinCategories.values.expand((categories) => categories).toList(),
    );
    return fln.InitializationSettings(
      android: fln.AndroidInitializationSettings(defaultIcon),
      iOS: darwin,
      macOS: darwin,
      linux: const fln.LinuxInitializationSettings(
        defaultActionName: "Open",
      ),
      windows: fln.WindowsInitializationSettings(
        appName: control.getString("app_name", "Flet App")!,
        appUserModelId:
            control.getString("app_user_model_id", "Flet.App.Notifications")!,
        guid: control.getString("windows_guid", _defaultWindowsGuid)!,
      ),
      web: const fln.WebInitializationSettings(),
    );
  }

  // ── Tap replay (background taps + cold starts) ──────────────────────

  Future<void> _replayQueuedTaps() async {
    if (_replaying) return;
    _replaying = true;
    try {
      final prefs = await SharedPreferences.getInstance();
      for (final event in await drainTapQueue(prefs)) {
        _emit(event);
      }
    } catch (e) {
      // Best-effort: preferences unavailable must not break the service.
      debugPrint("flet_notifications: tap queue replay failed: $e");
    } finally {
      _replaying = false;
    }
  }

  Future<void> _replayLaunchDetails() async {
    try {
      final details = await _plugin?.getNotificationAppLaunchDetails();
      if (details?.didNotificationLaunchApp != true ||
          details?.notificationResponse == null) {
        return;
      }
      final event = responseToEvent(details!.notificationResponse!);
      final prefs = await SharedPreferences.getInstance();
      if (await shouldEmitLaunch(prefs, event)) {
        _emit(event);
      }
    } catch (e) {
      // Best-effort: preferences unavailable must not break the service.
      debugPrint("flet_notifications: launch details replay failed: $e");
    }
  }

  void _handleResponse(fln.NotificationResponse response) {
    _emit(responseToEvent(response));
  }

  void _emit(Map<String, Object?> event) {
    final type = event["response_type"];
    final name = switch (type) {
      "action" => "action",
      "dismissed" => "dismiss",
      _ => "tap",
    };
    control.triggerEvent(name, event);
  }

  // ── Method routing ──────────────────────────────────────────────────

  /// Routes an invoke call from the Python control. Public so the invoke
  /// seam can be exercised in tests (Flet delivers invokes here via the
  /// listener registered in [init]).
  Future<dynamic> invokeMethod(String name, [dynamic args]) async {
    if (name != "initialize") {
      await _ensureInitialized();
      if (!_initialized) {
        return "error:init_failed:notification backend unavailable";
      }
    }
    try {
      return await _dispatch(name, args);
    } on UnimplementedError {
      // The plugin/platform cannot do this (e.g. scheduling on Linux/web).
      return "error:unsupported_platform:$name is not available on this "
          "platform";
    } on UnsupportedError {
      return "error:unsupported_platform:$name is not available on this "
          "platform";
    }
  }

  Future<dynamic> _dispatch(String name, dynamic args) async {
    switch (name) {
      case "initialize":
        await _ensureInitialized(force: true);
        return _initialized ? "ok" : "error:init_failed:initialize failed";

      case "show":
        return await _show(args);

      case "cancel":
        final map = args as Map;
        final tag = map["tag"] as String?;
        await _plugin?.cancel(
          id: parseInt(map["id"])!,
          tag: tag?.isEmpty == true ? null : tag,
        );
        return "ok";

      case "cancel_all":
        await _plugin?.cancelAll();
        return "ok";

      case "schedule":
        return await _schedule(args);

      case "periodically_show":
        return await _periodicallyShow(args);

      case "cancel_pending":
        await _plugin?.cancelAllPendingNotifications();
        return "ok";

      case "get_pending":
        return await _getPending();

      case "create_notification_channel":
        return await _createChannel(args);

      case "delete_notification_channel":
        return await _deleteChannel(args);

      case "get_notification_channels":
        return await _getChannels();

      case "start_foreground_service":
        return await _startForegroundService(args);

      case "stop_foreground_service":
        return await _stopForegroundService();

      case "request_permissions":
        return (await _requestPermissions()) ? "true" : "false";

      case "can_schedule_exact_notifications":
        final android = _androidPlugin;
        if (android == null) return "true";
        return (await android.canScheduleExactNotifications() ?? false)
            ? "true"
            : "false";

      case "request_exact_alarm_permission":
        final android = _androidPlugin;
        if (android == null) return "false";
        return (await android.requestExactAlarmsPermission() ?? false)
            ? "true"
            : "false";

      case "are_notifications_enabled":
        return (await _areNotificationsEnabled()) ? "true" : "false";

      case "open_app_settings":
        return (await _plugin?.openAppNotificationSettings() ?? false)
            ? "true"
            : "false";

      case "get_active":
        return await _getActive();

      case "get_launch_details":
        return await _getLaunchDetails();

      case "request_full_screen_intent":
        final android = _androidPlugin;
        return (await android?.requestFullScreenIntentPermission() ?? false)
            ? "true"
            : "false";

      case "has_notification_policy_access":
        return (await _hasNotificationPolicyAccess()) ? "true" : "false";

      case "request_notification_policy_access":
        final android = _androidPlugin;
        return (await android?.requestNotificationPolicyAccess() ?? false)
            ? "true"
            : "false";

      case "create_notification_channel_group":
        return await _createChannelGroup(args);

      case "delete_notification_channel_group":
        return await _deleteChannelGroup(args);

      default:
        return "error:unknown_method:$name";
    }
  }

  Future<String> _show(dynamic args) async {
    try {
      final map = args as Map;
      final id = parseInt(map["id"])!;
      final title = map["title"] as String?;
      final body = map["body"] as String?;
      final payload = map["payload"] as String? ?? "";
      final actions = parseActions(map["actions"]);
      final styleError = _invalidStyleCode(map["style"]);
      if (styleError != null) return styleError;
      await _plugin!.show(
        id: id,
        title: title,
        body: body,
        payload: payload,
        notificationDetails: await _buildNotificationDetails(
          id: id,
          actions: actions,
          style: parseStyle(map["style"]),
          details: map,
        ),
      );
      return "ok";
    } on InvalidNotificationOptionException catch (e) {
      return "error:invalid_option:${e.message}";
    } on FormatException catch (e) {
      return "error:invalid_action:${e.message}";
    } catch (e) {
      return "error:show_failed:$e";
    }
  }

  Future<String> _schedule(dynamic args) async {
    final map = args as Map;
    final List<ParsedAction> actions;
    try {
      actions = parseActions(map["actions"]);
    } on FormatException catch (e) {
      return "error:invalid_action:${e.message}";
    }
    final styleError = _invalidStyleCode(map["style"]);
    if (styleError != null) return styleError;
    final tz.TZDateTime scheduledDate;
    try {
      scheduledDate = parseWhen(map, tz.local);
    } on FormatException catch (e) {
      return "error:invalid_schedule:${e.message}";
    }
    try {
      await _plugin!.zonedSchedule(
        id: parseInt(map["id"])!,
        title: map["title"] as String?,
        body: map["body"] as String?,
        scheduledDate: scheduledDate,
        notificationDetails: await _buildNotificationDetails(
          id: parseInt(map["id"])!,
          actions: actions,
          style: parseStyle(map["style"]),
          details: map,
        ),
        androidScheduleMode: parseAndroidScheduleMode(
            map["schedule_mode"] as String?,
            fln.AndroidScheduleMode.exactAllowWhileIdle)!,
        payload: map["payload"] as String? ?? "",
        matchDateTimeComponents: parseDateTimeComponents(
          map["match_components"] as String?,
        ),
      );
      return "ok";
    } catch (e) {
      return "error:schedule_failed:$e";
    }
  }

  Future<String> _periodicallyShow(dynamic args) async {
    try {
      final map = args as Map;
      final id = parseInt(map["id"])!;
      final actions = parseActions(map["actions"]);
      final styleError = _invalidStyleCode(map["style"]);
      if (styleError != null) return styleError;
      final notificationDetails = await _buildNotificationDetails(
        id: id,
        actions: actions,
        style: parseStyle(map["style"]),
        details: map,
      );
      final scheduleMode = parseAndroidScheduleMode(
          map["schedule_mode"] as String?,
          fln.AndroidScheduleMode.exactAllowWhileIdle)!;
      final title = map["title"] as String?;
      final body = map["body"] as String?;
      final payload = map["payload"] as String? ?? "";
      final interval = map["repeat_interval"];
      if (interval is! String) {
        final duration = parseDuration(interval);
        if (duration == null || duration < const Duration(minutes: 1)) {
          return "error:invalid_option:repeat_interval must be at least one minute";
        }
        await _plugin!.periodicallyShowWithDuration(
          id: id,
          title: title,
          body: body,
          payload: payload,
          notificationDetails: notificationDetails,
          repeatDurationInterval: duration,
          androidScheduleMode: scheduleMode,
        );
        return "ok";
      }
      final repeatInterval = parseRepeatInterval(interval);
      if (repeatInterval == null) {
        return "error:invalid_option:Unknown repeat_interval: $interval";
      }
      await _plugin!.periodicallyShow(
        id: id,
        title: title,
        body: body,
        payload: payload,
        notificationDetails: notificationDetails,
        repeatInterval: repeatInterval,
        androidScheduleMode: scheduleMode,
      );
      return "ok";
    } on FormatException catch (e) {
      return "error:invalid_action:${e.message}";
    } catch (e) {
      return "error:schedule_failed:$e";
    }
  }

  Future<Object> _getPending() async {
    try {
      final pending = await _plugin!.pendingNotificationRequests();
      return pending
          .map((p) => {
                "id": p.id,
                "title": p.title ?? "",
                "body": p.body ?? "",
                "payload": p.payload ?? "",
              })
          .toList();
    } catch (e) {
      return "error:query_failed:$e";
    }
  }

  fln.AndroidFlutterLocalNotificationsPlugin? get _androidPlugin =>
      _plugin?.resolvePlatformSpecificImplementation<
          fln.AndroidFlutterLocalNotificationsPlugin>();

  fln.WebFlutterLocalNotificationsPlugin? get _webPlugin =>
      _plugin?.resolvePlatformSpecificImplementation<
          fln.WebFlutterLocalNotificationsPlugin>();

  // ── Notification details construction ───────────────────────────────

  Future<fln.NotificationDetails> _buildNotificationDetails({
    required int id,
    required List<ParsedAction> actions,
    ParsedStyle? style,
    Map? details,
  }) =>
      parseNotificationDetails(
        id: id,
        actions: actions,
        style: style,
        details: details,
        registerDarwinCategories: _registerDarwinCategories,
      );

  /// Parses the optional style of a show/schedule payload, mapping format
  /// failures to the `invalid_style` error code.
  String? _invalidStyleCode(Object? raw) {
    try {
      parseStyle(raw);
    } on FormatException catch (e) {
      return "error:invalid_style:${e.message}";
    }
    return null;
  }

  /// Registers the action buttons as a Darwin notification category.
  ///
  /// iOS/macOS require categories to be registered through
  /// `InitializationSettings.notificationCategories` before a notification
  /// can reference them, and `setNotificationCategories` replaces the whole
  /// set — so each notification with actions gets its own category,
  /// registered by re-initializing the plugin. iOS `initialize` is
  /// re-entrant (it re-applies permissions and categories), which makes this
  /// safe. Without this, action buttons silently never appear on iOS.
  Future<void> _registerDarwinCategories(
    int id,
    List<ParsedAction> actions,
  ) async {
    final categoryActions = actions.map((a) {
      final options = <fln.DarwinNotificationActionOption>{
        if (a.destructive) fln.DarwinNotificationActionOption.destructive,
        if (a.foreground) fln.DarwinNotificationActionOption.foreground,
      };
      final input = a.input;
      if (input == null) {
        return fln.DarwinNotificationAction.plain(
          a.id,
          a.title,
          options: options,
        );
      }
      return fln.DarwinNotificationAction.text(
        a.id,
        a.title,
        buttonTitle: input.label.isEmpty ? a.title : input.label,
        placeholder: input.label.isEmpty ? null : input.label,
        options: options,
      );
    }).toList();

    // setNotificationCategories REPLACES the set, so every category created
    // so far is re-applied together; otherwise notification B's actions would
    // clobber notification A's.
    _darwinCategories[id] = [
      fln.DarwinNotificationCategory(
        "$darwinNotificationCategoryPrefix$id",
        actions: categoryActions,
      ),
    ];
    await _plugin?.initialize(
      settings: _buildInitializationSettings(),
      onDidReceiveNotificationResponse: _handleResponse,
      onDidReceiveBackgroundNotificationResponse: notificationTapBackground,
    );
  }

  // ── Permissions ─────────────────────────────────────────────────────

  Future<bool> _requestPermissions() async {
    if (kIsWeb) {
      final web = _webPlugin;
      if (web == null || !fln.WebFlutterLocalNotificationsPlugin.isSupported) {
        return false;
      }
      if (web.permissionStatus == fln.WebNotificationPermission.granted) {
        return true;
      }
      return await web.requestNotificationsPermission() ?? false;
    }

    final android = _androidPlugin;
    if (android != null) {
      return await android.requestNotificationsPermission() ?? false;
    }

    final ios = _plugin?.resolvePlatformSpecificImplementation<
        fln.IOSFlutterLocalNotificationsPlugin>();
    if (ios != null) {
      return await ios.requestPermissions(
            sound: control.getBool("request_sound_permission", true)!,
            alert: control.getBool("request_alert_permission", true)!,
            badge: control.getBool("request_badge_permission", true)!,
            critical: control.getBool("request_critical_permission", false)!,
          ) ??
          false;
    }

    final macos = _plugin?.resolvePlatformSpecificImplementation<
        fln.MacOSFlutterLocalNotificationsPlugin>();
    if (macos != null) {
      return await macos.requestPermissions(
            sound: control.getBool("request_sound_permission", true)!,
            alert: control.getBool("request_alert_permission", true)!,
            badge: control.getBool("request_badge_permission", true)!,
            critical: control.getBool("request_critical_permission", false)!,
          ) ??
          false;
    }

    // Windows and Linux have no runtime notification permission request.
    return true;
  }

  // ── Channels (Android 8.0+) ──────────────────────────────────────────

  Future<String> _createChannel(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) {
      return "error:unsupported_platform:channels are Android-only";
    }
    try {
      final map = args as Map;
      final id = map["id"] as String;
      final name = map["name"] as String;
      if (id.isEmpty || name.isEmpty) {
        return "error:invalid_channel:id and name are required";
      }
      final ledColor = map["led_color"] as String?;
      await android.createNotificationChannel(
        fln.AndroidNotificationChannel(
          id,
          name,
          description: map["description"] as String?,
          groupId: map["group_id"] as String?,
          importance: parseNotificationImportance(
              map["importance"] as String?, fln.Importance.defaultImportance)!,
          bypassDnd: parseBool(map["bypass_dnd"], false)!,
          playSound: parseBool(map["play_sound"], true)!,
          sound: map["sound"] == null
              ? null
              : fln.RawResourceAndroidNotificationSound(
                  map["sound"] as String,
                ),
          enableVibration: parseBool(map["enable_vibration"], true)!,
          vibrationPattern:
              parseNotificationVibrationPattern(map["vibration_pattern"]),
          showBadge: parseBool(map["show_badge"], true)!,
          enableLights: parseBool(map["enable_lights"], false)!,
          ledColor: parseColor(ledColor?.trim(), null),
        ),
      );
      return "ok";
    } catch (e) {
      return "error:channel_failed:$e";
    }
  }

  Future<String> _deleteChannel(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) {
      return "error:unsupported_platform:channels are Android-only";
    }
    final map = args as Map;
    final channelId = map["channel_id"] as String;
    await android.deleteNotificationChannel(channelId: channelId);
    return "ok";
  }

  Future<String> _getChannels() async {
    final android = _androidPlugin;
    if (android == null) return "[]";
    try {
      final channels = await android.getNotificationChannels() ?? const [];
      return jsonEncode(
        channels
            .map(
              (c) => {
                "id": c.id,
                "name": c.name,
                "description": c.description ?? "",
                "groupId": c.groupId,
                "importance": c.importance.name,
                "bypass_dnd": c.bypassDnd,
                "play_sound": c.playSound,
                "sound": c.sound?.sound,
                "enable_vibration": c.enableVibration,
                "vibration_pattern": c.vibrationPattern?.toList(),
                "show_badge": c.showBadge,
                "enable_lights": c.enableLights,
                "led_color": c.ledColor == null
                    ? null
                    : "#${c.ledColor!.toARGB32().toRadixString(16).padLeft(8, "0")}",
              },
            )
            .toList(),
      );
    } catch (e) {
      return "error:channel_failed:$e";
    }
  }

  // ── Foreground service (Android) ─────────────────────────────────────

  Future<String> _startForegroundService(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) {
      return "error:unsupported_platform:foreground service is Android-only";
    }
    try {
      final map = args as Map;
      final id = parseInt(map["id"])!;
      if (id == 0) {
        return "error:invalid_service_id:foreground service id must be non-zero";
      }
      final actions = parseActions(map["actions"]);
      final styleError = _invalidStyleCode(map["style"]);
      if (styleError != null) return styleError;
      await android.startForegroundService(
        id: id,
        title: map["title"] as String?,
        body: map["body"] as String?,
        payload: map["payload"] as String? ?? "",
        startType: parseServiceStartType(map["start_type"] as String?,
            fln.AndroidServiceStartType.startSticky)!,
        foregroundServiceTypes: parseForegroundServiceTypes(
          map["foreground_service_types"] as List?,
        ),
        notificationDetails: (await _buildNotificationDetails(
          id: id,
          actions: actions,
          style: parseStyle(map["style"]),
          details: map,
        ))
            .android,
      );
      return "ok";
    } catch (e) {
      return "error:foreground_service_failed:$e";
    }
  }

  Future<String> _stopForegroundService() async {
    final android = _androidPlugin;
    if (android == null) {
      return "error:unsupported_platform:foreground service is Android-only";
    }
    await android.stopForegroundService();
    return "ok";
  }

  fln.AndroidServiceStartType? parseServiceStartType(String? value,
          [fln.AndroidServiceStartType? defaultValue]) =>
      parseEnum(fln.AndroidServiceStartType.values, value, defaultValue);

  Set<fln.AndroidServiceForegroundType>? parseForegroundServiceTypes(
    List? values,
  ) {
    if (values == null || values.isEmpty) return null;
    const lookup = {
      "camera": fln.AndroidServiceForegroundType.foregroundServiceTypeCamera,
      "connectedDevice":
          fln.AndroidServiceForegroundType.foregroundServiceTypeConnectedDevice,
      "dataSync":
          fln.AndroidServiceForegroundType.foregroundServiceTypeDataSync,
      "health": fln.AndroidServiceForegroundType.foregroundServiceTypeHealth,
      "location":
          fln.AndroidServiceForegroundType.foregroundServiceTypeLocation,
      "mediaPlayback":
          fln.AndroidServiceForegroundType.foregroundServiceTypeMediaPlayback,
      "mediaProjection":
          fln.AndroidServiceForegroundType.foregroundServiceTypeMediaProjection,
      "microphone":
          fln.AndroidServiceForegroundType.foregroundServiceTypeMicrophone,
      "phoneCall":
          fln.AndroidServiceForegroundType.foregroundServiceTypePhoneCall,
      "remoteMessaging":
          fln.AndroidServiceForegroundType.foregroundServiceTypeRemoteMessaging,
      "shortService":
          fln.AndroidServiceForegroundType.foregroundServiceTypeShortService,
      "specialUse":
          fln.AndroidServiceForegroundType.foregroundServiceTypeSpecialUse,
      "systemExempted":
          fln.AndroidServiceForegroundType.foregroundServiceTypeSystemExempted,
    };
    return values
        .map((v) => lookup["$v"])
        .whereType<fln.AndroidServiceForegroundType>()
        .toSet();
  }

  // ── Probes & OS integration ───────────────────────────────

  Future<bool> _areNotificationsEnabled() async {
    if (kIsWeb) {
      return fln.WebFlutterLocalNotificationsPlugin.isSupported &&
          _webPlugin?.permissionStatus == fln.WebNotificationPermission.granted;
    }

    final android = _androidPlugin;
    if (android != null) {
      return await android.areNotificationsEnabled() ?? false;
    }
    final ios = _plugin?.resolvePlatformSpecificImplementation<
        fln.IOSFlutterLocalNotificationsPlugin>();
    if (ios != null) {
      final options = await ios.checkPermissions();
      // Provisional (quiet) grants still deliver to the notification center.
      return (options?.isEnabled ?? false) ||
          (options?.isProvisionalEnabled ?? false);
    }
    final macos = _plugin?.resolvePlatformSpecificImplementation<
        fln.MacOSFlutterLocalNotificationsPlugin>();
    if (macos != null) {
      final options = await macos.checkPermissions();
      return (options?.isEnabled ?? false) ||
          (options?.isProvisionalEnabled ?? false);
    }
    // Windows and Linux have no queryable gate through this bridge.
    return true;
  }

  Future<bool> _hasNotificationPolicyAccess() async {
    final android = _androidPlugin;
    return await android?.hasNotificationPolicyAccess() ?? false;
  }

  Future<Object> _getActive() async {
    try {
      final active = await _plugin?.getActiveNotifications() ?? const [];
      return active
          .map((a) => {
                "id": a.id ?? 0,
                "channel_id": a.channelId ?? "",
                "group_key": a.groupKey ?? "",
                "tag": a.tag ?? "",
                "title": a.title ?? "",
                "body": a.body ?? "",
                "payload": a.payload ?? "",
                "big_text": a.bigText ?? "",
              })
          .toList();
    } catch (e) {
      return "error:query_failed:$e";
    }
  }

  Future<String> _getLaunchDetails() async {
    try {
      final details = await _plugin?.getNotificationAppLaunchDetails();
      if (details == null || details.didNotificationLaunchApp != true) {
        return jsonEncode({"did_notification_launch_app": false});
      }
      final response = details.notificationResponse;
      return jsonEncode({
        "did_notification_launch_app": true,
        "notification": response == null ? null : responseToEvent(response),
      });
    } catch (e) {
      return "error:query_failed:$e";
    }
  }

  Future<String> _createChannelGroup(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) {
      return "error:unsupported_platform:channel groups are Android-only";
    }
    try {
      final map = args as Map;
      await android.createNotificationChannelGroup(
        fln.AndroidNotificationChannelGroup(
          map["group_id"] as String,
          map["name"] as String,
          description: map["description"] as String?,
        ),
      );
      return "ok";
    } catch (e) {
      return "error:channel_failed:$e";
    }
  }

  Future<String> _deleteChannelGroup(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) {
      return "error:unsupported_platform:channel groups are Android-only";
    }
    final map = args as Map;
    await android.deleteNotificationChannelGroup(
      groupId: map["group_id"] as String,
    );
    return "ok";
  }
}
