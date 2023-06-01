import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:python_engine/python_engine.dart';

void main() {
  startPythonProgram();
  runApp(const MyApp());
}

void startPythonProgram() async {
  debugPrint("startPythonProgram()");
  WidgetsFlutterBinding.ensureInitialized();
  Directory directory = await getApplicationDocumentsDirectory();
  var appPath = p.join(directory.path, "main.py");
  ByteData data = await rootBundle.load("app/main.py");
  List<int> bytes =
      data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes);
  await File(appPath).writeAsBytes(bytes);

  var pythonEnginePlugin = PythonEngine();
  pythonEnginePlugin.runPython(appPath,
      modulePaths: ["main"], environmentVariables: {"a": "1", "b": "2"});
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Plugin example app'),
        ),
        body: const Center(
          child: Text('Hello!'),
        ),
      ),
    );
  }
}
