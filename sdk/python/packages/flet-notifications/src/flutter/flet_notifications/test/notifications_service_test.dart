import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui' show Color;

import 'package:flet/flet.dart';
import 'package:flet_notifications/src/responses/responses.dart';
import 'package:flet_notifications/src/notifications_service.dart';
import 'package:flet_notifications/src/utils/actions.dart';
import 'package:flet_notifications/src/utils/errors.dart';
import 'package:flet_notifications/src/utils/parsers.dart';
import 'package:flet_notifications/src/utils/details.dart'
    as notification_details;
import 'package:flutter/foundation.dart'
    show debugDefaultTargetPlatformOverride, TargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter/services.dart' show PlatformException;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shared_preferences_platform_interface/in_memory_shared_preferences_async.dart';
import 'package:shared_preferences_platform_interface/shared_preferences_async_platform_interface.dart';
import 'package:timezone/timezone.dart' as tz;

/// Records converted native details without performing operating-system actions.
class _RecordingAndroid extends fln.AndroidFlutterLocalNotificationsPlugin {
  final List<Map<String, Object?>> shown = [];
  final List<fln.AndroidNotificationChannel> channelsCreated = [];
  final List<Map<String, Object?>> periodicCalls = [];
  final List<Map<String, Object?>> scheduledCalls = [];
  List<fln.PendingNotificationRequest> pending = [];
  List<fln.ActiveNotification> active = [];
  List<fln.AndroidNotificationChannel>? queriedChannels = [];
  fln.NotificationAppLaunchDetails? launchDetails;
  bool failQueries = false;
  Object? operationError;

  void _checkOperation() {
    final error = operationError;
    if (error != null) throw error;
  }

  bool? _probeResult() {
    _checkOperation();
    return permissionResult;
  }

  fln.DidReceiveNotificationResponseCallback? onResponse;
  void Function()? onLaunchDetailsQuery;
  int permissionRequests = 0;
  bool? permissionResult = true;
  int foregroundStarts = 0;
  int initializations = 0;
  bool initializationResult = true;
  bool failInitialization = false;
  Completer<void>? initializationStarted;
  Future<void>? initializationGate;
  fln.AndroidInitializationSettings? lastInitializationSettings;
  fln.AndroidServiceStartType? lastStartType;
  Set<fln.AndroidServiceForegroundType>? lastForegroundServiceTypes;

  @override
  Future<bool> initialize({
    required fln.AndroidInitializationSettings settings,
    fln.DidReceiveNotificationResponseCallback?
        onDidReceiveNotificationResponse,
    fln.DidReceiveBackgroundNotificationResponseCallback?
        onDidReceiveBackgroundNotificationResponse,
  }) async {
    initializations++;
    lastInitializationSettings = settings;
    initializationStarted?.complete();
    if (initializationGate != null) await initializationGate;
    if (failInitialization) throw StateError("initialization failed");
    onResponse = onDidReceiveNotificationResponse;
    return initializationResult;
  }

  @override
  Future<void> show({
    required int id,
    String? title,
    String? body,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
  }) async {
    _checkOperation();
    shown.add({'id': id, 'details': notificationDetails});
  }

  @override
  Future<bool?> requestNotificationsPermission() async {
    _checkOperation();
    permissionRequests++;
    return permissionResult;
  }

  @override
  Future<List<fln.PendingNotificationRequest>>
      pendingNotificationRequests() async {
    _checkOperation();
    if (failQueries) throw StateError("Query unavailable");
    return pending;
  }

  @override
  Future<List<fln.ActiveNotification>> getActiveNotifications() async {
    _checkOperation();
    if (failQueries) throw StateError("Query unavailable");
    return active;
  }

  @override
  Future<List<fln.AndroidNotificationChannel>?>
      getNotificationChannels() async {
    _checkOperation();
    if (failQueries) throw StateError("Query unavailable");
    return queriedChannels;
  }

  @override
  Future<fln.NotificationAppLaunchDetails?>
      getNotificationAppLaunchDetails() async {
    _checkOperation();
    if (failQueries) throw StateError("Query unavailable");
    onLaunchDetailsQuery?.call();
    return launchDetails;
  }

  @override
  Future<void> createNotificationChannel(
      fln.AndroidNotificationChannel channel) async {
    _checkOperation();
    channelsCreated.add(channel);
  }

  @override
  Future<void> periodicallyShow({
    required int id,
    required fln.RepeatInterval repeatInterval,
    String? title,
    String? body,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
    fln.AndroidScheduleMode scheduleMode = fln.AndroidScheduleMode.exact,
  }) async {
    _checkOperation();
    periodicCalls.add({
      'interval': repeatInterval,
      'title': title,
      'body': body,
      'payload': payload,
      'scheduleMode': scheduleMode,
    });
  }

  @override
  Future<void> periodicallyShowWithDuration({
    required int id,
    required Duration repeatDurationInterval,
    String? title,
    String? body,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
    fln.AndroidScheduleMode scheduleMode = fln.AndroidScheduleMode.exact,
  }) async {
    _checkOperation();
    periodicCalls.add({
      'interval': repeatDurationInterval,
      'title': title,
      'body': body,
      'payload': payload,
      'scheduleMode': scheduleMode,
    });
  }

  @override
  Future<bool?> canScheduleExactNotifications() async => _probeResult();

  @override
  Future<bool?> requestExactAlarmsPermission() async => _probeResult();

  @override
  Future<bool?> areNotificationsEnabled() async => _probeResult();

  @override
  Future<bool?> requestFullScreenIntentPermission() async => _probeResult();

  @override
  Future<bool?> hasNotificationPolicyAccess() async => _probeResult();

  @override
  Future<bool?> requestNotificationPolicyAccess() async => _probeResult();

  @override
  Future<bool?> openAppNotificationSettings() async => _probeResult();

  @override
  Future<void> zonedSchedule({
    required int id,
    String? title,
    String? body,
    required tz.TZDateTime scheduledDate,
    String? payload,
    fln.DateTimeComponents? matchDateTimeComponents,
    fln.AndroidNotificationDetails? notificationDetails,
    fln.AndroidScheduleMode scheduleMode = fln.AndroidScheduleMode.exact,
  }) async {
    _checkOperation();
    scheduledCalls.add({
      "id": id,
      "title": title,
      "body": body,
      "payload": payload,
      "scheduledDate": scheduledDate,
      "scheduleMode": scheduleMode,
      "matchComponents": matchDateTimeComponents,
    });
  }

  @override
  Future<void> cancel({required int id, String? tag}) async =>
      _checkOperation();

  @override
  Future<void> cancelAll() async => _checkOperation();

  @override
  Future<void> cancelAllPendingNotifications() async => _checkOperation();

  @override
  Future<void> stopForegroundService() async => _checkOperation();

  @override
  Future<void> deleteNotificationChannel({required String channelId}) async =>
      _checkOperation();

  @override
  Future<void> createNotificationChannelGroup(
          fln.AndroidNotificationChannelGroup group) async =>
      _checkOperation();

  @override
  Future<void> deleteNotificationChannelGroup(
          {required String groupId}) async =>
      _checkOperation();

  @override
  Future<void> startForegroundService({
    required int id,
    String? title,
    String? body,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
    fln.AndroidServiceStartType startType =
        fln.AndroidServiceStartType.startSticky,
    Set<fln.AndroidServiceForegroundType>? foregroundServiceTypes,
  }) async {
    _checkOperation();
    foregroundStarts++;
    lastStartType = startType;
    lastForegroundServiceTypes = foregroundServiceTypes;
  }
}

/// Fake Windows platform implementation recording in-place updates.
///
/// The real class loads the Windows plugin's DLL when constructed, so the fake
/// only implements its interface; members the tests don't use are left to
/// [noSuchMethod].
class _FakeWindowsPlugin extends fln.FlutterLocalNotificationsPlatform
    implements fln.FlutterLocalNotificationsWindows {
  final List<(int, fln.WindowsProgressBar)> updates = [];
  fln.NotificationUpdateResult updateResult =
      fln.NotificationUpdateResult.success;

  @override
  Future<bool> initialize({
    required fln.WindowsInitializationSettings settings,
    fln.DidReceiveNotificationResponseCallback?
        onDidReceiveNotificationResponse,
  }) async =>
      true;

  @override
  Future<fln.NotificationUpdateResult> updateProgressBar({
    required int notificationId,
    required fln.WindowsProgressBar progressBar,
  }) async {
    updates.add((notificationId, progressBar));
    return updateResult;
  }

  @override
  Future<void> show({
    required int id,
    String? title,
    String? body,
    String? payload,
    fln.WindowsNotificationDetails? notificationDetails,
  }) =>
      throw UnimplementedError();

  @override
  Future<void> zonedSchedule({
    required int id,
    String? title,
    String? body,
    required tz.TZDateTime scheduledDate,
    fln.WindowsNotificationDetails? notificationDetails,
    String? payload,
    fln.DateTimeComponents? matchDateTimeComponents,
  }) =>
      throw UnimplementedError();

  @override
  Future<void> periodicallyShow({
    required int id,
    String? title,
    String? body,
    required fln.RepeatInterval repeatInterval,
    fln.WindowsNotificationDetails? notificationDetails,
    String? payload,
  }) =>
      throw UnimplementedError();

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

/// Fake macOS platform implementation recording Darwin notification details.
class _FakeMacOsPlugin extends fln.MacOSFlutterLocalNotificationsPlugin {
  fln.DarwinNotificationDetails? shownDarwin;
  final List<fln.DarwinInitializationSettings> initializations = [];
  bool? initializationResult = true;
  bool failInitialization = false;
  final List<Map<String, bool>> permissionRequests = [];

  @override
  Future<bool?> initialize({
    required fln.DarwinInitializationSettings settings,
    fln.DidReceiveNotificationResponseCallback?
        onDidReceiveNotificationResponse,
  }) async {
    initializations.add(settings);
    if (failInitialization) throw StateError("initialization failed");
    return initializationResult;
  }

  @override
  Future<bool?> requestPermissions({
    bool sound = false,
    bool alert = false,
    bool badge = false,
    bool provisional = false,
    bool critical = false,
    bool providesAppNotificationSettings = false,
  }) async {
    permissionRequests.add({
      "sound": sound,
      "alert": alert,
      "badge": badge,
      "critical": critical,
      "provisional": provisional,
    });
    return true;
  }

  @override
  Future<void> show({
    required int id,
    String? title,
    String? body,
    fln.DarwinNotificationDetails? notificationDetails,
    String? payload,
  }) async {
    shownDarwin = notificationDetails;
  }
}

class _RecordingControl extends Control {
  final List<Map<String, Object?>> events = [];

  _RecordingControl()
      : super(
          id: 1,
          type: "Notifications",
          properties: const {},
          backend: FletBackend(
            pageUri: Uri.parse("http://localhost"),
            assetsDir: "",
            extensions: [],
            multiView: false,
          ),
        );

  @override
  void triggerEvent(String name, [dynamic data]) {
    events.add({"name": name, "data": data});
  }
}

/// Invokes [method] and returns its result, or for a failure the text Flet
/// reports to Python: the [NotificationException]'s `"<code>: <message>"`.
Future<Object?> _call(NotificationsService service, String method,
    [Object? args]) async {
  try {
    return await service.invokeMethod(method, args);
  } on NotificationException catch (e) {
    return e.toString();
  }
}

/// Reinitializes [service] and returns `null`, or for a failure the text Flet
/// reports to Python, as [_call] does.
Future<Object?> _reinitialize(NotificationsService service) async {
  try {
    await service.reinitialize();
    return null;
  } on NotificationException catch (e) {
    return e.toString();
  }
}

NotificationsService _makeService(
    {Map<String, dynamic>? properties, Control? control}) {
  if (control != null) return NotificationsService(control: control);
  final backend = FletBackend(
    pageUri: Uri.parse("uri"),
    assetsDir: "",
    extensions: [],
    multiView: false,
  );
  final defaultControl = Control(
    id: 1,
    type: "Notifications",
    properties: properties ?? const {},
    backend: backend,
  );
  return NotificationsService(control: defaultControl);
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late _RecordingAndroid plugin;
  setUp(() {
    NotificationsService.resetForTesting();
    // Persisted Apple categories must not leak between tests.
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
    plugin = _RecordingAndroid();
    fln.FlutterLocalNotificationsPlatform.instance = plugin;
  });

  test("changing an initialization property reinitializes with the new value",
      () async {
    final service =
        _makeService(properties: {"android_default_icon": "ic_old"});
    expect(await _call(service, "cancel_all"), null);
    expect(plugin.initializations, 1);
    expect(plugin.lastInitializationSettings!.defaultIcon, "ic_old");

    // Other properties, such as event handlers, need no reinitialization.
    service.control.properties["on_tap"] = true;
    service.update();
    await pumpEventQueue();
    expect(plugin.initializations, 1);

    service.control.properties["android_default_icon"] = "ic_new";
    service.update();
    await pumpEventQueue();
    expect(plugin.initializations, 2);
    expect(plugin.lastInitializationSettings!.defaultIcon, "ic_new");
  });

  test("a property change during initialization is applied once it finishes",
      () async {
    final gate = Completer<void>();
    plugin.initializationStarted = Completer<void>();
    plugin.initializationGate = gate.future;
    final service =
        _makeService(properties: {"android_default_icon": "ic_old"});
    final pending = _call(service, "cancel_all");
    await plugin.initializationStarted!.future;

    service.control.properties["android_default_icon"] = "ic_new";
    service.update();
    plugin.initializationGate = null;
    gate.complete();
    expect(await pending, null);
    await pumpEventQueue();
    expect(plugin.initializations, 2);
    expect(plugin.lastInitializationSettings!.defaultIcon, "ic_new");
  });

  test("a failed backend picks up changed properties on its next retry",
      () async {
    plugin.failInitialization = true;
    final service =
        _makeService(properties: {"android_default_icon": "ic_old"});
    expect(await _call(service, "cancel_all"),
        startsWith("initialization_failed: "));
    expect(plugin.initializations, 1);

    service.control.properties["android_default_icon"] = "ic_new";
    service.update();
    await pumpEventQueue();
    // No extra attempt: the next method call retries.
    expect(plugin.initializations, 1);

    plugin.failInitialization = false;
    expect(await _call(service, "cancel_all"), null);
    expect(plugin.initializations, 2);
    expect(plugin.lastInitializationSettings!.defaultIcon, "ic_new");
  });

  test(
      "platform errors keep their code, and denied exact alarms are permissions",
      () async {
    final service = _makeService();
    plugin.operationError = PlatformException(
        code: "exact_alarms_not_permitted",
        message: "Exact alarms are not permitted");
    expect(
        await _call(service, "can_schedule_exact_alarms"),
        "permission_denied: exact_alarms_not_permitted: "
        "Exact alarms are not permitted");
    plugin.operationError = PlatformException(
        code: "invalid_icon", message: "The resource icon could not be found");
    expect(await _call(service, "can_schedule_exact_alarms"),
        "operation_failed: invalid_icon: The resource icon could not be found");
  });

  test("dispatcher distinguishes unsupported operations from native failures",
      () async {
    final service = _makeService();
    expect(await _reinitialize(service), null);
    final operations = <(String, Map<String, Object?>?, String)>[
      ("show", {"id": 4}, "operation_failed"),
      (
        "schedule",
        {
          "id": 4,
          "when": {"iso": "2099-01-01T12:00:00"}
        },
        "operation_failed"
      ),
      (
        "periodically_show",
        {"id": 4, "repeat_interval": "hourly"},
        "operation_failed"
      ),
      (
        "periodically_show",
        {"id": 4, "repeat_interval": 60000},
        "operation_failed"
      ),
      ("get_pending", null, "operation_failed"),
      ("get_active", null, "operation_failed"),
      ("get_notification_channels", null, "operation_failed"),
      (
        "create_notification_channel",
        {"id": "alerts", "name": "Alerts"},
        "operation_failed"
      ),
      (
        "delete_notification_channel",
        {"channel_id": "alerts"},
        "operation_failed"
      ),
      (
        "create_notification_channel_group",
        {"group_id": "alerts", "name": "Alerts"},
        "operation_failed"
      ),
      (
        "delete_notification_channel_group",
        {"group_id": "alerts"},
        "operation_failed"
      ),
      ("start_foreground_service", {"id": 4}, "operation_failed"),
      ("stop_foreground_service", null, "operation_failed"),
      ("cancel", {"id": 4}, "operation_failed"),
      ("cancel_all", null, "operation_failed"),
      ("cancel_all_pending", null, "operation_failed"),
      for (final method in [
        "request_permissions",
        "can_schedule_exact_alarms",
        "request_exact_alarm_permission",
        "are_notifications_enabled",
        "open_app_settings",
        "request_full_screen_intent",
        "has_notification_policy_access",
        "request_notification_policy_access"
      ])
        (method, null, "operation_failed"),
    ];
    for (final error in [
      UnsupportedError("feature unavailable"),
      UnimplementedError("feature unavailable"),
      StateError("native failure: keep this detail"),
      const FormatException("native format failure"),
    ]) {
      plugin.operationError = error;
      for (final (method, args, code) in operations) {
        final result = await _call(service, method, args);
        if (error is UnsupportedError || error is UnimplementedError) {
          expect(result,
              "unsupported_platform: $method is not available on this platform");
        } else {
          expect(result, "$code: $error", reason: method);
        }
      }
    }
  });

  test("parser errors keep their codes across notification methods", () async {
    final service = _makeService();
    for (final method in [
      "show",
      "schedule",
      "periodically_show",
      "start_foreground_service"
    ]) {
      final args = {
        "id": 4,
        "when": {"iso": "2099-01-01T12:00:00"},
        "repeat_interval": "hourly"
      };
      expect(
          await _call(service, method, {
            ...args,
            "actions": [{}]
          }),
          startsWith("invalid_argument: "));
      for (final options in [
        {
          "android": {"icon": 42}
        },
        {
          "android": {"timestamp": "invalid"}
        },
      ]) {
        expect(await _call(service, method, {...args, "options": options}),
            startsWith("invalid_argument: "));
      }
    }
    for (final when in [
      null,
      {"iso": "invalid"},
      {"iso": "2099-01-01T12:00:00", "timezone": "Invalid/Zone"},
      {"delay": "invalid"},
      {"iso": 42},
    ]) {
      expect(await _call(service, "schedule", {"id": 4, "when": when}),
          startsWith("invalid_argument: "));
    }
    expect(
        await _call(service, "create_notification_channel",
            {"id": "", "name": "Alerts"}),
        startsWith("invalid_argument: "));
    expect(await _call(service, "unknown"),
        "operation_failed: unknown method unknown");
    expect(plugin.shown, isEmpty);
    expect(plugin.foregroundStarts, 0);
    expect(plugin.channelsCreated, isEmpty);
  });

  for (final throws in [false, true]) {
    test("failed initialization ($throws) blocks showing and allows retry",
        () async {
      plugin.initializationResult = false;
      plugin.failInitialization = throws;
      final service = _makeService();
      final failure = await _call(service, "show", {"id": 1});
      expect(failure, startsWith("initialization_failed: "));
      // The cause of the failure, not a generic message, reaches Python.
      expect(failure, isNot(contains("notification backend unavailable")));
      expect(plugin.shown, isEmpty);
      plugin.initializationResult = true;
      plugin.failInitialization = false;
      expect(await _call(service, "show", {"id": 1}), null);
      expect(plugin.initializations, 2);
      expect(plugin.shown, hasLength(1));
      // Action buttons must not reinitialize non-Apple backends.
      expect(
          await _call(service, "show", {
            "id": 2,
            "actions": [
              {"id": "open", "title": "Open"}
            ],
          }),
          null);
      expect(plugin.initializations, 2);
    });
  }

  test("concurrent explicit and implicit initialization share a failed attempt",
      () async {
    final gate = Completer<void>();
    final started = Completer<void>();
    plugin.initializationGate = gate.future;
    plugin.initializationStarted = started;
    plugin.initializationResult = false;
    final service = _makeService();
    final results = Future.wait([
      _reinitialize(service),
      _reinitialize(service),
      _call(service, "show", {"id": 1}),
    ]);
    await started.future;
    expect(plugin.initializations, 1);
    gate.complete();
    expect(await results, everyElement(startsWith("initialization_failed: ")));
    expect(plugin.shown, isEmpty);
    plugin.initializationStarted = null;
    plugin.initializationGate = null;
    plugin.initializationResult = true;
    expect(await _call(service, "show", {"id": 1}), null);
    expect(plugin.initializations, 2);
  });

  test("failed forced reinitialization clears the previous ready state",
      () async {
    final service = _makeService();
    expect(await _reinitialize(service), null);
    plugin.initializationResult = false;
    expect(await _reinitialize(service), startsWith("initialization_failed: "));
    expect(await _call(service, "show", {"id": 1}),
        startsWith("initialization_failed: "));
    expect(plugin.shown, isEmpty);
    plugin.initializationResult = true;
    expect(await _call(service, "show", {"id": 1}), null);
  });

  test("Apple permission denial allows operations and category registration",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin()..initializationResult = false;
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    expect(await _reinitialize(service), null);
    expect(
        await _call(service, "show", {
          "id": 1,
          "actions": [
            {"id": "open", "title": "Open"}
          ],
        }),
        null);
    expect(macos.shownDarwin, isNotNull);
    expect(macos.initializations.last.notificationCategories, hasLength(1));
  });

  test("an absent Apple initialization result fails setup and can retry",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin()..initializationResult = null;
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    expect(await _call(service, "show", {"id": 1}),
        startsWith("initialization_failed: "));
    expect(macos.shownDarwin, isNull);
    macos.initializationResult = false;
    expect(await _call(service, "show", {"id": 1}), null);
  });

  test("failed Apple category registration blocks showing and retries setup",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    expect(await _reinitialize(service), null);
    macos.failInitialization = true;
    expect(
        await _call(service, "show", {
          "id": 1,
          "actions": [
            {"id": "open", "title": "Open"}
          ],
        }),
        startsWith("operation_failed: "));
    expect(macos.shownDarwin, isNull);
    macos.failInitialization = false;
    final retry = {
      "id": 1,
      "actions": [
        {"id": "open", "title": "Open"}
      ]
    };
    expect(await _call(service, "show", retry), null);
    expect(await _call(service, "show", retry), null);
    expect(macos.initializations, hasLength(3));
    expect(macos.initializations.last.notificationCategories, hasLength(1));
  });

  test("launch replay is once per process and allows identical later taps",
      () async {
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(
      true,
      notificationResponse: fln.NotificationResponse(
        id: 7,
        actionId: "reply",
        input: "Hello",
        payload: "conversation:7",
        notificationResponseType:
            fln.NotificationResponseType.selectedNotificationAction,
      ),
    );
    final firstControl = _RecordingControl();
    final firstService = _makeService(control: firstControl);
    expect(
        await Future.wait([
          _reinitialize(firstService),
          _reinitialize(firstService),
        ]),
        [null, null]);
    expect(await _reinitialize(firstService), null);
    expect(firstControl.events, hasLength(1));
    expect(firstControl.events.single["name"], "action");

    // A new user interaction with identical content is still delivered live.
    plugin.onResponse!(plugin.launchDetails!.notificationResponse!);
    expect(firstControl.events, hasLength(2));
    expect(firstControl.events.last, firstControl.events.first);

    // A later service, such as after a session restart, doesn't replay it.
    final nextControl = _RecordingControl();
    final nextService = _makeService(control: nextControl);
    expect(await _reinitialize(nextService), null);
    expect(nextControl.events, isEmpty);
  });

  test("a launch response also delivered live during startup is emitted once",
      () async {
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
    const response = fln.NotificationResponse(
      id: 50,
      payload: "cold launch",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(
      true,
      notificationResponse: response,
    );
    // Android delivers the launching tap live before launch details are read.
    plugin.onLaunchDetailsQuery = () => plugin.onResponse!(response);
    final control = _RecordingControl();
    final service = _makeService(control: control);
    expect(await _reinitialize(service), null);
    expect(control.events, hasLength(1));
    expect(control.events.single["name"], "tap");

    // A later tap with identical content is a new interaction and is delivered.
    plugin.onLaunchDetailsQuery = null;
    plugin.onResponse!(response);
    expect(control.events, hasLength(2));
  });

  test("responses reach the live service through an earlier one's callback",
      () async {
    const response = fln.NotificationResponse(
      id: 60,
      payload: "after restart",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    final firstControl = _RecordingControl();
    final first = _makeService(control: firstControl);
    expect(await _reinitialize(first), null);
    // Windows and Linux keep the first initialization's callback.
    final firstCallback = plugin.onResponse!;
    first.dispose();

    final nextControl = _RecordingControl();
    final next = _makeService(control: nextControl);
    expect(await _reinitialize(next), null);
    firstCallback(response);
    expect(firstControl.events, isEmpty);
    expect(nextControl.events.single["data"], containsPair("id", 60));
  });

  test("a response without a live service is replayed by the next one",
      () async {
    const response = fln.NotificationResponse(
      id: 61,
      payload: "between sessions",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    final first = _makeService(control: _RecordingControl());
    expect(await _reinitialize(first), null);
    final callback = plugin.onResponse!;
    first.dispose();
    callback(response);
    await pumpEventQueue();

    final nextControl = _RecordingControl();
    expect(await _reinitialize(_makeService(control: nextControl)), null);
    expect(nextControl.events.single["data"], containsPair("id", 61));
  });

  test("a service disposed while initializing leaves the queue to the next one",
      () async {
    final prefs = SharedPreferencesAsync();
    await prefs.setString("flet_notifications_queue_1-1",
        jsonEncode({"event": "tap", "id": 62, "payload": null, "data": {}}));
    final firstControl = _RecordingControl();
    final first = _makeService(control: firstControl);
    final initializing = _reinitialize(first);
    first.dispose();
    await initializing;
    expect(firstControl.events, isEmpty);

    final nextControl = _RecordingControl();
    expect(await _reinitialize(_makeService(control: nextControl)), null);
    expect(nextControl.events.single["data"], containsPair("id", 62));
  });

  test("reinitialization does not replay an already delivered live tap",
      () async {
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
    final control = _RecordingControl();
    final service = _makeService(control: control);
    expect(await _reinitialize(service), null);
    expect(control.events, isEmpty);

    const response = fln.NotificationResponse(
      id: 7,
      payload: "opened while running",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    plugin.onResponse!(response);
    // Android's current activity intent now exposes this same live response.
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(
      true,
      notificationResponse: response,
    );
    expect(await _reinitialize(service), null);
    expect(control.events, hasLength(1));
  });

  test("background responses are delivered while the service runs", () async {
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
    final control = _RecordingControl();
    final service = _makeService(control: control);
    expect(await _reinitialize(service), null);

    fln.NotificationResponse archive(int id) => fln.NotificationResponse(
          id: id,
          actionId: "archive",
          notificationResponseType:
              fln.NotificationResponseType.selectedNotificationAction,
        );
    // Responses arriving during a replay are delivered by a further pass.
    await Future.wait([
      notificationResponseBackground(archive(1)),
      notificationResponseBackground(archive(2)),
    ]);
    await pumpEventQueue();
    expect(control.events.map((e) => e["name"]), ["action", "action"]);
    expect(control.events.map((e) => (e["data"] as Map)["id"]), [1, 2]);
    expect(await SharedPreferencesAsync().getKeys(), isEmpty);

    // A disposed service leaves responses queued for the next one.
    service.dispose();
    await notificationResponseBackground(archive(3));
    await pumpEventQueue();
    expect(control.events, hasLength(2));
    expect(await SharedPreferencesAsync().getKeys(), hasLength(1));
  });

  test("queries return native collections with null unavailable fields",
      () async {
    plugin.pending = [
      const fln.PendingNotificationRequest(1, "Title", "Body", "payload"),
      const fln.PendingNotificationRequest(2, null, null, null),
    ];
    plugin.active = [
      const fln.ActiveNotification(
        id: 1,
        channelId: "updates",
        groupKey: "messages",
        tag: "reply",
        title: "Title",
        body: "Body",
        payload: "payload",
        bigText: "Expanded",
      ),
      const fln.ActiveNotification(),
    ];
    final service = _makeService();
    expect(await _call(service, "get_pending"), [
      {"id": 1, "title": "Title", "body": "Body", "payload": "payload"},
      {"id": 2, "title": null, "body": null, "payload": null},
    ]);
    expect(await _call(service, "get_active"), [
      {
        "id": 1,
        "channel_id": "updates",
        "group_key": "messages",
        "tag": "reply",
        "title": "Title",
        "body": "Body",
        "payload": "payload",
        "big_text": "Expanded"
      },
      {
        "id": null,
        "channel_id": null,
        "group_key": null,
        "tag": null,
        "title": null,
        "body": null,
        "payload": null,
        "big_text": null
      },
    ]);
    plugin.pending = [];
    plugin.active = [];
    for (final method in ["get_pending", "get_active"]) {
      expect(await _call(service, method), isEmpty);
    }
    plugin.failQueries = true;
    for (final method in ["get_pending", "get_active"]) {
      expect(await _call(service, method), startsWith("operation_failed: "));
    }
  });

  test("copying queried channels preserves resource and URI sound sources",
      () async {
    final service = _makeService();
    for (final sound in <fln.AndroidNotificationSound?>[
      null,
      const fln.RawResourceAndroidNotificationSound("chime"),
      const fln.UriAndroidNotificationSound(
          "content://media/internal/audio/media/1"),
      const fln.UriAndroidNotificationSound(
          "file:///storage/emulated/0/Notifications/chime.wav"),
    ]) {
      plugin.queriedChannels = [
        fln.AndroidNotificationChannel("original", "Alerts", sound: sound),
      ];
      final channels =
          await _call(service, "get_notification_channels") as List;
      final channel = channels.single as Map;
      expect(channel["sound"], sound?.sound);
      expect(
          await _call(service, "create_notification_channel", {
            ...channel,
            "id": "copy",
          }),
          null);
      final copied = plugin.channelsCreated.last.sound;
      if (sound == null) {
        expect(copied, isNull);
      } else {
        expect(copied.runtimeType, sound.runtimeType);
        expect(copied!.sound, sound.sound);
      }
    }
  });

  test("channel queries return native collections", () async {
    plugin.queriedChannels = [
      fln.AndroidNotificationChannel(
        "alerts",
        "Alerts",
        description: "Important updates",
        groupId: "updates",
        importance: fln.Importance.high,
        bypassDnd: true,
        playSound: false,
        sound: const fln.RawResourceAndroidNotificationSound("chime"),
        enableVibration: false,
        vibrationPattern: Int64List.fromList([0, 200, 100, 200]),
        showBadge: false,
        enableLights: true,
        ledColor: const Color(0x80ff0000),
      ),
    ];
    final service = _makeService();
    expect(await _call(service, "get_notification_channels"), [
      {
        "id": "alerts",
        "name": "Alerts",
        "description": "Important updates",
        "group_id": "updates",
        "importance": "high",
        "bypass_dnd": true,
        "play_sound": false,
        "sound": "chime",
        "enable_vibration": false,
        "vibration_pattern": [0, 200, 100, 200],
        "show_badge": false,
        "enable_lights": true,
        "led_color": "#80ff0000",
        "audio_attributes_usage": "notification"
      },
    ]);
    plugin.queriedChannels = null;
    expect(await _call(service, "get_notification_channels"), isEmpty);

    plugin.failQueries = true;
    expect(await _call(service, "get_notification_channels"),
        startsWith("operation_failed: "));
  });

  test("periodic intervals select presets or custom durations", () async {
    final service = _makeService();
    for (final (interval, expected) in <(Object, Object)>[
      ("HOURLY", fln.RepeatInterval.hourly),
      ({"minutes": 15}, const Duration(minutes: 15)),
      (
        {"seconds": 60, "milliseconds": 500},
        const Duration(seconds: 60, milliseconds: 500)
      ),
      (60000, const Duration(minutes: 1)),
    ]) {
      final result = await _call(service, "periodically_show", {
        "id": 1,
        "title": "Reminder",
        "body": "Take a break",
        "payload": "break",
        "repeat_interval": interval,
      });
      expect(result, null);
      expect(plugin.periodicCalls.last, {
        'interval': expected,
        'title': 'Reminder',
        'body': 'Take a break',
        'payload': 'break',
        'scheduleMode': fln.AndroidScheduleMode.inexactAllowWhileIdle,
      });
    }
  });

  test("invalid periodic intervals do not schedule notifications", () async {
    final service = _makeService();
    for (final interval in [
      {"seconds": 59, "milliseconds": 999, "microseconds": 999},
      59999,
      0,
      -1,
      "unknown",
      null,
    ]) {
      final result = await _call(service, "periodically_show", {
        "id": 1,
        "repeat_interval": interval,
      });
      expect(result, startsWith("invalid_argument: "));
    }
    expect(plugin.periodicCalls, isEmpty);
  });

  test("display timestamps preserve their instant across native details",
      () async {
    for (final timestamp in [
      DateTime.parse("2030-06-01T14:00:00.123+02:00"),
      DateTime.parse("2030-06-01T00:30:00+02:00"),
      DateTime.parse("2030-06-01T23:30:00-05:00"),
      DateTime(2030, 6, 1, 12, 0, 0, 123),
      null,
    ]) {
      final details = notification_details.parseNotificationDetails(
        actions: [],
        details: {
          "options": {
            "android": {"timestamp": timestamp, "show_timestamp": false},
            "windows": {"timestamp": timestamp},
            "web": {"timestamp": timestamp},
          },
        },
      );
      expect(details.android!.when, timestamp?.millisecondsSinceEpoch);
      expect(details.android!.showWhen, isFalse);
      expect(details.windows!.timestamp, timestamp);
      expect(details.web!.timestamp, timestamp);
    }
  });

  test("show maps actions onto AndroidNotificationAction", () async {
    final service = _makeService();
    final result = await _call(service, "show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": [
        {
          "id": "open",
          "title": "Open",
          "destructive": false,
          "foreground": true,
          "cancel_notification": true,
          "input": null,
        },
        {
          "id": "reply",
          "title": "Reply",
          "destructive": false,
          "foreground": false,
          "cancel_notification": true,
          "input": {
            "label": "Say",
            "choices": <String>[],
            "allow_free_form_input": true,
            "allowed_mime_types": <String>[],
          },
        },
      ],
    });
    expect(result, null);
    final details =
        plugin.shown.single["details"] as fln.AndroidNotificationDetails;
    expect(details.icon, isNull);
    expect(details.showWhen, isTrue);
    expect(details.audioAttributesUsage, fln.AudioAttributesUsage.notification);
    expect(details.additionalFlags, isNull);
    final actions = details.actions!;
    expect(actions, hasLength(2));
    expect(actions[0].id, "open");
    expect(actions[0].title, "Open");
    expect(actions[0].showsUserInterface, isTrue);
    expect(actions[1].id, "reply");
    expect(actions[1].showsUserInterface, isFalse);
    expect(actions[1].allowGeneratedReplies, isTrue);
    expect(actions[1].inputs, hasLength(1));
    expect(actions[1].inputs.single.label, "Say");
  });

  test("request_permissions uses the Android runtime permission", () async {
    final service = _makeService();
    expect(await _call(service, "request_permissions", null), isTrue);
    expect(plugin.permissionRequests, 1);

    plugin.permissionResult = false;
    expect(await _call(service, "request_permissions", null), isFalse);
  });

  test("boolean methods retain native grants, denials and null fallbacks",
      () async {
    final service = _makeService();
    for (final result in [true, false, null]) {
      plugin.permissionResult = result;
      for (final method in [
        "request_permissions",
        "can_schedule_exact_alarms",
        "request_exact_alarm_permission",
        "are_notifications_enabled",
        "request_full_screen_intent",
        "has_notification_policy_access",
        "request_notification_policy_access",
        "open_app_settings",
      ]) {
        expect(await _call(service, method), result ?? false, reason: method);
      }
    }
  });

  test("Android-only methods answer for the platform or do nothing elsewhere",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    fln.FlutterLocalNotificationsPlatform.instance = _FakeMacOsPlugin();
    final service = _makeService();
    // Exact timing is never restricted elsewhere.
    for (final method in [
      "can_schedule_exact_alarms",
      "request_exact_alarm_permission",
    ]) {
      expect(await _call(service, method), isTrue, reason: method);
    }
    // Full-screen intents and notification-policy access do not exist elsewhere.
    for (final method in [
      "request_full_screen_intent",
      "has_notification_policy_access",
      "request_notification_policy_access"
    ]) {
      expect(await _call(service, method), isFalse, reason: method);
    }
    expect(await _call(service, "get_notification_channels"), isEmpty);
    for (final (method, args) in [
      ("create_notification_channel", {"id": "alerts", "name": "Alerts"}),
      ("delete_notification_channel", {"channel_id": "alerts"}),
      ("create_notification_channel_group", {"group_id": "g", "name": "G"}),
      ("delete_notification_channel_group", {"group_id": "g"}),
      ("stop_foreground_service", null),
    ]) {
      expect(await _call(service, method, args), null, reason: method);
    }
    expect(await _call(service, "start_foreground_service", {"id": 1}),
        startsWith("unsupported_platform: "));
  });

  test("show forwards style onto styleInformation", () async {
    final service = _makeService();
    final result = await _call(service, "show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "options": {
        "android": {
          "style": {"_type": "big_text", "big_text": "long text"},
          "group": {
            "key": "grp",
            "summary": false,
            "alert_behavior": "summary"
          },
          "progress": {"value": 30},
        },
      },
    });
    expect(result, null);
    final details =
        plugin.shown.single["details"] as fln.AndroidNotificationDetails;
    final style = details.styleInformation;
    expect(style, isA<fln.BigTextStyleInformation>());
    expect((style as fln.BigTextStyleInformation).bigText, "long text");
    expect(details.groupKey, "grp");
    expect(details.setAsGroupSummary, isFalse);
    expect(details.groupAlertBehavior, fln.GroupAlertBehavior.summary);
    expect(details.showProgress, isTrue);
    expect(details.maxProgress, 100);
    expect(details.progress, 30);
  });

  test("show with an invalid style returns invalid_argument", () async {
    final service = _makeService();
    final result = await _call(service, "show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "options": {
        "android": {
          "style": {"_type": "nope"}
        }
      },
    });
    expect(result, startsWith("invalid_argument: "));
    expect(plugin.shown, isEmpty);
  });

  test("all notification methods report nested style failures consistently",
      () async {
    final service = _makeService();
    for (final method in [
      "show",
      "schedule",
      "periodically_show",
      "start_foreground_service"
    ]) {
      expect(
          await _call(service, method, {
            "id": 4,
            "when": {"iso": "2030-01-01T12:00:00"},
            "repeat_interval": "hourly",
            "options": {
              "android": {
                "style": {
                  "_type": "messaging",
                  "person": {"name": "Me"},
                  "messages": [
                    {
                      "text": "Hello",
                      "timestamp": "invalid",
                      "person": {"name": "Alex"}
                    }
                  ]
                },
              },
            },
          }),
          startsWith("invalid_argument: "),
          reason: method);
    }
    expect(plugin.shown, isEmpty);
    expect(plugin.periodicCalls, isEmpty);
    expect(plugin.foregroundStarts, 0);
  });

  test("show ignores an unknown Android category", () async {
    final result = await _call(_makeService(), "show", {
      "id": 1,
      "options": {
        "android": {"category": "unknown-category"},
      },
    });
    expect(result, null);
    final details =
        plugin.shown.single["details"] as fln.AndroidNotificationDetails;
    expect(details.category, isNull);
  });

  test(
      "show accepts enum names case-insensitively and falls back for unknown values",
      () async {
    final service = _makeService();
    for (final value in ["unknown", "HIGH"]) {
      expect(
          await _call(service, "show", {
            "id": 1,
            "options": {
              "android": {
                "channel": {"id": "c", "name": "C", "importance": value},
                "priority": value,
                "visibility": "PRIVATE",
              },
            },
          }),
          null);
      final details =
          plugin.shown.last["details"] as fln.AndroidNotificationDetails;
      expect(
          details.importance,
          value == "HIGH"
              ? fln.Importance.high
              : fln.Importance.defaultImportance);
      expect(details.priority,
          value == "HIGH" ? fln.Priority.high : fln.Priority.defaultPriority);
      expect(details.visibility, fln.NotificationVisibility.private);
    }
  });

  test("\"default\" names the default Android priority and importance", () {
    expect(parsePriority("default", fln.Priority.high),
        fln.Priority.defaultPriority);
    expect(parseNotificationImportance("default", fln.Importance.high),
        fln.Importance.defaultImportance);
    expect(notificationImportanceName(fln.Importance.defaultImportance),
        "default");
    expect(notificationImportanceName(fln.Importance.high), "high");
  });

  test("Windows sounds are selected by name and can loop", () {
    fln.WindowsNotificationAudio? audio(Map<String, Object?> windows) =>
        notification_details
            .parseNotificationDetails(
              actions: const [],
              details: {
                "options": {"windows": windows},
              },
            )
            .windows!
            .audio;

    // Every plugin sound is reachable by its name, "default" included.
    for (final sound in fln.WindowsNotificationSound.values) {
      final name = sound == fln.WindowsNotificationSound.defaultSound
          ? "default"
          : sound.toString().split(".").last;
      expect(audio({"sound": name})!.source, sound.name, reason: name);
    }
    expect(audio({"sound": "alarm3"})!.shouldLoop, isFalse);
    final looping = audio({"sound": "call10", "loop_sound": true})!;
    expect(looping.source, fln.WindowsNotificationSound.call10.name);
    expect(looping.shouldLoop, isTrue);
    expect(audio({"sound": "silent"})!.isSilent, isTrue);
    expect(audio({"sound": "unknown"})!.source,
        fln.WindowsNotificationSound.defaultSound.name);
    expect(audio({}), isNull);
  });

  test("Windows progress counts up to its max", () {
    double? value(Map<String, Object?> progress) =>
        parseWindowsProgress({"status": "Downloading", ...progress}).value;
    expect(value({}), 0);
    expect(value({"value": 30}), 0.3);
    expect(value({"value": 3, "max": 10}), 0.3);
    expect(value({"value": 30, "max": 0}), 0);
    expect(value({"value": 150}), 1);
    expect(value({"value": 30, "indeterminate": true}), isNull);

    final details = notification_details.parseNotificationDetails(
      actions: const [],
      details: {
        "options": {
          "windows": {
            "progress": {
              "status": "Downloading",
              "value": 3,
              "max": 10,
              "title": "report.pdf",
              "label": "3/10",
            },
          },
        },
      },
    );
    final bar = details.windows!.progressBars.single;
    expect(bar.status, "Downloading");
    expect(bar.title, "report.pdf");
    expect(bar.label, "3/10");
    expect(details.windows!.progressBars.single.value, 0.3);
  });

  test("Windows progress updates in place and reports dismissed notifications",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.windows;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final windows = _FakeWindowsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = windows;
    final service = _makeService();

    expect(
        await _call(service, "update_windows_progress", {
          "id": 5,
          "progress": {
            "status": "Downloading",
            "value": 3,
            "max": 10,
            "label": "3/10",
          },
        }),
        true);
    final (id, bar) = windows.updates.single;
    expect(id, 5);
    expect(bar.id, "progress");
    expect(bar.value, 0.3);
    expect(bar.label, "3/10");

    expect(
        await _call(service, "update_windows_progress", {
          "id": 5,
          "progress": {"status": "Downloading", "indeterminate": true},
        }),
        true);
    expect(windows.updates.last.$2.value, isNull);
    expect(windows.updates.last.$2.label, isNull);

    const progress = {
      "id": 5,
      "progress": {"status": "Downloading"},
    };
    windows.updateResult = fln.NotificationUpdateResult.notFound;
    expect(await _call(service, "update_windows_progress", progress), false);
    windows.updateResult = fln.NotificationUpdateResult.error;
    expect(await _call(service, "update_windows_progress", progress),
        startsWith("operation_failed: "));
  });

  test("Windows progress updates are unsupported elsewhere", () async {
    expect(
        await _call(_makeService(), "update_windows_progress", {
          "id": 5,
          "progress": {"status": "Downloading"},
        }),
        startsWith("unsupported_platform: "));
  });

  test("Linux timeouts accept duration maps and retain sentinel values",
      () async {
    final cases = <(Object?, int)>[
      ({"seconds": 5}, 5000),
      (5000, 5000),
      (0, 0),
      (-1, -1),
      (null, -1),
    ];
    for (final (timeout, expected) in cases) {
      final details = notification_details.parseNotificationDetails(
        actions: const [],
        details: {
          "options": {
            "linux": {"timeout": timeout}
          }
        },
      );
      expect(details.linux!.timeout.value, expected);
    }
  });

  test("Android durations convert maps and integer milliseconds", () async {
    final cases = <(Map<String, dynamic>, int, int, int)>[
      (
        {
          "timeout_after": {"minutes": 1},
          "led_on_duration": {"milliseconds": 100},
          "led_off_duration": {"milliseconds": 200},
        },
        60000,
        100,
        200
      ),
      (
        {
          "timeout_after": 60000,
          "led_on_duration": 100,
          "led_off_duration": 200
        },
        60000,
        100,
        200
      ),
      (
        {"timeout_after": 0, "led_on_duration": 0, "led_off_duration": 0},
        0,
        0,
        0
      ),
    ];
    final service = _makeService();
    for (final (options, timeout, on, off) in cases) {
      expect(
          await _call(service, "show", {
            "id": 1,
            "options": {"android": options},
          }),
          null);
      final details =
          plugin.shown.last["details"] as fln.AndroidNotificationDetails;
      expect(details.timeoutAfter, timeout);
      expect(details.ledOnMs, on);
      expect(details.ledOffMs, off);
    }
  });

  test("show uses Flet primitive parsers for notification values", () async {
    final result = await _call(_makeService(), "show", {
      "id": "7",
      "options": {
        "android": {
          "progress": {"max": "100", "value": "0", "indeterminate": "false"},
          "ongoing": "TRUE",
          "auto_cancel": "false",
          "badge_number": "0",
          "additional_flags": "36",
          "channel": {
            "id": "c",
            "name": "C",
            "vibration_pattern": [0, "250", 100],
          },
        },
      },
    });
    expect(result, null);
    expect(plugin.shown.single["id"], 7);
    final details =
        plugin.shown.single["details"] as fln.AndroidNotificationDetails;
    expect(details.showProgress, isTrue);
    expect(details.maxProgress, 100);
    expect(details.progress, 0);
    expect(details.ongoing, isTrue);
    expect(details.autoCancel, isFalse);
    expect(details.number, 0);
    expect(details.additionalFlags!.toList(), [36]);
    expect(details.vibrationPattern!.toList(), [0, 250, 100]);
  });

  test("show applies AndroidOptions onto the details", () async {
    final service = _makeService();
    final result = await _call(service, "show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "options": {
        "android": {
          "icon": "ic_stat_notify",
          "large_icon": {"_type": "file", "path": "/data/avatar.png"},
          "channel": {
            "id": "alarms",
            "name": "Alarms",
            "group_id": "urgent",
            "audio_attributes_usage": "alarm",
            "importance": "high",
            "vibration_pattern": [0, 250, 100],
            "play_sound": false,
            "sound": "alert_tone",
          },
          "additional_flags": 36,
          "ongoing": true,
          "silent": true,
          "category": "alarm",
          "priority": "max",
          "color": "#FF0000",
          "sub_text": "details",
          "badge_number": 4,
          "visibility": "private",
          "timeout_after": 60000,
          "full_screen_intent": true,
        },
      },
    });
    expect(result, null);
    final details =
        plugin.shown.single["details"] as fln.AndroidNotificationDetails;
    expect(details.icon, "ic_stat_notify");
    expect((details.largeIcon as fln.FilePathAndroidBitmap).data,
        "/data/avatar.png");
    expect(details.channelId, "alarms");
    expect(details.channelName, "Alarms");
    final channel = plugin.channelsCreated.single;
    expect(channel.id, "alarms");
    expect(channel.groupId, "urgent");
    expect(channel.importance, fln.Importance.high);
    expect(details.audioAttributesUsage, fln.AudioAttributesUsage.alarm);
    expect(details.additionalFlags!.toList(), [36]);
    expect(details.ongoing, isTrue);
    expect(details.silent, isTrue);
    expect(details.category, fln.AndroidNotificationCategory.alarm);
    expect(details.importance, fln.Importance.high);
    expect(details.priority, fln.Priority.max);
    expect(details.color, const Color(0xFFFF0000));
    expect(details.subText, "details");
    expect(details.number, 4);
    expect(details.visibility, fln.NotificationVisibility.private);
    expect(details.timeoutAfter, 60000);
    expect(details.fullScreenIntent, isTrue);
    expect(details.vibrationPattern!.toList(), [0, 250, 100]);
    expect(details.playSound, isFalse);
    expect(details.sound!.sound, "alert_tone");
  });

  test("a channel ID posts without registering a channel", () async {
    final service = _makeService();
    for (final channel in [null, "updates"]) {
      expect(
          await _call(service, "show", {
            "id": 1,
            "options": {
              "android": {"channel": channel},
            },
          }),
          null);
      final details =
          plugin.shown.last["details"] as fln.AndroidNotificationDetails;
      expect(details.channelId, channel ?? "flet_notifications");
      expect(details.channelName, "Notifications");
      expect(details.importance, fln.Importance.defaultImportance);
      expect(details.playSound, isTrue);
    }
    expect(plugin.channelsCreated, isEmpty);
  });

  test("an invalid inline channel does not post the notification", () async {
    final result = await _call(_makeService(), "show", {
      "id": 1,
      "options": {
        "android": {
          "channel": {"id": "c"},
        },
      },
    });
    expect(result, startsWith("invalid_argument: "));
    expect(plugin.shown, isEmpty);
    expect(plugin.channelsCreated, isEmpty);
  });

  for (final mask in [0, 4, 36]) {
    test("show forwards flag mask $mask and camel-case audio usage", () async {
      final service = _makeService();
      final result = await _call(service, "show", {
        "id": 1,
        "options": {
          "android": {
            "channel": {
              "id": "c",
              "name": "C",
              "audio_attributes_usage": "notificationRingtone",
            },
            "additional_flags": mask,
          },
        },
      });
      expect(result, null);
      final details =
          plugin.shown.single["details"] as fln.AndroidNotificationDetails;
      expect(
        details.audioAttributesUsage,
        fln.AudioAttributesUsage.notificationRingtone,
      );
      expect(details.additionalFlags!.toList(), [mask]);
    });
  }

  test(
      "Apple categories are shared by identical actions and kept for each variant",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    final open = <String, Object?>{"id": "open", "title": "Open"};
    final reply = <String, Object?>{
      "id": "reply",
      "title": "Reply",
      "input": {"label": "Message"}
    };
    final original = [open, reply];
    Future<dynamic> show(List<Map<String, Object?>> actions, {int id = 1}) =>
        _call(service, "show", {"id": id, "actions": actions});
    expect(await show(original), null);
    final initializations = macos.initializations.length;
    expect(
        await _call(service, "show", {
          "id": 1,
          "title": "Updated",
          "body": "Progress",
          "payload": "updated",
          "options": {
            "android": {
              "progress": {"value": 25, "max": 100},
            },
          },
          "actions": [
            {...open, "cancel_notification": false},
            {
              ...reply,
              "input": {
                "label": "Message",
                "choices": ["Yes"],
                "allow_free_form_input": false,
                "allowed_mime_types": ["image/png"]
              }
            },
          ],
        }),
        null);
    expect(macos.initializations, hasLength(initializations));
    // Each variant changes one Apple-visible aspect of the original actions.
    for (final actions in <List<Map<String, Object?>>>[
      [
        {...open, "title": "Open item"},
        reply
      ],
      [
        {...open, "id": "view"},
        reply
      ],
      [
        {...open, "destructive": true},
        reply
      ],
      [
        {...open, "foreground": false},
        reply
      ],
      [
        {...open, "require_authentication": true},
        reply
      ],
      [
        open,
        {
          ...reply,
          "input": {"label": "Answer"}
        }
      ],
      [
        open,
        {...reply, "input": null}
      ],
      [reply, open],
      [open],
    ]) {
      expect(await show(original), null);
      final before = macos.initializations.length;
      expect(await show(actions), null);
      expect(macos.initializations, hasLength(before + 1));
      expect(await show(actions), null);
      expect(macos.initializations, hasLength(before + 1));
    }
    // Another notification with the same actions reuses their category.
    final before = macos.initializations.length;
    expect(await show(original, id: 2), null);
    expect(macos.initializations, hasLength(before));
    // Every distinct set of actions keeps its category: the original and the
    // nine variants.
    expect(macos.initializations.last.notificationCategories, hasLength(10));
  });

  test("Apple authorization is requested only by request_permissions",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    List<bool> flags(fln.DarwinInitializationSettings settings) => [
          settings.requestAlertPermission,
          settings.requestSoundPermission,
          settings.requestBadgePermission,
          settings.requestCriticalPermission,
          settings.requestProvisionalPermission,
        ];
    expect(await _reinitialize(service), null);
    expect(flags(macos.initializations.single), everyElement(isFalse));
    // The native Apple implementation returns false when no permission is requested.
    macos.initializationResult = false;
    for (final id in [1, 2]) {
      expect(
          await _call(service, "show", {
            "id": id,
            "actions": [
              {"id": "open$id", "title": "Open"}
            ],
          }),
          null);
      expect(flags(macos.initializations.last), everyElement(isFalse));
    }
    final categories = macos.initializations.last.notificationCategories;
    expect(categories, hasLength(2));
    expect(macos.permissionRequests, isEmpty);

    expect(
        await _call(service, "request_permissions", {
          "alert": false,
          "sound": true,
          "badge": false,
          "critical": true,
          "provisional": true,
        }),
        isTrue);
    expect(macos.permissionRequests.single, {
      "alert": false,
      "sound": true,
      "badge": false,
      "critical": true,
      "provisional": true,
    });
    expect(await _reinitialize(service), null);
    expect(flags(macos.initializations.last), everyElement(isFalse));
    expect(
        macos.initializations.last.notificationCategories
            .map((c) => c.identifier),
        categories.map((c) => c.identifier));
  });

  test("reinitialization preserves all registered Apple action categories",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    for (final id in [1, 2]) {
      expect(
          await _call(service, "show", {
            "id": id,
            "actions": [
              {"id": "open$id", "title": "Open $id"},
            ],
          }),
          null);
    }
    final categories = macos.initializations.last.notificationCategories;
    expect(categories, hasLength(2));
    expect(
        categories.map((c) => c.actions.single.identifier), ["open1", "open2"]);

    expect(await _reinitialize(service), null);
    expect(
        macos.initializations.last.notificationCategories
            .map((c) => c.identifier),
        categories.map((c) => c.identifier));

    expect(
        await _call(service, "show", {
          "id": 3,
          "actions": [
            {
              "id": "reply",
              "title": "Reply",
              "input": {"label": "Message"}
            },
          ],
        }),
        null);
    final updated = macos.initializations.last.notificationCategories;
    expect(updated.map((c) => c.actions.single.identifier),
        ["open1", "open2", "reply"]);
    expect(updated.last.actions.single.buttonTitle, "Message");
  });

  test("Apple action categories survive an app restart", () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final actions = [
      {"id": "open", "title": "Open"},
    ];
    final first = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = first;
    expect(await _call(_makeService(), "show", {"id": 1, "actions": actions}),
        null);
    final identifier =
        first.initializations.last.notificationCategories.single.identifier;

    // A new service, as after a restart, registers the stored category while
    // initializing, so taps on notifications delivered earlier keep actions.
    final second = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = second;
    final service = _makeService();
    expect(await _reinitialize(service), null);
    expect(
        second.initializations.single.notificationCategories
            .map((c) => c.identifier),
        [identifier]);
    expect(await _call(service, "show", {"id": 2, "actions": actions}), null);
    expect(second.initializations, hasLength(1));
  });

  test("Apple category identifiers depend only on Apple-visible actions", () {
    List<List<Object?>> specs(Map<String, Object?> action) =>
        darwinActionSpecs(parseActions([
          {"id": "reply", "title": "Reply", ...action}
        ]));
    final base = darwinCategoryIdentifier(specs({}));
    expect(base, startsWith(darwinCategoryPrefix));
    expect(darwinCategoryIdentifier(specs({})), base);
    expect(
        darwinCategoryIdentifier(specs({"cancel_notification": false})), base);
    expect(darwinCategoryIdentifier(specs({"destructive": true})), isNot(base));
    expect(darwinCategoryIdentifier(specs({"require_authentication": true})),
        isNot(base));
  });

  test("actions can require unlocking the device on Apple platforms", () {
    final category = darwinCategory(
        "c",
        darwinActionSpecs(parseActions([
          {"id": "delete", "title": "Delete", "require_authentication": true},
          {"id": "open", "title": "Open"},
        ])));
    expect(category.actions.first.options,
        contains(fln.DarwinNotificationActionOption.authenticationRequired));
    expect(
        category.actions.last.options,
        isNot(contains(
            fln.DarwinNotificationActionOption.authenticationRequired)));
  });

  test("stored Apple categories gain the defaults of fields added since",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    const old = "${darwinCategoryPrefix}old";
    await SharedPreferencesAsync().setString(
        "flet_notifications_darwin_categories",
        jsonEncode({
          // Stored before `require_authentication` was added.
          old: [
            ["open", "Open", false, true, false, null]
          ],
          "${darwinCategoryPrefix}malformed": [
            [1, "Open"]
          ],
        }));
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    expect(await _reinitialize(_makeService()), null);
    final category = macos.initializations.single.notificationCategories.single;
    expect(category.identifier, old);
    expect(category.actions.single.identifier, "open");
    expect(category.actions.single.options,
        {fln.DarwinNotificationActionOption.foreground});
  });

  test("stored action specs complete to the specs of default actions", () {
    expect(
        completeDarwinActionSpec(["open", "Open"]),
        darwinActionSpecs(parseActions([
          {"id": "open", "title": "Open"}
        ])).single);
  });

  test("invalid scheduling arguments leave Apple categories unchanged",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    expect(await _reinitialize(service), null);
    final initializations = macos.initializations.length;
    final cases = <(String, Map<String, Object?>, String)>[
      ("schedule", {"schedule_mode": 42}, "operation_failed"),
      ("schedule", {"match_components": 42}, "operation_failed"),
      ("schedule", {"payload": 42}, "operation_failed"),
      ("periodically_show", {"repeat_interval": 59999}, "invalid_argument"),
      ("periodically_show", {"repeat_interval": "unknown"}, "invalid_argument"),
      ("periodically_show", {"repeat_interval": null}, "invalid_argument"),
      ("periodically_show", {"schedule_mode": 42}, "operation_failed"),
      ("periodically_show", {"title": 42}, "operation_failed"),
    ];
    for (final (method, invalid, code) in cases) {
      expect(
          await _call(service, method, {
            "id": 1,
            "when": {"iso": "2099-01-01T12:00:00"},
            "repeat_interval": "hourly",
            "actions": [
              {"id": "stale", "title": "Stale"}
            ],
            ...invalid,
          }),
          startsWith("$code: "));
      expect(macos.initializations, hasLength(initializations),
          reason: "$method $invalid");
    }
    expect(
        await _call(service, "show", {
          "id": 2,
          "actions": [
            {"id": "valid", "title": "Valid"}
          ],
        }),
        null);
    final categories = macos.initializations.last.notificationCategories;
    expect(categories, hasLength(1));
    expect(categories.single.actions.single.identifier, "valid");
  });

  test("schedule retains its native arguments after validation", () async {
    final service = _makeService();
    expect(
        await _call(service, "schedule", {
          "id": 4,
          "title": "Reminder",
          "body": "Meeting",
          "payload": "meeting:4",
          "when": {
            "iso": "2099-06-01T14:00:00+02:00",
            "utc_offset_seconds": 7200,
            "timezone": "UTC"
          },
          "schedule_mode": "inexactAllowWhileIdle",
          "match_components": "dayOfWeekAndTime",
        }),
        null);
    final call = plugin.scheduledCalls.single;
    expect(call["id"], 4);
    expect(call["title"], "Reminder");
    expect(call["body"], "Meeting");
    expect(call["payload"], "meeting:4");
    expect((call["scheduledDate"] as tz.TZDateTime).toUtc(),
        DateTime.utc(2099, 6, 1, 12));
    expect(call["scheduleMode"], fln.AndroidScheduleMode.inexactAllowWhileIdle);
    expect(call["matchComponents"], fln.DateTimeComponents.dayOfWeekAndTime);
  });

  test("invalid styles and details leave Apple action categories unchanged",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    expect(await _reinitialize(service), null);
    final initializations = macos.initializations.length;
    for (final (android, error) in [
      (
        {
          "style": {
            "_type": "big_picture",
            "image": {"_type": "content_uri", "uri": "content://image"}
          }
        },
        "invalid_argument: ",
      ),
      (
        {
          "style": {
            "_type": "messaging",
            "person": {"name": "Me"},
            "messages": [
              {
                "text": "Hello",
                "timestamp": "invalid",
                "person": {"name": "Alex"}
              }
            ]
          }
        },
        "invalid_argument: ",
      ),
      ({"icon": 42}, "invalid_argument: "),
    ]) {
      expect(
          await _call(service, "show", {
            "id": 1,
            "actions": [
              {"id": "open", "title": "Open"}
            ],
            "options": {"android": android},
          }),
          startsWith(error));
      expect(macos.initializations, hasLength(initializations));
      expect(macos.shownDarwin, isNull);
    }
    expect(
        await _call(service, "show", {
          "id": 2,
          "actions": [
            {"id": "reply", "title": "Reply"}
          ],
        }),
        null);
    expect(macos.initializations.last.notificationCategories, hasLength(1));
    expect(
        macos.initializations.last.notificationCategories.single.actions.single
            .identifier,
        "reply");
  });

  test("show applies DarwinOptions on the macOS platform", () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    final result = await _call(service, "show", {
      "id": 2,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "options": {
        "ios": {
          "badge_number": 3,
          "subtitle": "sub",
          "thread_identifier": "thread1",
          "interruption_level": "passive",
          "sound": "chime",
        },
        "macos": {
          "badge_number": 1,
          "subtitle": "sub",
          "thread_identifier": "thread1",
          "interruption_level": "passive",
          "sound": "chime",
        },
      },
    });
    expect(result, null);
    // Running on macOS applies the *macOS* options (badge 1), not iOS's.
    final details = macos.shownDarwin!;
    expect(details.badgeNumber, 1);
    expect(details.subtitle, "sub");
    expect(details.threadIdentifier, "thread1");
    expect(details.interruptionLevel, fln.InterruptionLevel.passive);
    expect(details.sound, "chime");
    expect(await _call(service, "get_notification_channels"), isEmpty);
  });

  test("Linux categories are selected by their freedesktop names", () {
    fln.LinuxNotificationCategory? category(String value) =>
        notification_details
            .parseNotificationDetails(
              actions: const [],
              details: {
                "options": {
                  "linux": {"category": value},
                },
              },
            )
            .linux!
            .category;
    expect(
        category("email.arrived"), fln.LinuxNotificationCategory.emailArrived);
    // Misspelled upstream; the freedesktop name stays the reliable key.
    expect(category("presence.offline"),
        fln.LinuxNotificationCategory.presenceOffile);
    expect(category("emailArrived"), isNull);
  });

  test(
    "Python Android category wire values select the intended native category",
    () async {
      const categories = {
        'error': fln.AndroidNotificationCategory.error,
        'message': fln.AndroidNotificationCategory.message,
        'locationSharing': fln.AndroidNotificationCategory.locationSharing,
      };
      final service = _makeService();
      for (final entry in categories.entries) {
        expect(
          await _call(service, "show", {
            "id": 1,
            "options": {
              "android": {"category": entry.key},
            },
          }),
          null,
          reason: entry.key,
        );
        final details =
            plugin.shown.last["details"] as fln.AndroidNotificationDetails;
        expect(details.category, entry.value, reason: entry.key);
      }
    },
  );

  test("foreground service forwards start type and service types", () async {
    final service = _makeService();
    final result = await _call(service, "start_foreground_service", {
      "id": 4,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "start_type": "startStickyCompatibility",
      "foreground_service_types": ["DATASYNC", "specialUse", "dataSync"],
    });
    expect(result, null);
    expect(plugin.foregroundStarts, 1);
    expect(plugin.lastStartType,
        fln.AndroidServiceStartType.startStickyCompatibility);
    expect(plugin.lastForegroundServiceTypes, {
      fln.AndroidServiceForegroundType.foregroundServiceTypeDataSync,
      fln.AndroidServiceForegroundType.foregroundServiceTypeSpecialUse,
    });
  });

  test("invalid foreground types prevent the native service from starting",
      () async {
    final service = _makeService();
    for (final value in [
      "dataSync",
      ["dataSync", "typo"],
      [42]
    ]) {
      final result = await _call(service, "start_foreground_service", {
        "id": 4,
        "foreground_service_types": value,
      });
      expect(result, startsWith("invalid_argument: "));
    }
    expect(plugin.foregroundStarts, 0);
  });

  test("absent and empty foreground types use the manifest", () async {
    final service = _makeService();
    for (final value in [null, []]) {
      expect(
          await _call(service, "start_foreground_service", {
            "id": 4,
            "foreground_service_types": value,
          }),
          null);
      expect(plugin.lastForegroundServiceTypes, isNull);
    }
    expect(plugin.foregroundStarts, 2);
  });

  test("malformed reply collections return invalid_argument before showing",
      () async {
    final service = _makeService();
    for (final input in [
      {
        "choices": ["Yes", 42]
      },
      {
        "allowed_mime_types": ["image/png", 42]
      },
      {"choices": "Yes"},
      {"allowed_mime_types": "image/png"},
    ]) {
      expect(
          await _call(service, "show", {
            "id": 1,
            "actions": [
              {"id": "reply", "title": "Reply", "input": input}
            ],
          }),
          startsWith("invalid_argument: "));
    }
    expect(plugin.shown, isEmpty);
  });

  final colorCases = <String, int?>{
    '#80FF0000': 0x80FF0000,
    'red': 0xFFF44336,
    'red,0.5': 0x80F44336,
    'primary': null,
  };
  for (final entry in colorCases.entries) {
    test("show resolves accent and LED color ${entry.key}", () async {
      final service = _makeService();
      final result = await _call(service, "show", {
        "id": 1,
        "options": {
          "android": {
            "color": entry.key,
            "channel": {
              "id": "lights",
              "name": "Lights",
              "led_color": entry.key,
              "enable_lights": true,
            },
            "led_on_duration": 100,
            "led_off_duration": 200,
          },
        },
      });
      expect(result, null);
      final details =
          plugin.shown.single["details"] as fln.AndroidNotificationDetails;
      expect(details.color?.toARGB32(), entry.value);
      expect(details.ledColor?.toARGB32(), entry.value);
    });
    test("channel resolves LED color ${entry.key}", () async {
      final service = _makeService();
      final result = await _call(service, "create_notification_channel", {
        "id": "lights",
        "name": "Lights",
        "enable_lights": true,
        "led_color": entry.key,
      });
      expect(result, null);
      expect(plugin.channelsCreated.single.ledColor?.toARGB32(), entry.value);
    });
  }
}
