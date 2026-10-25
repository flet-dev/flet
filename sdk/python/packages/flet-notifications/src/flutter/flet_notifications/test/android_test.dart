import 'dart:typed_data';
import 'dart:ui' show Color;

import 'package:flet_notifications/src/platforms/android.dart';
import 'package:flutter/foundation.dart'
    show debugDefaultTargetPlatformOverride, TargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RecordingAndroid plugin;
  setUp(() => plugin = resetNotifications());

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
    final service = makeService();
    expect(await invoke(service, "get_pending"), [
      {"id": 1, "title": "Title", "body": "Body", "payload": "payload"},
      {"id": 2, "title": null, "body": null, "payload": null},
    ]);
    expect(await invoke(service, "get_active"), [
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
  });

  test("copying queried channels preserves resource and URI sound sources",
      () async {
    final service = makeService();
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
      final channels = await invoke(service, "get_channels") as List;
      final channel = channels.single as Map;
      expect(channel["sound"], sound?.sound);
      expect(
          await invoke(service, "create_channel", {
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
    final service = makeService();
    expect(await invoke(service, "get_channels"), [
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
    expect(await invoke(service, "get_channels"), isEmpty);
  });

  test("show maps actions onto AndroidNotificationAction", () async {
    final service = makeService();
    final result = await invoke(service, "show", {
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
            "allow_free_form": true,
            "allowed_mime_types": <String>[],
          },
        },
      ],
    });
    expect(result, null);
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

  test("boolean methods answer false when the platform answers nothing",
      () async {
    final service = makeService();
    plugin.permissionResult = null;
    for (final method in [
      "request_permissions",
      "can_schedule_exact_alarms",
      "request_exact_alarm_permission",
      "are_notifications_enabled",
      "request_full_screen_intent",
      "has_notification_policy_access",
      "request_notification_policy_access",
      "open_settings",
    ]) {
      expect(await invoke(service, method), isFalse, reason: method);
    }
  });

  test("Android-only methods answer for the platform or do nothing elsewhere",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    fln.FlutterLocalNotificationsPlatform.instance = FakeMacOsPlugin();
    final service = makeService();
    // Exact timing is never restricted elsewhere.
    for (final method in [
      "can_schedule_exact_alarms",
      "request_exact_alarm_permission",
    ]) {
      expect(await invoke(service, method), isTrue, reason: method);
    }
    // Full-screen intents and notification-policy access do not exist elsewhere.
    for (final method in [
      "request_full_screen_intent",
      "has_notification_policy_access",
      "request_notification_policy_access"
    ]) {
      expect(await invoke(service, method), isFalse, reason: method);
    }
    expect(await invoke(service, "get_channels"), isEmpty);
    for (final (method, args) in [
      ("create_channel", {"id": "alerts", "name": "Alerts"}),
      ("delete_channel", {"channel_id": "alerts"}),
      ("create_channel_group", {"group_id": "g", "name": "G"}),
      ("delete_channel_group", {"group_id": "g"}),
      ("stop_foreground_service", null),
    ]) {
      expect(await invoke(service, method, args), null, reason: method);
    }
  });

  test("an empty cancel tag cancels the untagged notification", () async {
    final service = makeService();
    for (final tag in ["", "reply", null]) {
      expect(await invoke(service, "cancel", {"id": 3, "tag": tag}), null);
    }
    expect(plugin.cancelled, [(3, null), (3, "reply"), (3, null)]);
  });

  test("show forwards style onto styleInformation", () async {
    final service = makeService();
    final result = await invoke(service, "show", {
      "id": 1,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "options": {
        "android": {
          "style": {"_type": "big_text", "text": "long text"},
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

  test("\"default\" names the default Android priority and importance", () {
    expect(parsePriority("default", fln.Priority.high),
        fln.Priority.defaultPriority);
    expect(parseNotificationImportance("default", fln.Importance.high),
        fln.Importance.defaultImportance);
    expect(notificationImportanceName(fln.Importance.defaultImportance),
        "default");
  });

  test("show applies AndroidOptions onto the details", () async {
    final service = makeService();
    final result = await invoke(service, "show", {
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
    final service = makeService();
    for (final channel in [null, "updates"]) {
      expect(
          await invoke(service, "show", {
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

  test(
    "Python Android category wire values select the intended native category",
    () async {
      const categories = <String, fln.AndroidNotificationCategory?>{
        'error': fln.AndroidNotificationCategory.error,
        'message': fln.AndroidNotificationCategory.message,
        'locationSharing': fln.AndroidNotificationCategory.locationSharing,
        'unknown-category': null,
      };
      final service = makeService();
      for (final entry in categories.entries) {
        expect(
          await invoke(service, "show", {
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
    final service = makeService();
    final result = await invoke(service, "start_foreground_service", {
      "id": 4,
      "title": "t",
      "body": "b",
      "payload": "",
      "actions": null,
      "start_type": "startStickyCompatibility",
      "service_types": ["DATASYNC", "specialUse", "dataSync"],
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
    final service = makeService();
    for (final value in [
      "dataSync",
      ["dataSync", "typo"],
      [42]
    ]) {
      final result = await invoke(service, "start_foreground_service", {
        "id": 4,
        "service_types": value,
      });
      expect(result, startsWith("invalid_argument: "));
    }
    expect(plugin.foregroundStarts, 0);
  });

  test("absent and empty foreground types use the manifest", () async {
    final service = makeService();
    for (final value in [null, []]) {
      expect(
          await invoke(service, "start_foreground_service", {
            "id": 4,
            "service_types": value,
          }),
          null);
      expect(plugin.lastForegroundServiceTypes, isNull);
    }
    expect(plugin.foregroundStarts, 2);
  });

  test("malformed reply collections return invalid_argument before showing",
      () async {
    final service = makeService();
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
          await invoke(service, "show", {
            "id": 1,
            "actions": [
              {"id": "reply", "title": "Reply", "input": input}
            ],
          }),
          startsWith("invalid_argument: "));
    }
    expect(plugin.shown, isEmpty);
  });
}
