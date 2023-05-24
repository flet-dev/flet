import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:python_engine/python_engine.dart';

import 'utils.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  var tmpDir = await getTemporaryDirectory();
  debugPrint("TEMP DIR IN DART: ${tmpDir.path}");

  var appPath =
      await extractZipArchive("assets/python-app/app.zip", "python-app");
  debugPrint("PYTHON APP PATH: $appPath");
  Directory.current = appPath;

  var pythonEnginePlugin = PythonEngine();
  pythonEnginePlugin.runPython(appPath, "main");

  await setupDesktop();
  runApp(const FletApp(
    pageUrl: "http://Feodors-MacBook-Pro.local:8550/",
    assetsDir: "",
  ));
}
