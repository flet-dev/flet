import 'dart:async';
import 'dart:ui';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'flutter_test_finder.dart';

class FlutterWidgetTester implements Tester {
  final WidgetTester _tester;
  final IntegrationTestWidgetsFlutterBinding _binding;
  final lock = Lock();
  final Completer _teardown = Completer();

  FlutterWidgetTester(this._tester, this._binding);

  @override
  Future<void> pumpAndSettle({Duration? duration}) async {
    await lock.acquire();
    try {
      await _tester
          .pumpAndSettle(duration ?? const Duration(milliseconds: 100));
    } finally {
      lock.release();
    }
  }

  @override
  Future<void> pump({Duration? duration}) async {
    await lock.acquire();
    try {
      await _tester.pump(duration);
    } finally {
      lock.release();
    }
  }

  @override
  TestFinder findByText(String text) => FlutterTestFinder(find.text(text));

  @override
  TestFinder findByTextContaining(String pattern) =>
      FlutterTestFinder(find.textContaining(RegExp(pattern)));

  @override
  TestFinder findByKey(Key key) => FlutterTestFinder(find.byKey(key));

  @override
  TestFinder findByTooltip(String value) =>
      FlutterTestFinder(find.byTooltip(value));

  @override
  TestFinder findByIcon(IconData icon) => FlutterTestFinder(find.byIcon(icon));

  @override
  Future<Uint8List> takeScreenshot(String name) async {
    if (defaultTargetPlatform != TargetPlatform.android &&
        defaultTargetPlatform != TargetPlatform.iOS) {
      throw Exception(
          "Full app screenshots are only available on Android and iOS.");
    }
    if (defaultTargetPlatform == TargetPlatform.android) {
      await _binding.convertFlutterSurfaceToImage();
      await _tester.pump();
    }
    var bytes = await _binding.takeScreenshot(name);
    return Uint8List.fromList(bytes);
  }

  @override
  Future<void> tap(TestFinder finder) =>
      _tester.tap((finder as FlutterTestFinder).raw);

  @override
  Future<void> tapAt(Offset offset) =>
      _tester.tapAt(offset);

  @override
  Future<void> longPress(TestFinder finder) =>
      _tester.longPress((finder as FlutterTestFinder).raw);

  @override
  Future<void> enterText(TestFinder finder, String text) =>
      _tester.enterText((finder as FlutterTestFinder).raw, text);

  @override
  Future<void> mouseHover(TestFinder finder) async {
    final center = _tester.getCenter((finder as FlutterTestFinder).raw);
    final gesture = await _tester.createGesture(kind: PointerDeviceKind.mouse);
    await gesture.addPointer();
    await gesture.moveTo(center);
    await pumpAndSettle();
  }

  @override
  void teardown() => _teardown.complete();

  @override
  Future waitForTeardown() => _teardown.future;
}
