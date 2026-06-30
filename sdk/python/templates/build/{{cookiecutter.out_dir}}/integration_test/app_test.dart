{% if cookiecutter.test_mode %}import 'package:flet_integration_test/flet_integration_test.dart';
import 'package:{{ cookiecutter.project_name }}/main.dart' as app;

// Device-mode integration test entry point. The app under test runs on-device
// with embedded Python over dart_bridge; a RemoteWidgetTester drives it over a
// raw socket connected to the pytest RemoteTester server (FLET_TEST_SERVER_URL).
void main() => runFletDeviceTest(appMain: app.main);
{% endif %}