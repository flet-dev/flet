import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flet_ads/flet_ads.dart' as flet_ads;
// --FAT_CLIENT_START--
import 'package:flet_audio/flet_audio.dart' as flet_audio;
// --FAT_CLIENT_END--
import 'package:flet_audio_recorder/flet_audio_recorder.dart'
    as flet_audio_recorder;
import "package:flet_flashlight/flet_flashlight.dart" as flet_flashlight;
import 'package:flet_geolocator/flet_geolocator.dart' as flet_geolocator;
import 'package:flet_lottie/flet_lottie.dart' as flet_lottie;
import 'package:flet_map/flet_map.dart' as flet_map;
import 'package:flet_permission_handler/flet_permission_handler.dart'
    as flet_permission_handler;
import 'package:flet_rive/flet_rive.dart' as flet_rive;
// --FAT_CLIENT_START--
import 'package:flet_video/flet_video.dart' as flet_video;
// --FAT_CLIENT_END--
import 'package:flet_webview/flet_webview.dart' as flet_webview;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:url_strategy/url_strategy.dart';

const bool isProduction = bool.fromEnvironment('dart.vm.product');

void main([List<String>? args]) async {
  if (isProduction) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  }

  await setupDesktop();

  WidgetsFlutterBinding.ensureInitialized();

  // --FAT_CLIENT_START--
  flet_audio.ensureInitialized();
  flet_video.ensureInitialized();
  // --FAT_CLIENT_END--
  flet_audio_recorder.ensureInitialized();
  flet_geolocator.ensureInitialized();
  flet_permission_handler.ensureInitialized();
  flet_lottie.ensureInitialized();
  flet_map.ensureInitialized();
  flet_ads.ensureInitialized();
  flet_rive.ensureInitialized();
  flet_webview.ensureInitialized();
  flet_flashlight.ensureInitialized();

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

  runApp(FletApp(
    title: 'Flet',
    pageUrl: pageUrl,
    assetsDir: assetsDir,
    errorsHandler: errorsHandler,
    showAppStartupScreen: true,
    createControlFactories: [
// --FAT_CLIENT_START--
      flet_audio.createControl,
      flet_video.createControl,
// --FAT_CLIENT_END--
      flet_audio_recorder.createControl,
      flet_geolocator.createControl,
      flet_permission_handler.createControl,
      flet_lottie.createControl,
      flet_map.createControl,
      flet_ads.createControl,
      flet_rive.createControl,
      flet_webview.createControl,
      flet_flashlight.createControl,
    ],
  ));
}
