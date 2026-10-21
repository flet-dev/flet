import 'dart:ui' show Color;
import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flet_notifications/src/notifications_service.dart';
import 'package:flet_notifications/src/utils/details.dart'
    as notification_details;
import 'package:flutter/foundation.dart'
    show debugDefaultTargetPlatformOverride, TargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Records converted native details without performing operating-system actions.
class _RecordingAndroid extends fln.AndroidFlutterLocalNotificationsPlugin {
  final List<Map<String, Object?>> shown = [];
  final List<fln.AndroidNotificationChannel> channelsCreated = [];
  final List<Map<String, Object?>> periodicCalls = [];
  List<fln.PendingNotificationRequest> pending = [];
  List<fln.ActiveNotification> active = [];
  List<fln.AndroidNotificationChannel>? queriedChannels = [];
  fln.NotificationAppLaunchDetails? launchDetails;
  bool failQueries = false;
  fln.DidReceiveNotificationResponseCallback? onResponse;
  int permissionRequests = 0;
  bool permissionResult = true;
  int foregroundStarts = 0;
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
    onResponse = onDidReceiveNotificationResponse;
    return true;
  }

  @override
  Future<void> show({
    required int id,
    String? title,
    String? body,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
  }) async {
    shown.add({'id': id, 'details': notificationDetails});
  }

  @override
  Future<bool?> requestNotificationsPermission() async {
    permissionRequests++;
    return permissionResult;
  }

  @override
  Future<List<fln.PendingNotificationRequest>>
      pendingNotificationRequests() async {
    if (failQueries) throw StateError("Query unavailable");
    return pending;
  }

  @override
  Future<List<fln.ActiveNotification>> getActiveNotifications() async {
    if (failQueries) throw StateError("Query unavailable");
    return active;
  }

  @override
  Future<List<fln.AndroidNotificationChannel>?>
      getNotificationChannels() async {
    if (failQueries) throw StateError("Query unavailable");
    return queriedChannels;
  }

  @override
  Future<fln.NotificationAppLaunchDetails?>
      getNotificationAppLaunchDetails() async {
    if (failQueries) throw StateError("Query unavailable");
    return launchDetails;
  }

  @override
  Future<void> createNotificationChannel(
      fln.AndroidNotificationChannel channel) async {
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
    periodicCalls.add({
      'interval': repeatDurationInterval,
      'title': title,
      'body': body,
      'payload': payload,
      'scheduleMode': scheduleMode,
    });
  }

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
    foregroundStarts++;
    lastStartType = startType;
    lastForegroundServiceTypes = foregroundServiceTypes;
  }
}

/// Fake macOS platform implementation recording Darwin notification details.
class _FakeMacOsPlugin extends fln.MacOSFlutterLocalNotificationsPlugin {
  fln.DarwinNotificationDetails? shownDarwin;
  final List<fln.DarwinInitializationSettings> initializations = [];

  @override
  Future<bool?> initialize({
    required fln.DarwinInitializationSettings settings,
    fln.DidReceiveNotificationResponseCallback?
        onDidReceiveNotificationResponse,
  }) async {
    initializations.add(settings);
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
          type: "LocalNotifications",
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

LocalNotificationsService _makeService(
    {Map<String, dynamic>? properties, Control? control}) {
  if (control != null) return LocalNotificationsService(control: control);
  final backend = FletBackend(
    pageUri: Uri.parse("uri"),
    assetsDir: "",
    extensions: [],
    multiView: false,
  );
  final defaultControl = Control(
    id: 1,
    type: "LocalNotifications",
    properties: properties ?? const {},
    backend: backend,
  );
  return LocalNotificationsService(control: defaultControl);
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late _RecordingAndroid plugin;
  setUp(() {
    plugin = _RecordingAndroid();
    fln.FlutterLocalNotificationsPlatform.instance = plugin;
  });

  test("launch replay is once per service and allows identical later sessions",
      () async {
    SharedPreferences.setMockInitialValues({});
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
          firstService.invokeMethod("initialize"),
          firstService.invokeMethod("initialize"),
        ]),
        ["ok", "ok"]);
    expect(await firstService.invokeMethod("initialize"), "ok");
    expect(firstControl.events, hasLength(1));
    expect(firstControl.events.single["name"], "action");

    // A new user interaction with identical content is still delivered live.
    plugin.onResponse!(plugin.launchDetails!.notificationResponse!);
    expect(firstControl.events, hasLength(2));
    expect(firstControl.events.last, firstControl.events.first);

    final nextControl = _RecordingControl();
    final nextService = _makeService(control: nextControl);
    expect(await nextService.invokeMethod("initialize"), "ok");
    expect(nextControl.events, [firstControl.events.first]);
  });

  test("reinitialization does not replay an already delivered live tap",
      () async {
    SharedPreferences.setMockInitialValues({});
    final control = _RecordingControl();
    final service = _makeService(control: control);
    expect(await service.invokeMethod("initialize"), "ok");
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
    expect(await service.invokeMethod("initialize"), "ok");
    expect(control.events, hasLength(1));
  });

  test("queries return native collections with normalized unavailable fields",
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
    expect(await service.invokeMethod("get_pending"), [
      {"id": 1, "title": "Title", "body": "Body", "payload": "payload"},
      {"id": 2, "title": "", "body": "", "payload": ""},
    ]);
    expect(await service.invokeMethod("get_active"), [
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
        "id": 0,
        "channel_id": "",
        "group_key": "",
        "tag": "",
        "title": "",
        "body": "",
        "payload": "",
        "big_text": ""
      },
    ]);
    plugin.pending = [];
    plugin.active = [];
    for (final method in ["get_pending", "get_active"]) {
      expect(await service.invokeMethod(method), isEmpty);
    }
    plugin.failQueries = true;
    for (final method in ["get_pending", "get_active"]) {
      expect(await service.invokeMethod(method),
          startsWith("error:query_failed:"));
    }
  });

  test("channel and launch queries return native collections", () async {
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
    expect(await service.invokeMethod("get_notification_channels"), [
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
        "led_color": "#80ff0000"
      },
    ]);
    plugin.queriedChannels = null;
    expect(await service.invokeMethod("get_notification_channels"), isEmpty);

    expect(await service.invokeMethod("get_launch_details"),
        {"did_notification_launch_app": false});
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(true);
    expect(await service.invokeMethod("get_launch_details"),
        {"did_notification_launch_app": true, "notification": null});
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(
      true,
      notificationResponse: fln.NotificationResponse(
        id: 9,
        actionId: "reply",
        payload: "deep",
        input: "Hello",
        data: {"reply": "Hello"},
        notificationResponseType:
            fln.NotificationResponseType.selectedNotificationAction,
      ),
    );
    expect(await service.invokeMethod("get_launch_details"), {
      "did_notification_launch_app": true,
      "notification": {
        "id": 9,
        "action_id": "reply",
        "payload": "deep",
        "input": "Hello",
        "response_type": "action",
        "data": {"reply": "Hello"}
      },
    });
    plugin.failQueries = true;
    expect(await service.invokeMethod("get_notification_channels"),
        startsWith("error:channel_failed:"));
    expect(await service.invokeMethod("get_launch_details"),
        startsWith("error:query_failed:"));
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
      final result = await service.invokeMethod("periodically_show", {
        "id": 1,
        "title": "Reminder",
        "body": "Take a break",
        "payload": "break",
        "repeat_interval": interval,
      });
      expect(result, "ok");
      expect(plugin.periodicCalls.last, {
        'interval': expected,
        'title': 'Reminder',
        'body': 'Take a break',
        'payload': 'break',
        'scheduleMode': fln.AndroidScheduleMode.exactAllowWhileIdle,
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
      final result = await service.invokeMethod("periodically_show", {
        "id": 1,
        "repeat_interval": interval,
      });
      expect(result, startsWith("error:invalid_option:"));
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
        id: 1,
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
    final result = await service.invokeMethod("show", {
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
    expect(result, "ok");
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
    expect(await service.invokeMethod("request_permissions", null), "true");
    expect(plugin.permissionRequests, 1);

    plugin.permissionResult = false;
    expect(await service.invokeMethod("request_permissions", null), "false");
  });

  test("show forwards style onto styleInformation", () async {
    final service = _makeService();
    final result = await service.invokeMethod("show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "style": {"_type": "big_text", "big_text": "long text"},
      "channel_id": null,
      "group_key": "grp",
      "set_as_group_summary": false,
      "group_alert_behavior": "summary",
      "show_progress": true,
      "max_progress": 100,
      "progress": 30,
      "indeterminate": false,
    });
    expect(result, "ok");
    final details =
        plugin.shown.single["details"] as fln.AndroidNotificationDetails;
    final style = details.styleInformation;
    expect(style, isA<fln.BigTextStyleInformation>());
    expect((style as fln.BigTextStyleInformation).bigText, "long text");
    expect(details.groupKey, "grp");
    expect(details.groupAlertBehavior, fln.GroupAlertBehavior.summary);
    expect(details.showProgress, isTrue);
    expect(details.maxProgress, 100);
    expect(details.progress, 30);
  });

  test("show with an invalid style returns invalid_style", () async {
    final service = _makeService();
    final result = await service.invokeMethod("show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "style": {"_type": "nope"},
      "channel_id": null,
    });
    expect(result, startsWith("error:invalid_style:"));
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
          await service.invokeMethod(method, {
            "id": 4,
            "when": {"iso": "2030-01-01T12:00:00"},
            "repeat_interval": "hourly",
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
          }),
          startsWith("error:invalid_style:"),
          reason: method);
    }
    expect(plugin.shown, isEmpty);
    expect(plugin.periodicCalls, isEmpty);
    expect(plugin.foregroundStarts, 0);
  });

  test("show preserves invalid_option for an unknown Android category",
      () async {
    final result = await _makeService().invokeMethod("show", {
      "id": 1,
      "options": {
        "android": {"category": "unknown-category"},
      },
    });
    expect(result,
        "error:invalid_option:unknown notification category: unknown-category");
    expect(plugin.shown, isEmpty);
  });

  test(
      "show accepts enum names case-insensitively and falls back for unknown values",
      () async {
    final service = _makeService();
    for (final value in ["unknown", "HIGH"]) {
      expect(
          await service.invokeMethod("show", {
            "id": 1,
            "options": {
              "android": {
                "importance": value,
                "priority": value,
                "visibility": "PRIVATE",
              },
            },
          }),
          "ok");
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
        id: 1,
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
          await service.invokeMethod("show", {
            "id": 1,
            "options": {"android": options},
          }),
          "ok");
      final details =
          plugin.shown.last["details"] as fln.AndroidNotificationDetails;
      expect(details.timeoutAfter, timeout);
      expect(details.ledOnMs, on);
      expect(details.ledOffMs, off);
    }
  });

  test("show uses Flet primitive parsers for notification values", () async {
    final result = await _makeService().invokeMethod("show", {
      "id": "7",
      "show_progress": "true",
      "max_progress": "100",
      "progress": "0",
      "options": {
        "android": {
          "ongoing": "TRUE",
          "auto_cancel": "false",
          "number": "0",
          "additional_flags": "36",
          "vibration_pattern": [0, "250", 100],
        },
      },
    });
    expect(result, "ok");
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
    final result = await service.invokeMethod("show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "style": null,
      "channel_id": null,
      "options": {
        "android": {
          "icon": "ic_stat_notify",
          "audio_attributes_usage": "alarm",
          "additional_flags": 36,
          "ongoing": true,
          "silent": true,
          "category": "alarm",
          "importance": "high",
          "priority": "max",
          "color": "#FF0000",
          "sub_text": "details",
          "number": 4,
          "visibility": "private",
          "timeout_after": 60000,
          "full_screen_intent": true,
          "vibration_pattern": [0, 250, 100],
          "play_sound": false,
          "sound": "alert_tone",
        },
      },
    });
    expect(result, "ok");
    final details =
        plugin.shown.single["details"] as fln.AndroidNotificationDetails;
    expect(details.icon, "ic_stat_notify");
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

  for (final mask in [0, 4, 36]) {
    test("show forwards flag mask $mask and camel-case audio usage", () async {
      final service = _makeService();
      final result = await service.invokeMethod("show", {
        "id": 1,
        "options": {
          "android": {
            "audio_attributes_usage": "notificationRingtone",
            "additional_flags": mask,
          },
        },
      });
      expect(result, "ok");
      final details =
          plugin.shown.single["details"] as fln.AndroidNotificationDetails;
      expect(
        details.audioAttributesUsage,
        fln.AudioAttributesUsage.notificationRingtone,
      );
      expect(details.additionalFlags!.toList(), [mask]);
    });
  }

  test("reinitialization preserves all registered Apple action categories",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    for (final id in [1, 2]) {
      expect(
          await service.invokeMethod("show", {
            "id": id,
            "actions": [
              {"id": "open$id", "title": "Open $id"},
            ],
          }),
          "ok");
    }
    final categories = macos.initializations.last.notificationCategories;
    expect(categories, hasLength(2));
    expect(
        categories.map((c) => c.actions.single.identifier), ["open1", "open2"]);

    expect(await service.invokeMethod("initialize"), "ok");
    expect(macos.initializations.last.notificationCategories, categories);

    expect(
        await service.invokeMethod("show", {
          "id": 3,
          "actions": [
            {
              "id": "reply",
              "title": "Reply",
              "input": {"label": "Message"}
            },
          ],
        }),
        "ok");
    final updated = macos.initializations.last.notificationCategories;
    expect(updated.map((c) => c.actions.single.identifier),
        ["open1", "open2", "reply"]);
    expect(updated.last.actions.single.buttonTitle, "Message");
  });

  test("invalid styles and details leave Apple action categories unchanged",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = _FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = _makeService();
    expect(await service.invokeMethod("initialize"), "ok");
    final initializations = macos.initializations.length;
    for (final payload in [
      {
        "style": {
          "_type": "big_picture",
          "image": {"content_uri": "content://image"}
        }
      },
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
      {
        "options": {
          "android": {"category": "invalid"}
        }
      },
    ]) {
      expect(
          await service.invokeMethod("show", {
            "id": 1,
            "actions": [
              {"id": "open", "title": "Open"}
            ],
            ...payload,
          }),
          startsWith(payload.containsKey("style")
              ? "error:invalid_style:"
              : "error:invalid_option:"));
      expect(macos.initializations, hasLength(initializations));
      expect(macos.shownDarwin, isNull);
    }
    expect(
        await service.invokeMethod("show", {
          "id": 2,
          "actions": [
            {"id": "reply", "title": "Reply"}
          ],
        }),
        "ok");
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
    final result = await service.invokeMethod("show", {
      "id": 2,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "style": null,
      "channel_id": null,
      "options": {
        "iOS": {
          "badge_number": 3,
          "subtitle": "sub",
          "thread_identifier": "thread1",
          "interruption_level": "passive",
          "sound": "chime",
        },
        "macOS": {
          "badge_number": 1,
          "subtitle": "sub",
          "thread_identifier": "thread1",
          "interruption_level": "passive",
          "sound": "chime",
        },
      },
    });
    expect(result, "ok");
    // Running on macOS applies the *macOS* options (badge 1), not iOS's.
    final details = macos.shownDarwin!;
    expect(details.badgeNumber, 1);
    expect(details.subtitle, "sub");
    expect(details.threadIdentifier, "thread1");
    expect(details.interruptionLevel, fln.InterruptionLevel.passive);
    expect(details.sound, "chime");
    expect(await service.invokeMethod("get_notification_channels"), isEmpty);
  });

  test(
    "Python Linux category wire values match upstream and are accepted",
    () async {
      const categories = ['email.arrived', 'presence.offline'];
      expect(
        fln.LinuxNotificationCategory.values.map((value) => value.name),
        containsAll(categories),
      );
      final service = _makeService();
      for (final category in categories) {
        expect(
          await service.invokeMethod("show", {
            "id": 1,
            "options": {
              "linux": {"category": category},
            },
          }),
          "ok",
          reason: category,
        );
      }
      expect(plugin.shown.length, categories.length);
    },
  );

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
          await service.invokeMethod("show", {
            "id": 1,
            "options": {
              "android": {"category": entry.key},
            },
          }),
          "ok",
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
    final result = await service.invokeMethod("start_foreground_service", {
      "id": 4,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "style": null,
      "channel_id": null,
      "start_type": "startStickyCompatibility",
      "foreground_service_types": ["DATASYNC", "specialUse", "dataSync"],
    });
    expect(result, "ok");
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
      final result = await service.invokeMethod("start_foreground_service", {
        "id": 4,
        "foreground_service_types": value,
      });
      expect(result, startsWith("error:invalid_option:"));
    }
    expect(plugin.foregroundStarts, 0);
  });

  test("absent and empty foreground types use the manifest", () async {
    final service = _makeService();
    for (final value in [null, []]) {
      expect(
          await service.invokeMethod("start_foreground_service", {
            "id": 4,
            "foreground_service_types": value,
          }),
          "ok");
      expect(plugin.lastForegroundServiceTypes, isNull);
    }
    expect(plugin.foregroundStarts, 2);
  });

  test("malformed reply collections return invalid_action before showing",
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
          await service.invokeMethod("show", {
            "id": 1,
            "actions": [
              {"id": "reply", "title": "Reply", "input": input}
            ],
          }),
          startsWith("error:invalid_action:"));
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
      final result = await service.invokeMethod("show", {
        "id": 1,
        "options": {
          "android": {
            "color": entry.key,
            "led_color": entry.key,
            "enable_lights": true,
            "led_on_duration": 100,
            "led_off_duration": 200,
          },
        },
      });
      expect(result, "ok");
      final details =
          plugin.shown.single["details"] as fln.AndroidNotificationDetails;
      expect(details.color?.toARGB32(), entry.value);
      expect(details.ledColor?.toARGB32(), entry.value);
    });
    test("channel resolves LED color ${entry.key}", () async {
      final service = _makeService();
      final result = await service.invokeMethod("create_notification_channel", {
        "id": "lights",
        "name": "Lights",
        "enable_lights": true,
        "led_color": entry.key,
      });
      expect(result, "ok");
      expect(plugin.channelsCreated.single.ledColor?.toARGB32(), entry.value);
    });
  }
}
