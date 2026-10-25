import 'dart:convert';

import 'package:flet_notifications/src/platforms/darwin.dart';
import 'package:flet_notifications/src/utils/actions.dart';
import 'package:flutter/foundation.dart'
    show debugDefaultTargetPlatformOverride, TargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUp(resetNotifications);

  test("an absent Apple initialization result fails setup and can retry",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = FakeMacOsPlugin()..initializationResult = null;
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = makeService();
    expect(await invoke(service, "show", {"id": 1}),
        startsWith("initialization_failed: "));
    expect(macos.shownDarwin, isNull);
    macos.initializationResult = false;
    expect(await invoke(service, "show", {"id": 1}), null);
  });

  test("failed Apple category registration blocks showing and retries setup",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = makeService();
    expect(await reinitializeService(service), null);
    macos.failInitialization = true;
    expect(
        await invoke(service, "show", {
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
    expect(await invoke(service, "show", retry), null);
    expect(await invoke(service, "show", retry), null);
    expect(macos.initializations, hasLength(3));
    expect(macos.initializations.last.notificationCategories, hasLength(1));
  });

  test(
      "Apple categories are shared by identical actions and kept for each variant",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = makeService();
    final open = <String, Object?>{"id": "open", "title": "Open"};
    final reply = <String, Object?>{
      "id": "reply",
      "title": "Reply",
      "input": {"label": "Message"}
    };
    final original = [open, reply];
    Future<dynamic> show(List<Map<String, Object?>> actions, {int id = 1}) =>
        invoke(service, "show", {"id": id, "actions": actions});
    expect(await show(original), null);
    final initializations = macos.initializations.length;
    expect(
        await invoke(service, "show", {
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
                "allow_free_form": false,
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
    final macos = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = makeService();
    List<bool> flags(fln.DarwinInitializationSettings settings) => [
          settings.requestAlertPermission,
          settings.requestSoundPermission,
          settings.requestBadgePermission,
          settings.requestCriticalPermission,
          settings.requestProvisionalPermission,
        ];
    expect(await reinitializeService(service), null);
    expect(flags(macos.initializations.single), everyElement(isFalse));
    // The native Apple implementation returns false when no permission is requested.
    macos.initializationResult = false;
    for (final id in [1, 2]) {
      expect(
          await invoke(service, "show", {
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
        await invoke(service, "request_permissions", {
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
    expect(await reinitializeService(service), null);
    expect(flags(macos.initializations.last), everyElement(isFalse));
    expect(
        macos.initializations.last.notificationCategories
            .map((c) => c.identifier),
        categories.map((c) => c.identifier));
  });

  test("Apple action categories survive an app restart", () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final actions = [
      {"id": "open", "title": "Open"},
    ];
    final first = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = first;
    expect(await invoke(makeService(), "show", {"id": 1, "actions": actions}),
        null);
    final identifier =
        first.initializations.last.notificationCategories.single.identifier;

    // A new service, as after a restart, registers the stored category while
    // initializing, so taps on notifications delivered earlier keep actions.
    final second = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = second;
    final service = makeService();
    expect(await reinitializeService(service), null);
    expect(
        second.initializations.single.notificationCategories
            .map((c) => c.identifier),
        [identifier]);
    expect(await invoke(service, "show", {"id": 2, "actions": actions}), null);
    expect(second.initializations, hasLength(1));
  });

  test("background actions share no native identifier with foreground ones",
      () {
    final category = darwinCategory(
        "c",
        darwinActionSpecs(parseActions([
          {"id": "open", "title": "Open"},
          {"id": "archive", "title": "Archive", "foreground": false},
        ])));
    final identifiers = category.actions.map((a) => a.identifier);
    expect(identifiers.first, "open");
    expect(identifiers.last, isNot("archive"));
    expect(darwinActionId(identifiers.last), "archive");
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
    final macos = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    expect(await reinitializeService(makeService()), null);
    final category = macos.initializations.single.notificationCategories.single;
    expect(category.identifier, old);
    expect(category.actions.single.identifier, "open");
    expect(category.actions.single.options,
        {fln.DarwinNotificationActionOption.foreground});
    // A stored spec completes to the spec of the same action parsed today.
    expect(
        completeDarwinActionSpec(["open", "Open"]),
        darwinActionSpecs(parseActions([
          {"id": "open", "title": "Open"}
        ])).single);
  });

  test("notifications reference the category registered for their actions",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = makeService();
    expect(
        await invoke(service, "show", {
          "id": 1,
          "actions": [
            {"id": "open", "title": "Open"}
          ],
        }),
        null);
    expect(macos.shownDarwin!.categoryIdentifier,
        macos.initializations.last.notificationCategories.single.identifier);
    expect(await invoke(service, "show", {"id": 2}), null);
    expect(macos.shownDarwin!.categoryIdentifier, isNull);
  });

  test("invalid arguments leave Apple action categories unchanged", () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = makeService();
    expect(await reinitializeService(service), null);
    final initializations = macos.initializations.length;
    for (final (method, invalid, code)
        in <(String, Map<String, Object?>, String)>[
      ("schedule", {"payload": 42}, "operation_failed"),
      (
        "show",
        {
          "options": {
            "android": {"icon": 42}
          }
        },
        "invalid_argument"
      ),
    ]) {
      expect(
          await invoke(service, method, {
            "id": 1,
            "when": {"iso": "2099-01-01T12:00:00"},
            "repeat_interval": "hourly",
            "actions": [
              {"id": "stale", "title": "Stale"}
            ],
            ...invalid,
          }),
          startsWith("$code: "),
          reason: "$method $invalid");
      expect(macos.initializations, hasLength(initializations));
      expect(macos.shownDarwin, isNull);
    }
    expect(
        await invoke(service, "show", {
          "id": 2,
          "actions": [
            {"id": "valid", "title": "Valid"}
          ],
        }),
        null);
    final categories = macos.initializations.last.notificationCategories;
    expect(categories.single.actions.single.identifier, "valid");
  });

  test("show applies DarwinOptions on the macOS platform", () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final macos = FakeMacOsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = macos;
    final service = makeService();
    final result = await invoke(service, "show", {
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
  });
}
