import 'dart:typed_data';

import 'package:flutter/widgets.dart';

import 'test_finder.dart';

abstract class Tester {
  Future<void> pumpAndSettle({Duration? duration});
  Future<void> pump({Duration? duration});
  TestFinder findByText(String text);
  TestFinder findByTextContaining(String pattern);
  TestFinder findByKey(Key key);
  TestFinder findByTooltip(String value);
  TestFinder findByIcon(IconData icon);
  Future<Uint8List> takeScreenshot(String name);
  Future<void> tap(TestFinder finder);
  Future<void> longPress(TestFinder finder);
  Future<void> enterText(TestFinder finder, String text);
  Future<void> mouseHover(TestFinder finder);
  void teardown();
  Future waitForTeardown();
}
