import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

class FlutterTestFinder implements TestFinder {
  final Finder finder;

  FlutterTestFinder(this.finder);

  @override
  Finder get raw => finder;
}
