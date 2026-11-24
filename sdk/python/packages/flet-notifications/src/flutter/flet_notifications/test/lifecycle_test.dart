import 'dart:async';

import 'package:flutter_test/flutter_test.dart';

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RecordingAndroid plugin;
  setUp(() => plugin = resetNotifications());

  test("changing an initialization property reinitializes with the new value",
      () async {
    final service = makeService(properties: {"android_default_icon": "ic_old"});
    expect(await invoke(service, "cancel_all"), null);
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
    final service = makeService(properties: {"android_default_icon": "ic_old"});
    final pending = invoke(service, "cancel_all");
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
    final service = makeService(properties: {"android_default_icon": "ic_old"});
    expect(await invoke(service, "cancel_all"),
        startsWith("initialization_failed: "));
    expect(plugin.initializations, 1);

    service.control.properties["android_default_icon"] = "ic_new";
    service.update();
    await pumpEventQueue();
    // No extra attempt: the next method call retries.
    expect(plugin.initializations, 1);

    plugin.failInitialization = false;
    expect(await invoke(service, "cancel_all"), null);
    expect(plugin.initializations, 2);
    expect(plugin.lastInitializationSettings!.defaultIcon, "ic_new");
  });

  for (final throws in [false, true]) {
    test("failed initialization ($throws) blocks showing and allows retry",
        () async {
      plugin.initializationResult = false;
      plugin.failInitialization = throws;
      final service = makeService();
      final failure = await invoke(service, "show", {"id": 1});
      expect(failure, startsWith("initialization_failed: "));
      // The cause of the failure, not a generic message, reaches Python.
      expect(failure, isNot(contains("notification backend unavailable")));
      expect(plugin.shown, isEmpty);
      plugin.initializationResult = true;
      plugin.failInitialization = false;
      expect(await invoke(service, "show", {"id": 1}), null);
      expect(plugin.initializations, 2);
      expect(plugin.shown, hasLength(1));
      // Action buttons must not reinitialize non-Apple backends.
      expect(
          await invoke(service, "show", {
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
    final service = makeService();
    final results = Future.wait([
      reinitializeService(service),
      reinitializeService(service),
      invoke(service, "show", {"id": 1}),
    ]);
    await started.future;
    expect(plugin.initializations, 1);
    gate.complete();
    expect(await results, everyElement(startsWith("initialization_failed: ")));
    expect(plugin.shown, isEmpty);
    plugin.initializationStarted = null;
    plugin.initializationGate = null;
    plugin.initializationResult = true;
    expect(await invoke(service, "show", {"id": 1}), null);
    expect(plugin.initializations, 2);
  });

  test("failed forced reinitialization clears the previous ready state",
      () async {
    final service = makeService();
    expect(await reinitializeService(service), null);
    plugin.initializationResult = false;
    expect(await reinitializeService(service),
        startsWith("initialization_failed: "));
    expect(await invoke(service, "show", {"id": 1}),
        startsWith("initialization_failed: "));
    expect(plugin.shown, isEmpty);
    plugin.initializationResult = true;
    expect(await invoke(service, "show", {"id": 1}), null);
  });
}
