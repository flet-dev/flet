/// Flet integration-testing driver.
///
/// This is a separate package (not part of `package:flet`) because it depends
/// on the dev-only `flutter_test` and `integration_test` packages, which must
/// never enter a normal Flet app's runtime dependency graph. Depend on it only
/// from a Flutter integration test (under `integration_test/`), where those
/// packages are available.
library flet_integration_test;

export 'src/device_test.dart';
export 'src/flutter_test_finder.dart';
export 'src/flutter_tester.dart';
export 'src/host_test.dart';
export 'src/remote_widget_tester.dart';
