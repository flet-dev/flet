import 'package:flet/flet.dart';
import 'package:flet_ads/flet_ads.dart' as flet_ads;
// --FAT_CLIENT_START--
import 'package:flet_audio/flet_audio.dart' as flet_audio;
// --FAT_CLIENT_END--
import 'package:flet_audio_recorder/flet_audio_recorder.dart'
    as flet_audio_recorder;
import 'package:flet_charts/flet_charts.dart' as flet_charts;
import 'package:flet_datatable2/flet_datatable2.dart' as flet_datatable2;
import "package:flet_flashlight/flet_flashlight.dart" as flet_flashlight;
import 'package:flet_geolocator/flet_geolocator.dart' as flet_geolocator;
import 'package:flet_lottie/flet_lottie.dart' as flet_lottie;
import 'package:flet_map/flet_map.dart' as flet_map;
import 'package:flet_permission_handler/flet_permission_handler.dart'
    as flet_permission_handler;
import 'package:flet_secure_storage/flet_secure_storage.dart'
    as flet_secure_storage;
// --FAT_CLIENT_START--
// --RIVE_IMPORT_START--
import 'package:flet_rive/flet_rive.dart' as flet_rive;
// --RIVE_IMPORT_END--
import 'package:flet_video/flet_video.dart' as flet_video;
// --FAT_CLIENT_END--
import 'package:flet_webview/flet_webview.dart' as flet_webview;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_web_plugins/url_strategy.dart';

const bool isProduction = bool.fromEnvironment('dart.vm.product');

Tester? tester;

void main([List<String>? args]) async {
  if (isProduction) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  }

  await setupDesktop();

  WidgetsFlutterBinding.ensureInitialized();
  List<FletExtension> extensions = [
    flet_audio_recorder.Extension(),
    flet_geolocator.Extension(),
    flet_permission_handler.Extension(),
    flet_lottie.Extension(),
    flet_map.Extension(),
    flet_ads.Extension(),
    flet_webview.Extension(),
    flet_flashlight.Extension(),
    flet_datatable2.Extension(),
    flet_charts.Extension(),
    flet_secure_storage.Extension(),
    // --FAT_CLIENT_START--
    // --RIVE_EXTENSION_START--
    flet_rive.Extension(),
    // --RIVE_EXTENSION_END--
    flet_audio.Extension(),
    flet_video.Extension(),
    // --FAT_CLIENT_END--
  ];

  // initialize extensions
  for (var extension in extensions) {
    extension.ensureInitialized();
  }

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
      usePathUrlStrategy();
    }
  } else {
    if (args!.isNotEmpty) {
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
    } else if (!kDebugMode && (Platform.isWindows || Platform.isMacOS || Platform.isLinux)) {
      throw Exception('In desktop mode Flet app URL must be provided as a first argument.');
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

  var app = FletApp(
    title: 'Flet',
    pageUrl: pageUrl,
    assetsDir: assetsDir,
    errorsHandler: errorsHandler,
    showAppStartupScreen: true,
    appStartupScreenMessage: "Working...",
    appErrorMessage: "The application encountered an error: {message}",
    extensions: extensions,
    multiView: isMultiView(),
    tester: tester,
  );

  if (app.multiView) {
    debugPrint("Flet Web Multi-View mode");
    runWidget(app);
  } else {
    runApp(app);
  }
}
