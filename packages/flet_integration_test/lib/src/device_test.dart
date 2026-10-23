// ignore_for_file: depend_on_referenced_packages
import 'dart:async';
import 'dart:ui';

import 'package:flet/flet.dart';
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
      // pump frames here, in the test body, until it has loaded its first
      // page, so no remote command arrives before the app's UI exists.
      appMain(const []);
      await _waitForAppLoaded(tester);

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

/// Pumps frames until the on-device app has loaded its first page.
///
/// The embedded Python app can take several seconds to start, for example on
/// the first launch after a build, when antivirus software scans the bundle,
/// so a fixed number of frames is not enough. Throws when the app reports a
/// startup error or has not loaded within [timeout].
Future<void> _waitForAppLoaded(WidgetTester tester,
    {Duration timeout = const Duration(minutes: 2)}) async {
  final deadline = DateTime.now().add(timeout);
  while (true) {
    await tester.pump(const Duration(milliseconds: 100));
    final backend = _findFletBackend(tester);
    if (backend != null && !backend.isLoading) {
      if (backend.error.isNotEmpty) {
        throw Exception("The app failed to start: ${backend.error}");
      }
      return;
    }
    if (DateTime.now().isAfter(deadline)) {
      throw TimeoutException(
          "The app did not load its first page within $timeout.");
    }
  }
}

/// Returns the [FletBackend] of the first [FletApp], or `null` before the app
/// has built one.
///
/// The backend is provided below [FletApp], so it is looked up from the
/// app's descendants; the provider's own element can't see it.
FletBackend? _findFletBackend(WidgetTester tester) {
  final apps = find.byType(FletApp);
  if (apps.evaluate().isEmpty) {
    return null;
  }
  final elements = find
      .descendant(of: apps.first, matching: find.byWidgetPredicate((_) => true))
      .evaluate();
  for (final element in elements) {
    try {
      return FletBackend.of(element);
    } catch (_) {
      continue;
    }
  }
  return null;
}
