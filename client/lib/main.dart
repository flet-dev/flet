import 'dart:io';

import 'package:flet_view/utils/desktop.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:url_strategy/url_strategy.dart';

import '../utils/platform_utils_non_web.dart'
    if (dart.library.js) "../utils/platform_utils_web.dart";
import '../utils/session_store_non_web.dart'
    if (dart.library.js) "../utils/session_store_web.dart";
import 'flet_app.dart';

const bool isProduction = bool.fromEnvironment('dart.vm.product');

void main([List<String>? args]) async {
  if (isProduction) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  }

  await setupDesktop();

  var pageUrl = Uri.base.toString();
  //debugPrint("Uri.base: ${Uri.base}");

  if (kDebugMode) {
    pageUrl = "http://localhost:8550";
  }

  if (kIsWeb) {
    debugPrint("Flet View is running in Web mode");
    var routeUrlStrategy = getRouteUrlStrategy();
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
  }

  debugPrint("Page URL: $pageUrl");

  String sessionId = SessionStore.get("sessionId") ?? "";
  runApp(FletApp(title: 'Flet', pageUrl: pageUrl, sessionId: sessionId));
}
