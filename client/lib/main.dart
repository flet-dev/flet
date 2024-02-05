import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:url_strategy/url_strategy.dart';

const bool isProduction = bool.fromEnvironment('dart.vm.product');

void main([List<String>? args]) async {
  if (isProduction) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  }

  await setupDesktop();

  var pageUrl = Uri.base.toString();
  var assetsDir = "";
  //debugPrint("Uri.base: ${Uri.base}");

  if (kDebugMode) {
    pageUrl = "http://localhost:8550";
  }

  if (kIsWeb) {
    debugPrint("Flet View is running in Web mode");
    var routeUrlStrategy = getFletRouteUrlStrategy();
    debugPrint("URL Strategy: $routeUrlStrategy");
    if (routeUrlStrategy == "path") {
      setPathUrlStrategy();
    }
  } else if ((Platform.isWindows || Platform.isMacOS || Platform.isLinux) &&
      !kDebugMode) {
    debugPrint("Flet View is running in Desktop mode");
    // first argument must be
    if (args!.isEmpty) {
      throw Exception('Page URL must be provided as a first argument.');
    }
    pageUrl = args[0];
    if (args.length > 1) {
      var pidFilePath = args[1];
      debugPrint("Args contain a path to PID file: $pidFilePath}");
      var pidFile = await File(pidFilePath).create();
      await pidFile.writeAsString("$pid");
    }
    if (args.length > 2) {
      assetsDir = args[2];
      debugPrint("Args contain a path assets directory: $assetsDir}");
    }
  }

  debugPrint("Page URL: $pageUrl");

  FletAppErrorsHandler errorsHandler = FletAppErrorsHandler();

  if (!kDebugMode) {
    FlutterError.onError = (details) {
      errorsHandler.onError(details.exceptionAsString());
    };

    PlatformDispatcher.instance.onError = (error, stack) {
      errorsHandler.onError(error.toString());
      return true;
    };
  }

  WidgetsFlutterBinding.ensureInitialized();
  MediaKit.ensureInitialized();

  runApp(FletApp(
    title: 'Flet',
    pageUrl: pageUrl,
    assetsDir: assetsDir,
    errorsHandler: errorsHandler,
  ));
}
