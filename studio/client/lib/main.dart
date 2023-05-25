import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
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
  pythonEnginePlugin.runPython(appPath, "main");
}
