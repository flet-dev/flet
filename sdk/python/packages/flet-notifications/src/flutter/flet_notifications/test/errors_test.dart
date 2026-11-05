import 'package:flutter/services.dart' show PlatformException;
import 'package:flutter_test/flutter_test.dart';

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RecordingAndroid plugin;
  setUp(() => plugin = resetNotifications());

  test(
      "platform errors keep their code, and denied exact alarms are permissions",
      () async {
    final service = makeService();
    plugin.operationError = PlatformException(
        code: "exact_alarms_not_permitted",
        message: "Exact alarms are not permitted");
    expect(
        await invoke(service, "can_schedule_exact_alarms"),
        "permission_denied: exact_alarms_not_permitted: "
        "Exact alarms are not permitted");
    plugin.operationError = PlatformException(
        code: "invalid_icon", message: "The resource icon could not be found");
    expect(await invoke(service, "can_schedule_exact_alarms"),
        "operation_failed: invalid_icon: The resource icon could not be found");
  });

  test("native failures map to the code of their kind", () async {
    final service = makeService();
    expect(await reinitializeService(service), null);
    const unsupported =
        "unsupported_platform: show is not available on this platform";
    for (final (error, code) in <(Object, String?)>[
      (UnsupportedError("feature unavailable"), null),
      (UnimplementedError("feature unavailable"), null),
      // The plugin's own argument checks, such as a schedule date in the past.
      (ArgumentError("date must be in the future"), "invalid_argument"),
      // Unlike a parser's, a native FormatException is a failed operation.
      (const FormatException("native format failure"), "operation_failed"),
      (StateError("native failure: keep this detail"), "operation_failed"),
    ]) {
      plugin.operationError = error;
      expect(await invoke(service, "show", {"id": 4}),
          code == null ? unsupported : "$code: $error",
          reason: "$error");
    }
  });

  test("invalid arguments fail with invalid_argument before the plugin call",
      () async {
    final service = makeService();
    for (final android in [
      {"icon": 42},
      {
        "style": {"_type": "nope"}
      },
    ]) {
      expect(
          await invoke(service, "show", {
            "id": 4,
            "options": {"android": android},
          }),
          startsWith("invalid_argument: "),
          reason: "$android");
    }
    expect(
        await invoke(service, "schedule", {
          "id": 4,
          "when": {"iso": "2099-01-01T12:00:00", "timezone": "Invalid/Zone"},
        }),
        startsWith("invalid_argument: "));
    expect(await invoke(service, "unknown"),
        "operation_failed: unknown method unknown");
    expect(plugin.shown, isEmpty);
    expect(plugin.scheduledCalls, isEmpty);
  });
}
