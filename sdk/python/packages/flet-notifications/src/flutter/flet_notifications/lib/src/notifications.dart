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

import 'platforms/android.dart';
import 'platforms/darwin.dart';
import 'platforms/windows.dart';
import 'platforms/windows_identity.dart';
import 'responses/response_queue_signal.dart';
import 'responses/responses.dart';
import 'utils/actions.dart';
import 'utils/details.dart';
import 'utils/errors.dart';
import 'utils/scheduling.dart';

/// The `Notifications` service: runs Python's method calls on the
/// notifications plugin and sends notification responses back as events.
///
/// The backend initializes when the service starts, and method calls wait for
/// it. Responses that arrive while no service runs, such as taps in a
/// background isolate or the tap that launched the app, are replayed once a
/// service initializes.
class NotificationsService extends FletService {
  NotificationsService({required super.control});

  fln.FlutterLocalNotificationsPlugin? _plugin;

  /// This app's default Windows identity, read once on Windows.
  WindowsIdentity? _windowsIdentity;
  bool _initialized = false;

  /// The [_initializationProperties] of the last successful initialization.
  Object? _appliedInitializationProperties;
  String? _initializationError;
  bool _replaying = false;

  /// Whether the queue gained entries during the running replay.
  bool _replayAgain = false;

  /// Stops replaying the queue when background isolates add to it.
  void Function()? _stopListeningForQueuedResponses;
  bool _disposed = false;
  Future<void>? _initFuture;

  /// The live service, which receives the plugin's notification responses.
  ///
  /// The Windows and Linux plugins keep the response callback of their first
  /// initialization until the app exits, so every service hands the plugin
  /// [_forwardResponse], which reaches whichever service is live.
  static NotificationsService? _live;

  /// Whether the response that launched the app was handled.
  ///
  /// Launch details describe how the process started, so only the first
  /// service replays them.
  static bool _launchReplayComplete = false;

  /// Live responses received before the launch replay finishes.
  ///
  /// Android can deliver the response that launched the app both live and through
  /// launch details, so a launch response already seen live is not replayed.
  static final Set<String> _liveResponsesBeforeLaunchReplay = {};

  /// Resets the state services share across the process.
  @visibleForTesting
  static void resetForTesting() {
    _live = null;
    _launchReplayComplete = false;
    _liveResponsesBeforeLaunchReplay.clear();
  }

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
    _live = this;
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
    _disposed = true;
    if (identical(_live, this)) _live = null;
    _stopListeningForQueuedResponses?.call();
    _stopListeningForQueuedResponses = null;
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

  /// Initializes the backend again as the live service, failing as the next
  /// method call would.
  @visibleForTesting
  Future<void> reinitialize() async {
    _live = this;
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
            for (final MapEntry(:key, :value) in categories.entries)
              darwinCategory(key, value),
          ],
        ),
        onDidReceiveNotificationResponse: _forwardResponse,
        onDidReceiveBackgroundNotificationResponse:
            notificationResponseBackground,
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

  /// Loads what the backend needs, initializes it, then replays the queued
  /// and launch responses.
  ///
  /// The steps run in order: the timezone for scheduling, the Windows identity,
  /// the stored Apple categories, then the backend. The queue is listened to
  /// before it's drained, so entries added meanwhile aren't missed. A failure
  /// is kept for the next method call to report, and that call retries.
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
      if (_disposed) return;

      _plugin ??= fln.FlutterLocalNotificationsPlugin();
      if (isWindowsDesktop()) {
        _windowsIdentity ??= await defaultWindowsIdentity();
      }
      if (isApplePlatform()) await _loadDarwinCategories();
      if (_disposed) return;
      await _initializeBackend();
      _initialized = true;
      // A service disposed meanwhile leaves the queue to its successor.
      if (_disposed) return;
      // Listen before draining, so entries queued meanwhile are not missed.
      _stopListeningForQueuedResponses ??=
          listenForQueuedResponses(() => unawaited(_replayQueuedResponses()));
      await _replayQueuedResponses();
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
    final customAppUserModelId = control.getString("windows_app_user_model_id");
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
        appName: control.getString("windows_app_name") ??
            _windowsIdentity?.appName ??
            "Flet App",
        appUserModelId: customAppUserModelId ??
            _windowsIdentity?.appUserModelId ??
            "Flet.App",
        iconPath: _windowsIdentity?.iconPath,
        guid: control.getString("windows_guid") ??
            (customAppUserModelId != null
                ? windowsGuid(customAppUserModelId)
                : _windowsIdentity?.guid) ??
            windowsGuid("Flet.App"),
      ),
      web: const fln.WebInitializationSettings(),
    );
  }

  /// Emits the responses queued while no service ran, oldest first.
  ///
  /// Signals that arrive during a replay make it drain the queue again rather
  /// than run concurrently.
  Future<void> _replayQueuedResponses() async {
    if (_disposed) return;
    if (_replaying) {
      _replayAgain = true;
      return;
    }
    _replaying = true;
    try {
      do {
        _replayAgain = false;
        if (_disposed) break;
        for (final event
            in await drainResponseQueue(SharedPreferencesAsync())) {
          _triggerResponseEvent(event);
        }
      } while (_replayAgain);
    } catch (e) {
      // Best-effort: preferences unavailable must not break the service.
      debugPrint("flet_notifications: response queue replay failed: $e");
    } finally {
      _replaying = false;
    }
  }

  /// Emits the response that launched the app, once per process.
  ///
  /// Android can also deliver that response live; one already seen live isn't
  /// emitted again.
  Future<void> _replayLaunchDetails() async {
    if (_launchReplayComplete || _disposed) return;
    try {
      final details = await _plugin?.getNotificationAppLaunchDetails();
      // Concurrent initialization may already have handled the startup
      // response, and a disposed service leaves it to its successor.
      if (_launchReplayComplete || _disposed) return;
      final response = details?.notificationResponse;
      if (details?.didNotificationLaunchApp == true &&
          response != null &&
          !_liveResponsesBeforeLaunchReplay.contains(_responseKey(response))) {
        _triggerResponseEvent(responseToEvent(response));
      }
      _liveResponsesBeforeLaunchReplay.clear();
      // Later activity intents can describe taps already delivered by callbacks.
      _launchReplayComplete = true;
    } on UnimplementedError {
      // Linux reports no launch details.
      _liveResponsesBeforeLaunchReplay.clear();
      _launchReplayComplete = true;
    } catch (e) {
      debugPrint("flet_notifications: launch details replay failed: $e");
    }
  }

  /// Hands [response] to the live service, or queues it for the next one.
  static void _forwardResponse(fln.NotificationResponse response) {
    final live = _live;
    if (live != null) {
      live._handleResponse(response);
    } else {
      unawaited(queueResponse(response));
    }
  }

  /// Emits a live response, noting it until the launch replay finishes so
  /// the launch response isn't emitted twice.
  void _handleResponse(fln.NotificationResponse response) {
    if (!_launchReplayComplete) {
      _liveResponsesBeforeLaunchReplay.add(_responseKey(response));
    }
    _triggerResponseEvent(responseToEvent(response));
  }

  /// Identifies a response by the fields delivered to Python.
  static String _responseKey(fln.NotificationResponse response) =>
      jsonEncode(responseToEvent(response));

  /// Sends [event] to Python as the event it names, without the `event` key.
  void _triggerResponseEvent(Map<String, Object?> event) {
    final data = Map<String, Object?>.of(event);
    final name = data.remove("event") as String? ?? "tap";
    control.triggerEvent(name, data);
  }

  fln.AndroidFlutterLocalNotificationsPlugin? get _androidPlugin =>
      _plugin?.resolvePlatformSpecificImplementation<
          fln.AndroidFlutterLocalNotificationsPlugin>();

  fln.FlutterLocalNotificationsWindows? get _windowsPlugin =>
      _plugin?.resolvePlatformSpecificImplementation<
          fln.FlutterLocalNotificationsWindows>();

  fln.WebFlutterLocalNotificationsPlugin? get _webPlugin =>
      _plugin?.resolvePlatformSpecificImplementation<
          fln.WebFlutterLocalNotificationsPlugin>();

  /// Runs the Python method [name] with [args] once the backend is ready.
  ///
  /// Every failure is thrown as a [NotificationException], whose code selects
  /// the exception class Python raises.
  Future<dynamic> invokeMethod(String name, [dynamic args]) async {
    await _ensureInitialized();
    // The backend can't initialize in a browser without notifications, or
    // whose service worker can't register, as in Firefox's private windows.
    // The permission probes still answer, so apps can fall back.
    if (isWebPlatform() && !_initialized) {
      if (name == "request_permissions" ||
          name == "are_notifications_enabled") {
        return false;
      }
      throw const NotificationException.unsupportedPlatform(
        "this browser can't show notifications",
      );
    }
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
    } on ArgumentError catch (e) {
      // The plugin's own checks, such as a schedule date in the past.
      throw NotificationException.invalidArgument(e.toString());
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
        return await _cancel(args);

      case "cancel_all":
        await _plugin?.cancelAll();
        return null;

      case "schedule":
        return await _schedule(args);

      case "periodically_show":
        return await _periodicallyShow(args);

      case "cancel_all_pending":
        await _plugin?.cancelAllPendingNotifications();
        return null;

      case "get_pending":
        return await _getPending();

      case "create_channel":
        return await _createChannel(args);

      case "delete_channel":
        return await _deleteChannel(args);

      case "get_channels":
        return await _getChannels();

      case "start_foreground_service":
        return await _startForegroundService(args);

      case "update_windows_progress":
        return await _updateWindowsProgress(args);

      case "stop_foreground_service":
        return await _stopForegroundService();

      case "request_permissions":
        return await _requestPermissions(args);

      case "can_schedule_exact_alarms":
        return _androidPlugin == null ||
            (await _androidPlugin!.canScheduleExactNotifications() ?? false);

      case "request_exact_alarm_permission":
        return _androidPlugin == null ||
            (await _androidPlugin!.requestExactAlarmsPermission() ?? false);

      case "are_notifications_enabled":
        return await _areNotificationsEnabled();

      case "open_settings":
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

      case "create_channel_group":
        return await _createChannelGroup(args);

      case "delete_channel_group":
        return await _deleteChannelGroup(args);

      default:
        throw NotificationException.operationFailed("unknown method $name");
    }
  }

  Future<void> _cancel(dynamic args) async {
    final map = args as Map;
    final tag = map["tag"] as String?;
    await _plugin?.cancel(
      id: parseInt(map["id"])!,
      tag: tag?.isEmpty == true ? null : tag,
    );
  }

  Future<void> _show(dynamic args) async {
    final map = args as Map;
    final id = parseInt(map["id"])!;
    final title = map["title"] as String?;
    final body = map["body"] as String?;
    final payload = _launchPayload(id, map["payload"] as String?);
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
    final payload = _launchPayload(id, map["payload"] as String?);
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
    final payload = _launchPayload(id, map["payload"] as String?);
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

  /// The payload to give the plugin: on Windows, the notification's launch
  /// arguments, so a click on its body can be told apart from its buttons.
  String? _launchPayload(int id, String? payload) => isWindowsDesktop()
      ? windowsLaunchArguments(notificationId: id, payload: payload)
      : payload;

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
        final specs = [
          for (final spec in value as List)
            completeDarwinActionSpec(List<Object?>.of(spec as List))
        ];
        if (specs.contains(null)) continue;
        _darwinCategories.putIfAbsent(
            key as String, () => specs.cast<List<Object?>>());
      }
    } catch (e) {
      // Best-effort: categories registered in this run still work.
      debugPrint("flet_notifications: loading action categories failed: $e");
    }
  }

  /// Stores the Apple categories for [_loadDarwinCategories] to restore in
  /// later app runs.
  Future<void> _saveDarwinCategories() async {
    try {
      await SharedPreferencesAsync()
          .setString(_darwinCategoriesKey, jsonEncode(_darwinCategories));
    } catch (e) {
      debugPrint("flet_notifications: saving action categories failed: $e");
    }
  }

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
            "importance": notificationImportanceName(c.importance),
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

  /// Updates the progress bar of a shown Windows notification in place.
  ///
  /// Returns `false` when the notification is no longer shown.
  Future<bool> _updateWindowsProgress(dynamic args) async {
    final windows = _windowsPlugin;
    if (windows == null) {
      throw const NotificationException.unsupportedPlatform(
          "update_windows_progress() is only supported on Windows");
    }
    final map = args as Map;
    // Windows only updates the bar's value and label; its status and title stay
    // as shown.
    final result = await windows.updateProgressBar(
      notificationId: parseInt(map["id"])!,
      progressBar: parseWindowsProgress(map["progress"] as Map),
    );
    return switch (result) {
      fln.NotificationUpdateResult.success => true,
      fln.NotificationUpdateResult.notFound => false,
      fln.NotificationUpdateResult.error =>
        throw const NotificationException.operationFailed(
            "Windows could not update the notification"),
    };
  }

  Future<void> _startForegroundService(dynamic args) async {
    final android = _androidPlugin;
    if (android == null) {
      throw const NotificationException.unsupportedPlatform(
          "start_foreground_service() is only supported on Android");
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
        map["service_types"],
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
