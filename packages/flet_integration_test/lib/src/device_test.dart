// ignore_for_file: depend_on_referenced_packages
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

  // The built app boots via the template's `BootHost` (`initState` ->
  // `await prepareApp()` -> `setState`). Under the default `fadePointers` frame
  // policy that deadlocks `flutter test`: `WidgetTester.pump()` schedules a frame
  // and blocks until it is drawn, but during this boot the frame never arrives,
  // so `pump()` hangs.
  //
  // benchmarkLive is Flutter's documented policy "for running the test on a
  // device": its `pump()` no longer waits on an engine-drawn frame (it just
  // delays), while framework-requested frames — the app's own `setState` /
  // animations, including Python's control updates arriving over dart_bridge —
  // are still serviced and rendered. The cost is that pumps no longer *force* a
  // frame, so steps that need the app to make progress (boot, command
  // round-trips) must allow real wall-clock time; see the boot loop below and
  // `FlutterWidgetTester.pumpAndSettle`.
  binding.framePolicy = LiveTestWidgetsFlutterBindingFramePolicy.benchmarkLive;

  group('end-to-end test', () {
    testWidgets('test app', (tester) async {
      const serverUrl = String.fromEnvironment("FLET_TEST_SERVER_URL");
      if (serverUrl.isEmpty) {
        throw Exception("FLET_TEST_SERVER_URL dart-define is required.");
      }

      // Launch the on-device app (no args => production/dart_bridge mode).
      appMain(const []);

      // Wait for the app to finish booting before handing off to the remote
      // tester. The boot screen shows a continuously animating
      // CircularProgressIndicator while the embedded Python starts over
      // dart_bridge, so the tree stays busy for the whole boot; once Python
      // connects, renders the first page and the boot screen fades out, the tree
      // goes idle. Interleave real delays (benchmarkLive pumps don't advance
      // wall-clock on their own) and require the tree to stay idle for several
      // consecutive checks — a single idle frame happens transiently before the
      // spinner's first tick, so breaking on it would hand off before the app has
      // rendered. Capped by a generous timeout.
      final deadline = DateTime.now().add(const Duration(seconds: 90));
      var idle = 0;
      while (DateTime.now().isBefore(deadline)) {
        await tester.runAsync(
          () => Future.delayed(const Duration(milliseconds: 200)),
        );
        await tester.pump();
        if (binding.hasScheduledFrame) {
          idle = 0;
        } else if (++idle >= 5) {
          break;
        }
      }

      // Connect the remote tester last; the Python RemoteTester server unblocks
      // once connected and drives the app from here on.
      final widgetTester = await RemoteWidgetTester.connect(
        tester: tester,
        binding: binding,
        serverUri: Uri.parse(serverUrl),
      );

      await widgetTester.waitForTeardown();
    });
  });
}
