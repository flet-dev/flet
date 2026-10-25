/// Fakes and helpers shared by the service tests.
library;

import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flet_notifications/src/notifications_service.dart';
import 'package:flet_notifications/src/utils/errors.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:shared_preferences_platform_interface/in_memory_shared_preferences_async.dart';
import 'package:shared_preferences_platform_interface/shared_preferences_async_platform_interface.dart';
import 'package:timezone/timezone.dart' as tz;

/// Records converted native details without performing operating-system actions.
class RecordingAndroid extends fln.AndroidFlutterLocalNotificationsPlugin {
  final List<Map<String, Object?>> shown = [];
  final List<fln.AndroidNotificationChannel> channelsCreated = [];
  final List<Map<String, Object?>> periodicCalls = [];
  final List<Map<String, Object?>> scheduledCalls = [];
  List<fln.PendingNotificationRequest> pending = [];
  List<fln.ActiveNotification> active = [];
  List<fln.AndroidNotificationChannel>? queriedChannels = [];
  fln.NotificationAppLaunchDetails? launchDetails;
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
    return permissionResult;
  }

  @override
  Future<List<fln.PendingNotificationRequest>>
      pendingNotificationRequests() async {
    _checkOperation();
    return pending;
  }

  @override
  Future<List<fln.ActiveNotification>> getActiveNotifications() async {
    _checkOperation();
    return active;
  }

  @override
  Future<List<fln.AndroidNotificationChannel>?>
      getNotificationChannels() async {
    _checkOperation();
    return queriedChannels;
  }

  @override
  Future<fln.NotificationAppLaunchDetails?>
      getNotificationAppLaunchDetails() async {
    _checkOperation();
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

  final List<(int, String?)> cancelled = [];

  @override
  Future<void> cancel({required int id, String? tag}) async {
    _checkOperation();
    cancelled.add((id, tag));
  }

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
class FakeWindowsPlugin extends fln.FlutterLocalNotificationsPlatform
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
class FakeMacOsPlugin extends fln.MacOSFlutterLocalNotificationsPlugin {
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

class RecordingControl extends Control {
  final List<Map<String, Object?>> events = [];

  RecordingControl()
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
Future<Object?> invoke(NotificationsService service, String method,
    [Object? args]) async {
  try {
    return await service.invokeMethod(method, args);
  } on NotificationException catch (e) {
    return e.toString();
  }
}

/// Reinitializes [service] and returns `null`, or for a failure the text Flet
/// reports to Python, as [invoke] does.
Future<Object?> reinitializeService(NotificationsService service) async {
  try {
    await service.reinitialize();
    return null;
  } on NotificationException catch (e) {
    return e.toString();
  }
}

NotificationsService makeService(
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

/// Resets the service's process-wide state and installs a fresh
/// [RecordingAndroid] as the plugin, which it returns.
RecordingAndroid resetNotifications() {
  NotificationsService.resetForTesting();
  // Persisted Apple categories must not leak between tests.
  SharedPreferencesAsyncPlatform.instance =
      InMemorySharedPreferencesAsync.empty();
  final plugin = RecordingAndroid();
  fln.FlutterLocalNotificationsPlatform.instance = plugin;
  return plugin;
}
