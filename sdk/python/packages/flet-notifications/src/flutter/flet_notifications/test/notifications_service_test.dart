import 'dart:ui' show Color;

import 'package:flet/flet.dart';
import 'package:flet_notifications/src/notifications_service.dart';
import 'package:flutter/foundation.dart'
    show debugDefaultTargetPlatformOverride, TargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';

/// Records converted native details without performing operating-system actions.
class _RecordingAndroid extends fln.AndroidFlutterLocalNotificationsPlugin {
  final List<Map<String, Object?>> shown = [];
  final List<fln.AndroidNotificationChannel> channelsCreated = [];
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
  }) async =>
      true;

  @override
  Future<void> show({
    required int id,
    String? title,
    String? body,
    fln.AndroidNotificationDetails? notificationDetails,
    String? payload,
  }) async {
    shown.add({'details': notificationDetails});
  }

  @override
  Future<bool?> requestNotificationsPermission() async {
    permissionRequests++;
    return permissionResult;
  }

  @override
  Future<void> createNotificationChannel(
      fln.AndroidNotificationChannel channel) async {
    channelsCreated.add(channel);
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

  @override
  Future<bool?> initialize({
    required fln.DarwinInitializationSettings settings,
    fln.DidReceiveNotificationResponseCallback?
        onDidReceiveNotificationResponse,
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

void main() {
  late _RecordingAndroid plugin;
  setUp(() {
    plugin = _RecordingAndroid();
    fln.FlutterLocalNotificationsPlatform.instance = plugin;
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
      "foreground_service_types": ["dataSync", "specialUse"],
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
}
