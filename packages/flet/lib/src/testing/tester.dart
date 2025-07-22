import 'test_finder.dart';

abstract class Tester {
  Future<void> pump();
  Future<void> pumpAndSettle([Duration duration]);
  int countByText(String text);
  Future<void> tap(TestFinder finder);
  Future<void> enterText(TestFinder finder, String text);
  void expect(dynamic actual, dynamic matcher);
  TestFinder text(String value);
  TestFinder tooltip(String value);
  void teardown();
  Future waitForTeardown();
}
