import 'dart:convert';
import 'dart:ui' show Color;

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart'
    show debugDefaultTargetPlatformOverride, TargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_notifications/src/notifications_service.dart';
import 'package:timezone/timezone.dart' as tz;

/// Fake Android platform implementation recording what the service sends.
class _FakeAndroidPlugin extends fln.AndroidFlutterLocalNotificationsPlugin {
  final List<Map<String, Object?>> shown = [];
  final List<Map<String, Object?>> scheduled = [];
  final List<Map<String, Object?>> periodic = [];
  final List<int> cancelled = [];
  int cancelAllCalls = 0;
  int cancelPendingCalls = 0;
  int permissionRequests = 0;
  bool permissionResult = true;
  bool exactAlarmsAllowed = true;
  int exactAlarmRequests = 0;
  final List<fln.PendingNotificationRequest> pending = [];
  bool rejectPastSchedules = false;

  @override
  Future<bool> initialize({
    required fln.AndroidInitializationSettings settings,
    fln.DidReceiveNotificationResponseCallback? onDidReceiveNotificationResponse,
    fln.DidReceiveBackgroundNotificationResponseCallback?
    onDidReceiveBackgroundNotificationResponse,
  }) async {
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
    shown.add({
      "id": id,
      "title": title,
      "body": body,
      "payload": payload,
      "details": notificationDetails,
    });
  }

  @override
  Future<void> zonedSchedule({
    required int id,
    String? title,
    String? body,
    required tz.TZDateTime scheduledDate,
    String? payload,
    fln.DateTimeComponents? matchDateTimeComponents,
    fln.AndroidNotificationDetails? notificationDetails,
    fln.AndroidScheduleMode scheduleMode =
        fln.AndroidScheduleMode.exact,
  }) async {
    if (rejectPastSchedules) {
      // Mirrors the real platform's validateDateIsInTheFuture.
      throw ArgumentError("scheduled date must be in the future");
    }
    scheduled.add({
      "id": id,
      "title": title,
      "body": body,
      "payload": payload,
      "scheduledDate": scheduledDate,
      "matchDateTimeComponents": matchDateTimeComponents,
      "scheduleMode": scheduleMode,
      "details": notificationDetails,
    });
  }

  @override
  Future<void> periodicallyShow({
    required int id,
    String? title,
    String? body,
    required fln.RepeatInterval repeatInterval,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
    fln.AndroidScheduleMode scheduleMode = fln.AndroidScheduleMode.exact,
  }) async {
    periodic.add({
      "id": id,
      "title": title,
      "body": body,
      "payload": payload,
      "repeatInterval": repeatInterval,
      "scheduleMode": scheduleMode,
      "details": notificationDetails,
    });
  }

  @override
  Future<void> periodicallyShowWithDuration({
    required int id,
    String? title,
    String? body,
    required Duration repeatDurationInterval,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
    fln.AndroidScheduleMode scheduleMode = fln.AndroidScheduleMode.exact,
  }) async {
    periodic.add({
      "id": id,
      "title": title,
      "body": body,
      "payload": payload,
      "repeatDurationInterval": repeatDurationInterval,
      "scheduleMode": scheduleMode,
      "details": notificationDetails,
    });
  }

  @override
  Future<void> cancel({required int id, String? tag}) async {
    cancelled.add(id);
  }

  @override
  Future<void> cancelAll() async {
    cancelAllCalls++;
  }

  @override
  Future<void> cancelAllPendingNotifications() async {
    cancelPendingCalls++;
  }

  @override
  Future<List<fln.PendingNotificationRequest>> pendingNotificationRequests() async {
    return pending;
  }

  @override
  Future<bool?> requestNotificationsPermission() async {
    permissionRequests++;
    return permissionResult;
  }

  @override
  Future<bool?> canScheduleExactNotifications() async {
    return exactAlarmsAllowed;
  }

  @override
  Future<bool?> requestExactAlarmsPermission() async {
    exactAlarmRequests++;
    return true;
  }
}

LocalNotificationsService _makeService({Map<String, dynamic>? properties}) {
  final backend = FletBackend(
    pageUri: Uri.parse("uri"),
    assetsDir: "",
    extensions: [],
    multiView: false,
  );
  final control = Control(
    id: 1,
    type: "LocalNotifications",
    properties: properties ?? const {},
    backend: backend,
  );
  return LocalNotificationsService(control: control);
}

Map<String, Object?> _whenIso(String iso, {String? timeZone}) {
  return {
    "iso": iso,
    "utc_offset_seconds": null,
    "time_zone": timeZone,
  };
}

void main() {
  late _FakeAndroidPlugin plugin;

  setUp(() {
    plugin = _FakeAndroidPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = plugin;
  });

  test("show forwards id/title/body/payload to the platform", () async {
    final service = _makeService();
    final result = await service.invokeMethod("show", {
      "id": 42,
      "title": "Title",
      "body": "Body",
      "payload": "deep.link",
      "actions": null,
    });
    expect(result, "ok");
    expect(plugin.shown, hasLength(1));
    final call = plugin.shown.single;
    expect(call["id"], 42);
    expect(call["title"], "Title");
    expect(call["body"], "Body");
    expect(call["payload"], "deep.link");
    final details = call["details"] as fln.AndroidNotificationDetails?;
    expect(details, isNotNull);
    expect(details!.channelId, "flet_notifications");
    expect(details.channelName, "Notifications");
    expect(details.actions ?? const [], isEmpty);
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

  test("show with invalid action returns an error string", () async {
    final service = _makeService();
    final result = await service.invokeMethod("show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": [
        {"title": "no id"},
      ],
    });
    expect(result, startsWith("error:invalid_action:"));
    expect(plugin.shown, isEmpty);
  });

  test("cancel and cancel_all route to the platform", () async {
    final service = _makeService();
    expect(await service.invokeMethod("cancel", {"id": 9}), "ok");
    expect(plugin.cancelled, [9]);
    expect(await service.invokeMethod("cancel_all", null), "ok");
    expect(plugin.cancelAllCalls, 1);
  });

  test("request_permissions uses the Android runtime permission", () async {
    final service = _makeService();
    expect(await service.invokeMethod("request_permissions", null), "true");
    expect(plugin.permissionRequests, 1);

    plugin.permissionResult = false;
    expect(await service.invokeMethod("request_permissions", null), "false");
  });

  // ── Scheduling ────────────────────────────────────────────────────────

  test("schedule converts naive wall-clock time in the target zone",
      () async {
    final service = _makeService();
    final result = await service.invokeMethod("schedule", {
      "id": 5,
      "title": "Reminder",
      "body": "Later",
      "payload": "",
      "actions": null,
      "when": _whenIso("2030-01-15T09:30:00", timeZone: "Africa/Lagos"),
      "repeat_interval": null,
      "match_components": "time",
      "schedule_mode": "exactAllowWhileIdle",
    });
    expect(result, "ok");
    final call = plugin.scheduled.single;
    final date = call["scheduledDate"] as tz.TZDateTime;
    expect(date.year, 2030);
    expect(date.month, 1);
    expect(date.day, 15);
    expect(date.hour, 9);
    expect(date.minute, 30);
    expect(date.location.name, "Africa/Lagos");
    expect(
      call["matchDateTimeComponents"],
      fln.DateTimeComponents.time,
    );
    expect(call["scheduleMode"], fln.AndroidScheduleMode.exactAllowWhileIdle);
  });

  test("schedule preserves the instant for aware datetimes", () async {
    final service = _makeService();
    final result = await service.invokeMethod("schedule", {
      "id": 6,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "when": {
        "iso": "2030-06-01T12:00:00+01:00",
        "utc_offset_seconds": 3600,
        "time_zone": null,
      },
      "repeat_interval": null,
      "match_components": null,
      "schedule_mode": "exact",
    });
    expect(result, "ok");
    final date =
        plugin.scheduled.single["scheduledDate"] as tz.TZDateTime;
    // 12:00 +01:00 is 11:00 UTC — the instant must survive the conversion.
    expect(date.hour, 11);
    expect(date.minute, 0);
    expect(plugin.scheduled.single["scheduleMode"], fln.AndroidScheduleMode.exact);
  });

  test("schedule accepts a delay from now", () async {
    final service = _makeService();
    final result = await service.invokeMethod("schedule", {
      "id": 7,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "when": {"delay_seconds": 30, "time_zone": null},
      "repeat_interval": null,
      "match_components": null,
      "schedule_mode": "exactAllowWhileIdle",
    });
    expect(result, "ok");
    final date =
        plugin.scheduled.single["scheduledDate"] as tz.TZDateTime;
    final delta = date.difference(tz.TZDateTime.now(tz.local));
    expect(delta.inSeconds.abs(), greaterThan(25));
  });

  test("schedule failure returns an error string", () async {
    final service = _makeService();
    final result = await service.invokeMethod("schedule", {
      "id": 8,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "when": {"nonsense": true},
      "repeat_interval": null,
      "match_components": null,
      "schedule_mode": "exactAllowWhileIdle",
    });
    expect(result, startsWith("error:invalid_schedule:"));
    expect(plugin.scheduled, isEmpty);
  });

  test("schedule in the past surfaces as schedule_failed", () async {
    // The real platform rejects past dates via validateDateIsInTheFuture.
    plugin.rejectPastSchedules = true;
    final service = _makeService();
    final result = await service.invokeMethod("schedule", {
      "id": 99,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "when": {"iso": "2020-01-01T09:00:00", "utc_offset_seconds": null},
      "repeat_interval": null,
      "match_components": null,
      "schedule_mode": "exactAllowWhileIdle",
    });
    expect(result, startsWith("error:schedule_failed:"));
    expect(plugin.scheduled, isEmpty);
  });

  test("periodically_show maps the repeat interval", () async {
    final service = _makeService();
    final result = await service.invokeMethod("periodically_show", {
      "id": 9,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "repeat_interval": "daily",
      "schedule_mode": "exactAllowWhileIdle",
      "repeat_duration_seconds": null,
    });
    expect(result, "ok");
    final call = plugin.periodic.single;
    expect(call["id"], 9);
    expect(call["repeatInterval"], fln.RepeatInterval.daily);
  });

  test("periodically_show with a custom duration", () async {
    final service = _makeService();
    final result = await service.invokeMethod("periodically_show", {
      "id": 10,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "repeat_interval": "daily",
      "schedule_mode": "exactAllowWhileIdle",
      "repeat_duration_seconds": 900,
    });
    expect(result, "ok");
    final call = plugin.periodic.single;
    expect(
      call["repeatDurationInterval"],
      const Duration(seconds: 900),
    );
  });

  test("cancel_pending routes to the platform", () async {
    final service = _makeService();
    expect(await service.invokeMethod("cancel_pending", null), "ok");
    expect(plugin.cancelPendingCalls, 1);
  });

  test("get_pending returns JSON records", () async {
    plugin.pending.add(
      const fln.PendingNotificationRequest(3, "Pending", "Body", "p"),
    );
    final service = _makeService();
    final result = await service.invokeMethod("get_pending", null);
    final decoded = result is String ? jsonDecode(result) : result;
    expect(decoded, isA<List>());
    final first = (decoded as List).single as Map;
    expect(first["id"], 3);
    expect(first["title"], "Pending");
    expect(first["payload"], "p");
  });

  test("exact-alarm probes and request route to Android", () async {
    final service = _makeService();
    expect(
      await service.invokeMethod("can_schedule_exact_notifications", null),
      "true",
    );
    plugin.exactAlarmsAllowed = false;
    expect(
      await service.invokeMethod("can_schedule_exact_notifications", null),
      "false",
    );
    expect(
      await service.invokeMethod("request_exact_alarm_permission", null),
      "true",
    );
    expect(plugin.exactAlarmRequests, 1);
  });

  test("unknown method returns the unknown_method error code", () async {
    final service = _makeService();
    expect(
      await service.invokeMethod("nope", null),
      "error:unknown_method:nope",
    );
  });

  registerPhase3Tests();
}

/// Fake macOS platform implementation recording Darwin notification details.
class _FakeMacOsPlugin extends fln.MacOSFlutterLocalNotificationsPlugin {
  fln.DarwinNotificationDetails? shownDarwin;

  @override
  Future<bool?> initialize({
    required fln.DarwinInitializationSettings settings,
    fln.DidReceiveNotificationResponseCallback? onDidReceiveNotificationResponse,
  }) async {
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

// ── Phase 3: channels, styles, progress, foreground service ────────────

class _ChannelRecordingPlugin extends _FakeAndroidPlugin {
  final List<fln.AndroidNotificationChannel> channelsCreated = [];
  final List<String> channelsDeleted = [];
  final List<fln.AndroidNotificationChannel> channelsStored = [];
  int foregroundStarts = 0;
  int foregroundStops = 0;

  @override
  Future<void> createNotificationChannel(
    fln.AndroidNotificationChannel channel,
  ) async {
    channelsCreated.add(channel);
  }

  @override
  Future<void> deleteNotificationChannel({required String channelId}) async {
    channelsDeleted.add(channelId);
  }

  @override
  Future<List<fln.AndroidNotificationChannel>> getNotificationChannels() async {
    return channelsStored;
  }

  @override
  Future<void> startForegroundService({
    required int id,
    String? title,
    String? body,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
    fln.AndroidServiceStartType startType = fln.AndroidServiceStartType.startSticky,
    Set<fln.AndroidServiceForegroundType>? foregroundServiceTypes,
  }) async {
    foregroundStarts++;
    lastStartType = startType;
    lastForegroundServiceTypes = foregroundServiceTypes;
  }

  @override
  Future<void> createNotificationChannelGroup(
    fln.AndroidNotificationChannelGroup notificationChannelGroup,
  ) async {
    groupsCreated.add(notificationChannelGroup);
  }

  @override
  Future<void> stopForegroundService() async {
    foregroundStops++;
  }

  bool notificationsEnabled = true;
  int settingsOpened = 0;
  final List<fln.ActiveNotification> activeNotifications = [];
  final List<fln.AndroidNotificationChannelGroup> groupsCreated = [];
  fln.AndroidServiceStartType? lastStartType;
  Set<fln.AndroidServiceForegroundType>? lastForegroundServiceTypes;

  @override
  Future<bool?> areNotificationsEnabled() async {
    return notificationsEnabled;
  }

  @override
  Future<bool?> openAppNotificationSettings() async {
    settingsOpened++;
    return true;
  }

  @override
  Future<List<fln.ActiveNotification>> getActiveNotifications() async {
    return activeNotifications;
  }
}

void registerPhase3Tests() {
  group("Phase 3: rich notifications", () {
  late _ChannelRecordingPlugin plugin;

  setUp(() {
    plugin = _ChannelRecordingPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = plugin;
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

  test("create_notification_channel maps the config", () async {
    final service = _makeService();
    final result = await service.invokeMethod("create_notification_channel", {
      "id": "alerts",
      "name": "Alerts",
      "description": "Important stuff",
      "importance": "high",
      "bypass_dnd": true,
      "play_sound": true,
      "sound": "alert_tone",
      "enable_vibration": true,
      "vibration_pattern": [0, 250, 100],
      "show_badge": true,
      "enable_lights": false,
      "led_color": null,
    });
    expect(result, "ok");
    final channel = plugin.channelsCreated.single;
    expect(channel.id, "alerts");
    expect(channel.name, "Alerts");
    expect(channel.description, "Important stuff");
    expect(channel.importance, fln.Importance.high);
    expect(channel.bypassDnd, isTrue);
    expect(channel.sound!.sound, "alert_tone");
    expect(channel.vibrationPattern!.toList(), [0, 250, 100]);
  });

  test("create_notification_channel rejects empty id", () async {
    final service = _makeService();
    final result = await service.invokeMethod("create_notification_channel", {
      "id": "",
      "name": "x",
    });
    expect(result, "error:invalid_channel:id and name are required");
  });

  test("delete_notification_channel routes by id", () async {
    final service = _makeService();
    final result = await service.invokeMethod("delete_notification_channel", {
      "channel_id": "alerts",
    });
    expect(result, "ok");
    expect(plugin.channelsDeleted, ["alerts"]);
  });

  test("get_notification_channels returns JSON", () async {
    plugin.channelsStored.add(
      const fln.AndroidNotificationChannel("alerts", "Alerts"),
    );
    final service = _makeService();
    final result = await service.invokeMethod(
      "get_notification_channels",
      null,
    );
    final decoded = jsonDecode(result as String) as List;
    expect(decoded.single["id"], "alerts");
    expect(decoded.single["name"], "Alerts");
  });

  test("foreground service start and stop", () async {
    final service = _makeService();
    expect(
      await service.invokeMethod("start_foreground_service", {
        "id": 7,
        "title": "Syncing",
        "body": "Working…",
        "payload": "",
        "actions": null,
        "style": null,
        "show_progress": true,
        "max_progress": 100,
        "progress": 10,
        "indeterminate": false,
        "channel_id": null,
      }),
      "ok",
    );
    expect(plugin.foregroundStarts, 1);
    expect(await service.invokeMethod("stop_foreground_service", null), "ok");
    expect(plugin.foregroundStops, 1);
  });

  test("are_notifications_enabled routes to the platform probe", () async {
    final service = _makeService();
    expect(
      await service.invokeMethod("are_notifications_enabled", null),
      "true",
    );
    plugin.notificationsEnabled = false;
    expect(
      await service.invokeMethod("are_notifications_enabled", null),
      "false",
    );
  });

  test("open_app_settings routes to the platform", () async {
    final service = _makeService();
    expect(await service.invokeMethod("open_app_settings", null), "true");
    expect(plugin.settingsOpened, 1);
  });

  test("get_active returns JSON records", () async {
    plugin.activeNotifications.add(
      const fln.ActiveNotification(
        id: 3,
        channelId: "alerts",
        groupKey: "g",
        tag: "t",
        title: "T",
        body: "B",
        payload: "p",
        bigText: "long",
      ),
    );
    final service = _makeService();
    final result = await service.invokeMethod("get_active", null);
    final decoded = jsonDecode(result as String) as List;
    final first = decoded.single as Map;
    expect(first["id"], 3);
    expect(first["title"], "T");
    expect(first["payload"], "p");
    expect(first["big_text"], "long");
  });

  test("foreground service rejects id zero", () async {
    final service = _makeService();
    final result = await service.invokeMethod("start_foreground_service", {
      "id": 0,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "style": null,
      "channel_id": null,
    });
    expect(result, startsWith("error:invalid_service_id:"));
  });

  // ── Options surface (per-platform details) ───────────────────────────

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

  final colorCases = <String?, int?>{
    null: null,
    "#FF0000": 0xFFFF0000,
    "#80FF0000": 0x80FF0000,
    "  #FF0000  ": 0xFFFF0000,
    "#FFF": 0xFFFFFFFF,
    "#8FFF": 0x88FFFFFF,
    "0xff00ff00": 0xFF00FF00,
    "red": 0xFFF44336,
    "red700": 0xFFD32F2F,
    "activeBlue": 0xFF007AFF,
    "red,0.5": 0x80F44336,
    "primary": null,
    "not-a-color": null,
    "#GGGGGG": null,
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
            "led_on_ms": 100,
            "led_off_ms": 200,
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
  });

  test("unknown Android category surfaces as an error", () async {
    final service = _makeService();
    final result = await service.invokeMethod("show", {
      "id": 3,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "style": null,
      "channel_id": null,
      "options": {
        "android": {"category": "bogus"},
      },
    });
    expect(result, startsWith("error:invalid_option:"));
    expect(plugin.shown, isEmpty);
  });

  test("foreground service forwards start type and service types",
      () async {
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
      "foreground_service_types": ["dataSync", "specialUse"],
    });
    expect(result, "ok");
    expect(plugin.foregroundStarts, 1);
    expect(plugin.lastStartType, fln.AndroidServiceStartType.startStickyCompatibility);
    expect(plugin.lastForegroundServiceTypes, {
      fln.AndroidServiceForegroundType.foregroundServiceTypeDataSync,
      fln.AndroidServiceForegroundType.foregroundServiceTypeSpecialUse,
    });
  });

  test("channel group carries its description", () async {
    final service = _makeService();
    final result = await service.invokeMethod(
      "create_notification_channel_group",
      {
        "group_id": "g",
        "name": "G",
        "description": "the description",
      },
    );
    expect(result, "ok");
    expect(plugin.groupsCreated.single.description, "the description");
  });
});
}
