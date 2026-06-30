// ignore_for_file: depend_on_referenced_packages
import 'dart:ui';

import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'remote_widget_tester.dart';

/// Device-mode integration test entry point for an app built with `flet build`.
///
/// The app under test runs on-device with embedded Python over the in-process
/// dart_bridge transport (via [appMain]). A [RemoteWidgetTester] connects over a
/// raw socket to the Python `RemoteTester` server (`FLET_TEST_SERVER_URL`) and
/// drives the integration-test `WidgetTester` — an independent channel that does
/// not touch Flet's own transport and adds no widget to the tree.
void runFletDeviceTest({required void Function(List<String>) appMain}) {
  var binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('end-to-end test', () {
    testWidgets('test app', (tester) async {
      const serverUrl = String.fromEnvironment("FLET_TEST_SERVER_URL");
      if (serverUrl.isEmpty) {
        throw Exception("FLET_TEST_SERVER_URL dart-define is required.");
      }

      if (!kIsWeb && defaultTargetPlatform == TargetPlatform.linux) {
        await binding.setSurfaceSize(const Size(1280, 720));
        addTearDown(() => binding.setSurfaceSize(null));
      }

      // Launch the on-device app (no args => production/dart_bridge mode) and
      // pump frames here, in the test body, so it starts and renders its first
      // UI before any remote command arrives.
      appMain(const []);
      for (var i = 0; i < 20; i++) {
        await tester.pump(const Duration(milliseconds: 100));
      }

      // Connect the remote tester last; the Python RemoteTester server unblocks
      // once connected and drives the app from here on.
      debugPrint("Connecting to remote tester at $serverUrl");
      final widgetTester = await RemoteWidgetTester.connect(
        tester: tester,
        binding: binding,
        serverUri: Uri.parse(serverUrl),
      );

      await widgetTester.waitForTeardown();
    });
  });
}
