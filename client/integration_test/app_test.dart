import 'package:flet/testing.dart';
import 'package:flet_client/main.dart' as app;

void main() => runFletHostTest(
      appMain: app.main,
      assignTester: (t) => app.tester = t,
    );
