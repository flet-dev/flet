import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flet_integration_test/src/app_startup.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

// Keep the real FletApp/provider tree, with a small page renderer that avoids
// platform services and renders when the page patch arrives.
class _PageExtension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    if (control.type != 'Page') return null;
    return ListenableBuilder(
      listenable: control,
      builder: (_, __) => Text(control.getString('test_text', '')!),
    );
  }
}

Future<FletBackend> _mountApp(WidgetTester tester) async {
  late FletBackend backend;
  await tester.pumpWidget(Directionality(
    textDirection: TextDirection.ltr,
    child: FletApp(
      pageUrl: 'mock',
      assetsDir: '',
      extensions: [_PageExtension()],
      onBackendCreated: (created) => backend = created,
    ),
  ));
  return backend;
}

void main() {
  testWidgets('registration alone does not finish the startup wait',
      (tester) async {
    final backend = await _mountApp(tester);
    backend.isLoading = false; // Registration arrives before main().
    Timer(const Duration(milliseconds: 500), () {
      backend.page.update({
        'test_text': 'Ready',
        '_internals': {'test_ready': true},
      }, shouldNotify: true);
    });

    await waitForAppLoaded(tester);

    // The wait must also pump the frame containing main's final page patch.
    expect(find.text('Ready'), findsOneWidget);
  });

  testWidgets('an intentionally empty app can finish loading', (tester) async {
    final backend = await _mountApp(tester);
    backend.isLoading = false;
    backend.page.update({
      '_internals': {'test_ready': true},
    }, shouldNotify: true);

    await waitForAppLoaded(tester);
  });

  testWidgets('errors after registration fail instead of connecting the tester',
      (tester) async {
    final backend = await _mountApp(tester);
    backend.isLoading = false;
    Timer(const Duration(milliseconds: 300), () {
      backend.error = 'Initialization failed';
    });

    await expectLater(
        () => waitForAppLoaded(tester),
        throwsA(isA<Exception>().having((e) => e.toString(), 'message',
            contains('Initialization failed'))));
  });

  testWidgets('a registered app that never initializes times out',
      (tester) async {
    final backend = await _mountApp(tester);
    backend.isLoading = false;

    await expectLater(
      () => waitForAppLoaded(tester, timeout: const Duration(seconds: 1)),
      throwsA(isA<TimeoutException>()),
    );
  });

  testWidgets('a missing FletApp times out', (tester) async {
    await expectLater(
      () => waitForAppLoaded(tester, timeout: const Duration(seconds: 1)),
      throwsA(isA<TimeoutException>()),
    );
  });
}
