import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

import 'flutter_test_finder.dart';

class FlutterWidgetTester implements Tester {
  final WidgetTester _tester;
  final lock = Lock();
  final Completer _teardown = Completer();

  FlutterWidgetTester(this._tester);

  @override
  Future<void> pumpAndSettle(
      [Duration duration = const Duration(milliseconds: 100)]) async {
    await lock.acquire();
    try {
      await _tester.pumpAndSettle(duration);
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
  TestFinder findByTextContaining(String text) =>
      FlutterTestFinder(find.textContaining(text));

  @override
  TestFinder findByKey(Key key) => FlutterTestFinder(find.byKey(key));

  @override
  TestFinder findByTooltip(String value) =>
      FlutterTestFinder(find.byTooltip(value));

  @override
  TestFinder findByIcon(IconData icon) => FlutterTestFinder(find.byIcon(icon));

  @override
  Future<void> tap(TestFinder finder) =>
      _tester.tap((finder as FlutterTestFinder).raw);

  @override
  Future<void> enterText(TestFinder finder, String text) =>
      _tester.enterText((finder as FlutterTestFinder).raw, text);

  @override
  void teardown() => _teardown.complete();

  @override
  Future waitForTeardown() => _teardown.future;
}
