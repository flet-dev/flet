import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

/// Pumps frames until the on-device app has loaded its first page.
///
/// The embedded Python app can take several seconds to start, for example on
/// the first launch after a build, when antivirus software scans the bundle,
/// so a fixed number of frames is not enough. Throws when the app reports a
/// startup error or has not loaded within [timeout].
///
/// A startup error includes the embedded Python program failing before it
/// connects, such as an exception raised while importing the app's modules.
/// The app reports that on its boot screen rather than through the Flet
/// protocol, so the thrown exception carries the boot screen's error text,
/// including the Python traceback.
Future<void> waitForAppLoaded(WidgetTester tester,
    {Duration timeout = const Duration(minutes: 2)}) async {
  final deadline = tester.binding.clock.now().add(timeout);
  while (true) {
    await tester.pump(const Duration(milliseconds: 100));
    final backend = _findFletBackend(tester);
    final bootError = backend?.bootStatus.value.error;
    if (bootError != null && bootError.isNotEmpty) {
      throw Exception("The app failed to start:\n$bootError");
    }
    if (backend != null && !backend.isLoading) {
      if (backend.error.isNotEmpty) {
        throw Exception("The app failed to start: ${backend.error}");
      }
      // The registration response clears isLoading before Python runs main().
      // The test_ready page patch follows main's initial UI updates.
      if (backend.page.internals?["test_ready"] == true) {
        return;
      }
    }
    if (tester.binding.clock.now().isAfter(deadline)) {
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
