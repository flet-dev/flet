import 'dart:io';

import 'package:flet_client/main.dart' as app;
import 'package:flet_integration_test/flet_integration_test.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  var binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('end-to-end test', () {
    testWidgets('test app', (tester) async {
      var dir = Directory.current.path;
      debugPrint("Current dir: $dir");

      const testerServerUrl = String.fromEnvironment("FLET_TEST_SERVER_URL");
      FlutterWidgetTester? widgetTester;

      if (testerServerUrl.isNotEmpty) {
        debugPrint("Connecting to remote tester at $testerServerUrl");
        widgetTester = await RemoteWidgetTester.connect(
          tester: tester,
          binding: binding,
          serverUri: Uri.parse(testerServerUrl),
        );
      } else {
        widgetTester = FlutterWidgetTester(tester, binding);
        app.tester = widgetTester;
      }

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

      app.main(args);

      if (testerServerUrl.isEmpty) {
        await Future.delayed(const Duration(milliseconds: 500));
        await widgetTester?.pump(duration: const Duration(seconds: 1));
        await widgetTester?.pumpAndSettle(
          duration: const Duration(milliseconds: 100),
        );
      }
      await widgetTester?.waitForTeardown();
    });
  });
}
