import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:python_engine/python_engine.dart';

import 'utils.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  var tmpDir = await getTemporaryDirectory();
  debugPrint("TEMP DIR IN DART: ${tmpDir.path}");

  await setupDesktop();
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _pythonEnginePlugin = PythonEngine();

  @override
  void initState() {
    super.initState();
    initPlatformState();
  }

  // Platform messages are asynchronous, so we initialize in an async method.
  Future<void> initPlatformState() async {
    var appPath =
        await extractZipArchive("assets/python-app/app.zip", "python-app");
    debugPrint("PYTHON APP PATH: $appPath");

    // Platform messages may fail, so we use a try/catch PlatformException.
    // We also handle the message potentially returning null.
    try {
      await _pythonEnginePlugin.runPython(appPath, "main") ??
          'Unknown run python result';
    } on PlatformException catch (e) {
      debugPrint('Failed to run Python: ${e.message}');
    }
  }

  @override
  Widget build(BuildContext context) {
    // TODO
    // get getTemporaryDirectory()
    // create UDS path

    return const FletApp(
      pageUrl: "http://192.168.1.243:8550/",
      assetsDir: "",
    );
  }
}
