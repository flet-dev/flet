import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

class FlutterTestFinder extends TestFinder {
  final Finder finder;

  FlutterTestFinder(this.finder) : super();

  @override
  int get count => finder.evaluate().length;

  @override
  Finder get raw => finder;
}
