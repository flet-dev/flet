import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:python_engine/python_engine.dart';

import 'utils.dart';

void main() async {
  startPythonProgram();
  await setupDesktop();
  runApp(const FletApp(
    pageUrl: "flet.sock",
    assetsDir: "",
  ));
}

void startPythonProgram() async {
  debugPrint("startPythonProgram()");
  WidgetsFlutterBinding.ensureInitialized();
  var appPath =
      await extractZipArchive("assets/python-app/app.zip", "python-app");
  debugPrint("Python app path: $appPath");
  Directory.current = appPath;

  var pythonEnginePlugin = PythonEngine();
  pythonEnginePlugin.runPython(p.join(appPath, "main.py"),
      environmentVariables: {
        "FLET_PLATFORM": "iOS",
        "FLET_SERVER_UDS_PATH": "flet.sock"
      });
}
