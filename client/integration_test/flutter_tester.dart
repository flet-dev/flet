import 'dart:async';
import 'package:flet/flet.dart';
import 'package:flutter/gestures.dart';
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
  TestGesture? _gesture;

  FlutterWidgetTester(this._tester, this._binding);

  @override
  Future<void> pumpAndSettle({Duration? duration}) async {
    await lock.acquire();
    try {
      await _tester.pumpAndSettle(
        duration ?? const Duration(milliseconds: 100),
      );
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
        "Full app screenshots are only available on Android and iOS.",
      );
    }
    if (defaultTargetPlatform == TargetPlatform.android) {
      await _binding.convertFlutterSurfaceToImage();
      await _tester.pump();
    }
    var bytes = await _binding.takeScreenshot(name);
    return Uint8List.fromList(bytes);
  }

  @override
  Future<void> tap(TestFinder finder, int finderIndex) =>
      _tester.tap((finder as FlutterTestFinder).raw.at(finderIndex));

  @override
  Future<void> mouseClick(TestFinder finder, int finderIndex) async {
    final center = _tester.getCenter(
      (finder as FlutterTestFinder).raw.at(finderIndex),
    );
    await _mouseClickAt(center, kPrimaryButton);
  }

  @override
  Future<void> mouseDoubleClick(TestFinder finder, int finderIndex) async {
    final center = _tester.getCenter(
      (finder as FlutterTestFinder).raw.at(finderIndex),
    );
    await _mouseDoubleClickAt(center);
  }

  @override
  Future<void> rightMouseClick(TestFinder finder, int finderIndex) async {
    final center = _tester.getCenter(
      (finder as FlutterTestFinder).raw.at(finderIndex),
    );
    await _mouseClickAt(center, kSecondaryButton);
  }

  @override
  Future<void> tapAt(Offset offset) =>
      _tester.tapAt(offset);

  @override
  Future<void> mouseClickAt(Offset offset) => _mouseClickAt(offset, kPrimaryButton);

  @override
  Future<void> mouseDoubleClickAt(Offset offset) => _mouseDoubleClickAt(offset);

  @override
  Future<void> rightMouseClickAt(Offset offset) =>
      _mouseClickAt(offset, kSecondaryButton);

  @override
  Future<void> longPress(TestFinder finder, int finderIndex) =>
      _tester.longPress((finder as FlutterTestFinder).raw.at(finderIndex));

  @override
  Future<void> enterText(
      TestFinder finder, int finderIndex, String text) =>
      _tester.enterText(
        (finder as FlutterTestFinder).raw.at(finderIndex),
        text,
      );

  @override
  Future<void> mouseHover(TestFinder finder, int finderIndex) async {
    final center = _tester.getCenter(
      (finder as FlutterTestFinder).raw.at(finderIndex),
    );

    await _mouseExit();
    _gesture = await _tester.createGesture(kind: PointerDeviceKind.mouse);
    await _gesture?.addPointer();
    await _gesture?.moveTo(center);
  }

  Future<void> _mouseClickAt(Offset offset, int buttons) async {
    await _mouseExit();
    _gesture = await _tester.createGesture(
      kind: PointerDeviceKind.mouse,
      buttons: buttons,
    );
    await _gesture?.addPointer();
    await _gesture?.moveTo(offset);
    await _gesture?.down(offset);
    await _gesture?.up();
    await _mouseExit();
  }

  Future<void> _mouseDoubleClickAt(Offset offset) async {
    await _mouseExit();
    _gesture = await _tester.createGesture(
      kind: PointerDeviceKind.mouse,
      buttons: kPrimaryButton,
    );
    await _gesture?.addPointer();
    await _gesture?.moveTo(offset);
    await _gesture?.down(offset);
    await _gesture?.up();
    await _tester.pump(const Duration(milliseconds: 50));
    await _gesture?.down(offset);
    await _gesture?.up();
    await _mouseExit();
  }

  @override
  void teardown() => _teardown.complete();

  @override
  Future waitForTeardown() => _teardown.future;

  Future<void> _mouseExit() async {
    if (_gesture != null) {
      await _gesture?.removePointer();
      _gesture = null;
    }
  }
}
