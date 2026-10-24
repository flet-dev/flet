import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart' show debugPrint, visibleForTesting;
import 'package:flutter/services.dart' show PlatformException;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_timezone/flutter_timezone.dart';
import 'package:shared_preferences/shared_preferences.dart';
// Mirrors the plugin's own example: the database lives in the data library
// since timezone 0.10; both libraries share the `tz` prefix.
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

import 'background_handler.dart';
import 'utils/actions.dart';
import 'utils/details.dart';
import 'utils/errors.dart';
import 'utils/parsers.dart';
import 'utils/scheduling.dart';
import 'utils/tap_queue_signal.dart';

class NotificationsService extends FletService {
  NotificationsService({required super.control});

  static const String _defaultWindowsGuid =
      "9F4B0E2A-1C3D-4E5F-8A9B-0C1D2E3F4A5B";

  fln.FlutterLocalNotificationsPlugin? _plugin;
  bool _initialized = false;

  /// The [_initializationProperties] of the last successful initialization.
  Object? _appliedInitializationProperties;
  String? _initializationError;
  bool _replaying = false;

  /// Whether the queue gained entries during the running replay.
  bool _replayAgain = false;

  /// Stops replaying the queue when background isolates add to it.
  void Function()? _stopListeningForQueuedTaps;
  bool _launchReplayComplete = false;

  /// Live responses received before the launch replay finishes.
  ///
  /// Android can deliver the response that launched the app both live and through
  /// launch details, so a launch response already seen live is not replayed.
  final Set<String> _liveResponsesBeforeLaunchReplay = {};
  Future<void>? _initFuture;

  /// [SharedPreferencesAsync] key of the persisted Apple action categories,
  /// out of reach of `ft.SharedPreferences`.
  static const String _darwinCategoriesKey =
      "flet_notifications_darwin_categories";

  /// Apple action categories by identifier, as [darwinActionSpecs].
  ///
  /// Apple replaces every registered category on each registration, so all of
  /// them, including those of notifications scheduled in earlier app runs, are
  /// persisted and registered together.
  final Map<String, List<List<Object?>>> _darwinCategories = {};
  bool _darwinCategoriesLoaded = false;

  /// Identifiers of the categories registered by the last successful
  /// initialization.
  Set<String> _registeredDarwinCategories = {};

  @override
  void init() {
    super.init();
    control.addInvokeMethodListener(invokeMethod);
    unawaited(_ensureInitialized());
  }

  @override
  void update() {
    if (_initializationProperties != _appliedInitializationProperties) {
      unawaited(_applyChangedInitializationProperties());
    }
  }

  @override
  void dispose() {
    _stopListeningForQueuedTaps?.call();
    control.removeInvokeMethodListener(invokeMethod);
    super.dispose();
  }

  /// Service properties the native backend is initialized with.
  ///
  /// Other property changes, such as setting an event handler, need no
  /// reinitialization.
  (String?, String?, String?, String?) get _initializationProperties => (
        control.getString("android_default_icon"),
        control.getString("windows_app_name"),
        control.getString("windows_app_user_model_id"),
        control.getString("windows_guid"),
      );

  /// Reinitializes the backend with changed initialization properties.
  ///
  /// A running initialization finishes first; a backend that never initialized
  /// picks up the new properties on its next retry instead.
  Future<void> _applyChangedInitializationProperties() async {
    await _initFuture;
    if (_appliedInitializationProperties == null ||
        _initializationProperties == _appliedInitializationProperties) {
      return;
    }
    await _ensureInitialized(force: true);
  }

  /// Initializes the backend again, failing as the next method call would.
  @visibleForTesting
  Future<void> reinitialize() async {
    await _ensureInitialized(force: true);
    _throwIfNotInitialized();
  }

  /// Idempotent initialization. Concurrent callers await the same future, so
  /// invokes issued before initialization completes wait for it instead of
  /// silently no-oping.
  Future<void> _ensureInitialized({bool force = false}) {
    if (_initFuture != null) return _initFuture!;
    if (_initialized && !force) return Future.value();
    return _initFuture = _doInitialize().whenComplete(() => _initFuture = null);
  }

  Future<void> _initializeBackend() async {
    final properties = _initializationProperties;
    try {
      final categories = Map.of(_darwinCategories);
      final result = await _plugin!.initialize(
        settings: _buildInitializationSettings(
          notificationCategories: [
            for (final specs in categories.values) darwinCategory(specs),
          ],
        ),
        onDidReceiveNotificationResponse: _handleResponse,
        onDidReceiveBackgroundNotificationResponse: notificationTapBackground,
      );
      // Apple returns the permission-request result, even when no prompt is
      // requested. A false result still means the backend was configured.
      if (result != true && !(isApplePlatform() && result == false)) {
        throw StateError(
            "notification backend initialization returned $result");
      }
      if (isApplePlatform()) {
        _registeredDarwinCategories = categories.keys.toSet();
      }
      _appliedInitializationProperties = properties;
    } catch (_) {
      _initialized = false;
      rethrow;
    }
  }

  Future<void> _doInitialize() async {
    _initialized = false;
    _initializationError = null;
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
      if (isApplePlatform()) await _loadDarwinCategories();
      await _initializeBackend();
      _initialized = true;
      // Listen before draining, so entries queued meanwhile are not missed.
      _stopListeningForQueuedTaps ??=
          listenForQueuedTaps(() => unawaited(_replayQueuedTaps()));
      await _replayQueuedTaps();
      await _replayLaunchDetails();
    } catch (e) {
      // Initialization failed (e.g. invalid platform settings). Allow a
      // retry on the next invoke and surface the failure to the caller.
      debugPrint("flet_notifications: initialization failed: $e");
      _initialized = false;
      _initializationError = e.toString();
    }
  }

  fln.InitializationSettings _buildInitializationSettings({
    required List<fln.DarwinNotificationCategory> notificationCategories,
  }) {
    final darwin = fln.DarwinInitializationSettings(
      requestAlertPermission: false,
      requestSoundPermission: false,
      requestBadgePermission: false,
      notificationCategories: notificationCategories,
    );
    return fln.InitializationSettings(
      android: fln.AndroidInitializationSettings(control.getString(
          "android_default_icon", "flet_notifications_icon")!),
      iOS: darwin,
      macOS: darwin,
      linux: const fln.LinuxInitializationSettings(
        defaultActionName: "Open",
      ),
      windows: fln.WindowsInitializationSettings(
        appName: control.getString("windows_app_name", "Flet App")!,
        appUserModelId: control.getString(
            "windows_app_user_model_id", "Flet.App.Notifications")!,
        guid: control.getString("windows_guid", _defaultWindowsGuid)!,
      ),
      web: const fln.WebInitializationSettings(),
    );
  }

  // ── Tap replay (background taps + cold starts) ──────────────────────

  Future<void> _replayQueuedTaps() async {
    if (_replaying) {
      _replayAgain = true;
      return;
    }
    _replaying = true;
    try {
      do {
        _replayAgain = false;
        for (final event in await drainTapQueue(SharedPreferencesAsync())) {
          _emit(event);
        }
      } while (_replayAgain);
    } catch (e) {
      // Best-effort: preferences unavailable must not break the service.
      debugPrint("flet_notifications: tap queue replay failed: $e");
    } finally {
      _replaying = false;
    }
  }

  Future<void> _replayLaunchDetails() async {
    if (_launchReplayComplete) return;
    try {
      final details = await _plugin?.getNotificationAppLaunchDetails();
      // Concurrent initialization may already have handled the startup response.
      if (_launchReplayComplete) return;
      final response = details?.notificationResponse;
      if (details?.didNotificationLaunchApp == true &&
          response != null &&
          !_liveResponsesBeforeLaunchReplay.contains(_responseKey(response))) {
        _emit(responseToEvent(response));
      }
      _liveResponsesBeforeLaunchReplay.clear();
      // Later activity intents can describe taps already delivered by callbacks.
      _launchReplayComplete = true;
    } catch (e) {
      debugPrint("flet_notifications: launch details replay failed: $e");
    }
  }

  void _handleResponse(fln.NotificationResponse response) {
    if (!_launchReplayComplete) {
      _liveResponsesBeforeLaunchReplay.add(_responseKey(response));
    }
    _emit(responseToEvent(response));
  }

  /// Identifies a response by the fields delivered to Python.
  static String _responseKey(fln.NotificationResponse response) =>
      jsonEncode(responseToEvent(response));

  void _emit(Map<String, Object?> event) {
    final data = Map<String, Object?>.of(event);
    final name = data.remove("event") as String? ?? "tap";
    control.triggerEvent(name, data);
  }

  Future<dynamic> invokeMethod(String name, [dynamic args]) async {
    await _ensureInitialized();
    _throwIfNotInitialized();
    try {
      return await _dispatch(name, args);
    } on NotificationException {
      rethrow;
    } on UnimplementedError {
      throw NotificationException.unsupportedPlatform(
        "$name is not available on this platform",
      );
    } on UnsupportedError {
      throw NotificationException.unsupportedPlatform(
        "$name is not available on this platform",
      );
    } on PlatformException catch (e) {
      final message = "${e.code}: ${e.message ?? ""}";
      throw e.code == "exact_alarms_not_permitted"
          ? NotificationException.permissionDenied(message)
          : NotificationException.operationFailed(message);
    } catch (e) {
      throw NotificationException.operationFailed(e.toString());
    }
  }

  void _throwIfNotInitialized() {
    if (!_initialized) {
      throw NotificationException.initializationFailed(
        _initializationError ?? "notification backend unavailable",
      );
    }
  }

  Future<dynamic> _dispatch(String name, dynamic args) async {
    switch (name) {
      case "show":
        return await _show(args);

      case "cancel":
        final map = args as Map;
        final tag = map["tag"] as String?;
        await _plugin?.cancel(
          id: parseInt(map["id"])!,
          tag: tag?.isEmpty == true ? null : tag,
        );
        return null;

      case "cancel_all":
        await _plugin?.cancelAll();
        return null;

      case "schedule":
        return await _schedule(args);

      case "periodically_show":
        return await _periodicallyShow(args);

      case "cancel_pending":
        await _plugin?.cancelAllPendingNotifications();
        return null;

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
        return await _requestPermissions(args);

      case "can_schedule_exact_notifications":
        final android = _androidPlugin;
        if (android == null) return true;
        return await android.canScheduleExactNotifications() ?? false;

      case "request_exact_alarm_permission":
        final android = _androidPlugin;
        if (android == null) return true;
        return await android.requestExactAlarmsPermission() ?? false;

      case "are_notifications_enabled":
        return await _areNotificationsEnabled();

      case "open_app_settings":
        return await _plugin?.openAppNotificationSettings() ?? false;

      case "get_active":
        return await _getActive();

      case "request_full_screen_intent":
        return await _androidPlugin?.requestFullScreenIntentPermission() ??
            false;

      case "has_notification_policy_access":
        return await _hasNotificationPolicyAccess();

      case "request_notification_policy_access":
        return await _androidPlugin?.requestNotificationPolicyAccess() ?? false;

      case "create_notification_channel_group":
        return await _createChannelGroup(args);

      case "delete_notification_channel_group":
        return await _deleteChannelGroup(args);

      default:
        throw NotificationException.operationFailed("unknown method $name");
    }
  }

  Future<void> _show(dynamic args) async {
    final map = args as Map;
    final id = parseInt(map["id"])!;
    final title = map["title"] as String?;
    final body = map["body"] as String?;
    final payload = map["payload"] as String?;
    final actions = parseActions(map["actions"]);
    await _plugin!.show(
      id: id,
      title: title,
      body: body,
      payload: payload,
      notificationDetails: await _buildNotificationDetails(
        actions: actions,
        details: map,
      ),
    );
  }

  Future<void> _schedule(dynamic args) async {
    final map = args as Map;
    final id = parseInt(map["id"])!;
    final title = map["title"] as String?;
    final body = map["body"] as String?;
    final payload = map["payload"] as String?;
    final actions = parseActions(map["actions"]);
    final scheduledDate = parseWhen(map, tz.local);
    final scheduleMode = parseAndroidScheduleMode(
        map["schedule_mode"] as String?,
        fln.AndroidScheduleMode.inexactAllowWhileIdle)!;
    final matchComponents =
        parseDateTimeComponents(map["match_components"] as String?);
    await _plugin!.zonedSchedule(
      id: id,
      title: title,
      body: body,
      scheduledDate: scheduledDate,
      androidScheduleMode: scheduleMode,
      payload: payload,
      matchDateTimeComponents: matchComponents,
      notificationDetails: await _buildNotificationDetails(
        actions: actions,
        details: map,
      ),
    );
  }

  Future<void> _periodicallyShow(dynamic args) async {
    final map = args as Map;
    final id = parseInt(map["id"])!;
    final title = map["title"] as String?;
    final body = map["body"] as String?;
    final payload = map["payload"] as String?;
    final actions = parseActions(map["actions"]);
    final scheduleMode = parseAndroidScheduleMode(
        map["schedule_mode"] as String?,
        fln.AndroidScheduleMode.inexactAllowWhileIdle)!;
    final interval = map["repeat_interval"];
    final repeatInterval =
        interval is String ? parseRepeatInterval(interval) : null;
    final duration = interval is! String ? parseDuration(interval) : null;
    if (interval is String && repeatInterval == null) {
      throw NotificationException.invalidArgument(
          "Unknown repeat_interval: $interval");
    }
    if (interval is! String &&
        (duration == null || duration < const Duration(minutes: 1))) {
      throw const NotificationException.invalidArgument(
          "repeat_interval must be at least one minute");
    }
    final notificationDetails = await _buildNotificationDetails(
      actions: actions,
      details: map,
    );
    if (duration != null) {
      await _plugin!.periodicallyShowWithDuration(
        id: id,
        title: title,
        body: body,
        payload: payload,
        notificationDetails: notificationDetails,
        repeatDurationInterval: duration,
        androidScheduleMode: scheduleMode,
      );
    } else {
      await _plugin!.periodicallyShow(
        id: id,
        title: title,
        body: body,
        payload: payload,
        notificationDetails: notificationDetails,
        repeatInterval: repeatInterval!,
        androidScheduleMode: scheduleMode,
      );
    }
  }

  Future<List<Map<String, Object?>>> _getPending() async {
    final pending = await _plugin!.pendingNotificationRequests();
    return pending
        .map(
          (p) => {
            "id": p.id,
            "title": p.title,
            "body": p.body,
            "payload": p.payload,
          },
        )
        .toList();
  }

  fln.AndroidFlutterLocalNotificationsPlugin? get _androidPlugin =>
      _plugin?.resolvePlatformSpecificImplementation<
          fln.AndroidFlutterLocalNotificationsPlugin>();

  fln.WebFlutterLocalNotificationsPlugin? get _webPlugin =>
      _plugin?.resolvePlatformSpecificImplementation<
          fln.WebFlutterLocalNotificationsPlugin>();

  // ── Notification details construction ───────────────────────────────

  Future<fln.NotificationDetails> _buildNotificationDetails({
    required List<ParsedAction> actions,
    Map? details,
  }) async {
    final notificationDetails = parseNotificationDetails(
      actions: actions,
      details: details,
    );
    await _ensureAndroidChannel(details);
    if (actions.isNotEmpty) {
      await _registerDarwinCategory(actions);
    }
    return notificationDetails;
  }

  /// Creates or updates a channel declared inline on a notification.
  ///
  /// Posting alone creates a missing channel without its group; registering it
  /// first applies every declared setting, including the group.
  Future<void> _ensureAndroidChannel(Map? details) async {
    final options = details?["options"];
    final android = options is Map ? options["android"] : null;
    final channel = android is Map ? android["channel"] : null;
    final plugin = _androidPlugin;
    if (channel is! Map || plugin == null) return;
    await plugin.createNotificationChannel(parseNotificationChannel(channel));
  }

  /// Registers the Apple category of [actions] if it is new.
  ///
  /// Category updates use initialization without requesting authorization.
  Future<void> _registerDarwinCategory(List<ParsedAction> actions) async {
    if (!isApplePlatform()) return;
    final specs = darwinActionSpecs(actions);
    final identifier = darwinCategoryIdentifier(specs);
    if (_registeredDarwinCategories.contains(identifier)) return;
    _darwinCategories[identifier] = specs;
    await _saveDarwinCategories();
    await _initializeBackend();
  }

  /// Restores the categories registered in earlier app runs, once per service.
  Future<void> _loadDarwinCategories() async {
    if (_darwinCategoriesLoaded) return;
    _darwinCategoriesLoaded = true;
    try {
      final stored =
          await SharedPreferencesAsync().getString(_darwinCategoriesKey);
      if (stored == null) return;
      for (final MapEntry(:key, :value)
          in (jsonDecode(stored) as Map).entries) {
        _darwinCategories.putIfAbsent(
          key as String,
          () => [
            for (final spec in value as List) List<Object?>.of(spec as List)
          ],
        );
      }
    } catch (e) {
      // Best-effort: categories registered in this run still work.
      debugPrint("flet_notifications: loading action categories failed: $e");
    }
  }

  Future<void> _saveDarwinCategories() async {
    try {
      await SharedPreferencesAsync()
          .setString(_darwinCategoriesKey, jsonEncode(_darwinCategories));
    } catch (e) {
      debugPrint("flet_notifications: saving action categories failed: $e");
    }
  }

  // ── Permissions ─────────────────────────────────────────────────────

  Future<bool> _requestPermissions(dynamic args) async {
    if (isWebPlatform()) {
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

    final map = args is Map ? args : const {};
    final alert = parseBool(map["alert"], true)!;
    final sound = parseBool(map["sound"], true)!;
    final badge = parseBool(map["badge"], true)!;
    final critical = parseBool(map["critical"], false)!;
    final provisional = parseBool(map["provisional"], false)!;
    final ios = _plugin?.resolvePlatformSpecificImplementation<
        fln.IOSFlutterLocalNotificationsPlugin>();
    if (ios != null) {
      return await ios.requestPermissions(
            alert: alert,
            sound: sound,
            badge: badge,
            critical: critical,
            provisional: provisional,
          ) ??
          false;
    }

    final macos = _plugin?.resolvePlatformSpecificImplementation<
        fln.MacOSFlutterLocalNotificationsPlugin>();
    if (macos != null) {
      return await macos.requestPermissions(
            alert: alert,
            sound: sound,
            badge: badge,
            critical: critical,
            provisional: provisional,
          ) ??
          false;
    }

    // Windows and Linux have no runtime notification permission request.
    return true;
  }

  // ── Channels (Android 8.0+) ──────────────────────────────────────────

  Future<void> _createChannel(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) return;
    if (args is! Map) {
      throw const NotificationException.invalidArgument(
          "channel must be a NotificationChannel");
    }
    await android.createNotificationChannel(parseNotificationChannel(args));
  }

  Future<void> _deleteChannel(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) return;
    final map = args as Map;
    final channelId = map["channel_id"] as String;
    await android.deleteNotificationChannel(channelId: channelId);
  }

  Future<List<Map<String, Object?>>> _getChannels() async {
    final android = _androidPlugin;
    if (android == null) return <Map<String, Object?>>[];
    final channels = await android.getNotificationChannels() ?? const [];
    return channels
        .map(
          (c) => {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "group_id": c.groupId,
            "importance": c.importance.name,
            "bypass_dnd": c.bypassDnd,
            "play_sound": c.playSound,
            "sound": c.sound?.sound,
            "enable_vibration": c.enableVibration,
            "vibration_pattern": c.vibrationPattern?.toList(),
            "show_badge": c.showBadge,
            "enable_lights": c.enableLights,
            "audio_attributes_usage": c.audioAttributesUsage.name,
            "led_color": c.ledColor == null
                ? null
                : "#${c.ledColor!.toARGB32().toRadixString(16).padLeft(8, "0")}",
          },
        )
        .toList();
  }

  // ── Foreground service (Android) ─────────────────────────────────────

  Future<void> _startForegroundService(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) {
      throw UnsupportedError("foreground service is Android-only");
    }
    final map = args as Map;
    final id = parseInt(map["id"])!;
    if (id == 0) {
      throw const NotificationException.invalidArgument(
        "foreground service id must be non-zero",
      );
    }
    final actions = parseActions(map["actions"]);
    await android.startForegroundService(
      id: id,
      title: map["title"] as String?,
      body: map["body"] as String?,
      payload: map["payload"] as String?,
      startType: parseServiceStartType(
        map["start_type"] as String?,
        fln.AndroidServiceStartType.startSticky,
      )!,
      foregroundServiceTypes: parseForegroundServiceTypes(
        map["foreground_service_types"],
      ),
      notificationDetails: (await _buildNotificationDetails(
        actions: actions,
        details: map,
      ))
          .android,
    );
  }

  Future<void> _stopForegroundService() async {
    final android = _androidPlugin;
    if (android == null) return;
    await android.stopForegroundService();
  }

  // ── Probes & OS integration ───────────────────────────────

  Future<bool> _areNotificationsEnabled() async {
    if (isWebPlatform()) {
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

  Future<List<Map<String, Object?>>> _getActive() async {
    final active = await _plugin?.getActiveNotifications() ?? const [];
    return active
        .map(
          (a) => {
            "id": a.id,
            "channel_id": a.channelId,
            "group_key": a.groupKey,
            "tag": a.tag,
            "title": a.title,
            "body": a.body,
            "payload": a.payload,
            "big_text": a.bigText,
          },
        )
        .toList();
  }

  Future<void> _createChannelGroup(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) return;
    final map = args as Map;
    await android.createNotificationChannelGroup(
      fln.AndroidNotificationChannelGroup(
        map["group_id"] as String,
        map["name"] as String,
        description: map["description"] as String?,
      ),
    );
  }

  Future<void> _deleteChannelGroup(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) return;
    final map = args as Map;
    await android.deleteNotificationChannelGroup(
      groupId: map["group_id"] as String,
    );
  }
}
