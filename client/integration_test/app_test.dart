import 'dart:io';

import 'package:flet_client/main.dart' as app;
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'flutter_tester.dart';

void main() {
  var binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('end-to-end test', () {
    testWidgets('test app', (tester) async {
      var dir = Directory.current.path;
      debugPrint("Current dir: $dir");

      app.tester = FlutterWidgetTester(tester, binding);

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

      await Future.delayed(const Duration(milliseconds: 500));
      await app.tester?.pump(duration: const Duration(seconds: 1));
      await app.tester
          ?.pumpAndSettle(duration: const Duration(milliseconds: 100));
      await app.tester?.waitForTeardown();
    });
  });
}
