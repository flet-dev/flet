// ignore_for_file: depend_on_referenced_packages

import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:flet/flet.dart';
import 'flutter_tester.dart';

/// Runs an integration test in "host" mode: the Flet app under test runs in a
/// separate Python (pytest) process which also acts as the Flet server, and the
/// Flutter app connects back to it over a single transport (TCP/HTTP/UDS). The
/// [Tester] rides that same connection.
///
/// This is the mechanism used by the Flet dev "client" shell and the Flet
/// team's white-box tests. For testing an app built with `flet build` (embedded
/// Python over dart_bridge), use `runFletDeviceTest` instead.
///
/// [appMain] is the host app's `main(args)` entry point. [assignTester] is
/// called with the constructed [Tester] before `appMain` runs so the host can
/// wire it into its `FletApp(tester: ...)`.
void runFletHostTest({
  required void Function(List<String>) appMain,
  required void Function(Tester) assignTester,
}) {
  var binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('end-to-end test', () {
    testWidgets('test app', (tester) async {
      var dir = Directory.current.path;
      debugPrint("Current dir: $dir");

      var fletTester = FlutterWidgetTester(tester, binding);
      assignTester(fletTester);

      List<String> args = [];
      const fletTestAppUrl = String.fromEnvironment("FLET_TEST_APP_URL");
      if (fletTestAppUrl != "") {
        args.add(fletTestAppUrl);
      }

      const fletTestPidFile = String.fromEnvironment("FLET_TEST_PID_FILE_PATH");
      if (fletTestPidFile != "") {
        args.add(fletTestPidFile);
      }

      const fletTestAssetsDir = String.fromEnvironment("FLET_TEST_ASSETS_DIR");
      if (fletTestAssetsDir != "") {
        args.add(fletTestAssetsDir);
      }

      appMain(args);

      await Future.delayed(const Duration(milliseconds: 500));
      await fletTester.pump(duration: const Duration(seconds: 1));
      await fletTester.pumpAndSettle(
          duration: const Duration(milliseconds: 100));
      await fletTester.waitForTeardown();
    });
  });
}
