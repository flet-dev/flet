/// Flet integration-testing driver.
///
/// This library is intentionally NOT exported from `package:flet/flet.dart`
/// because it depends on the dev-only `flutter_test` and `integration_test`
/// packages. Import it only from a Flutter integration test (under
/// `integration_test/`), where those packages are available as dev
/// dependencies.
library flet.testing;

export 'src/testing/flutter/device_test.dart';
export 'src/testing/flutter/flutter_test_finder.dart';
export 'src/testing/flutter/flutter_tester.dart';
export 'src/testing/flutter/host_test.dart';
export 'src/testing/flutter/remote_widget_tester.dart';
