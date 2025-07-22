import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

import 'flutter_test_finder.dart';

class FlutterWidgetTester implements Tester {
  final WidgetTester _tester;
  final lock = Lock();
  final Completer _teardown = Completer();

  FlutterWidgetTester(this._tester);

  @override
  Future<void> pump() async {
    await lock.acquire();
    try {
      await _tester.pump();
    } finally {
      lock.release();
    }
  }

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
  int countByText(String text) => find.text(text).evaluate().length;

  @override
  Future<void> tap(TestFinder finder) =>
      _tester.tap((finder as FlutterTestFinder).raw);

  @override
  Future<void> enterText(TestFinder finder, String text) =>
      _tester.enterText((finder as FlutterTestFinder).raw, text);

  @override
  void expect(dynamic actual, dynamic matcher) =>
      expect(actual, matcher); // shadows global `expect`

  @override
  TestFinder text(String value) => FlutterTestFinder(find.text(value));

  @override
  TestFinder tooltip(String value) => FlutterTestFinder(find.byTooltip(value));

  @override
  void teardown() => _teardown.complete();

  @override
  Future waitForTeardown() => _teardown.future;
}
