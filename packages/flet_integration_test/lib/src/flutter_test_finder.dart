// ignore_for_file: depend_on_referenced_packages
import 'package:flutter_test/flutter_test.dart';

import 'package:flet/flet.dart';

class FlutterTestFinder extends TestFinder {
  final Finder finder;

  FlutterTestFinder(this.finder) : super();

  @override
  int get count => finder.evaluate().length;

  @override
  Finder get raw => finder;
}
