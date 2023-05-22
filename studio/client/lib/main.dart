import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:python_engine/python_engine.dart';

import 'utils.dart';

void main() async {
  await setupDesktop();
  // runApp(const FletApp(
  //   pageUrl: "http://Feodors-MacBook-Pro.local:8550",
  //   assetsDir: "",
  // ));
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String _runResult = 'Unknown';
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

    String runResult;
    // Platform messages may fail, so we use a try/catch PlatformException.
    // We also handle the message potentially returning null.
    try {
      runResult = await _pythonEnginePlugin.runPython(appPath, "main") ??
          'Unknown run python result';
    } on PlatformException catch (e) {
      runResult = 'Failed to run Python: ${e.message}';
    }

    // If the widget was removed from the tree while the asynchronous platform
    // message was in flight, we want to discard the reply rather than calling
    // setState to update our non-existent appearance.
    if (!mounted) return;

    setState(() {
      _runResult = runResult;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Plugin example app'),
        ),
        body: Column(
          children: [Text('Running on: $_runResult\n')],
        ),
      ),
    );
  }
}
