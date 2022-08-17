import 'dart:io';

import 'package:flet_view/actions.dart';
import 'package:flet_view/utils/desktop.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';
import 'package:url_strategy/url_strategy.dart';

import '../utils/platform_utils_non_web.dart'
    if (dart.library.js) "../utils/platform_utils_web.dart";
import '../utils/session_store_non_web.dart'
    if (dart.library.js) "../utils/session_store_web.dart";
import 'controls/create_control.dart';
import 'flet_app.dart';
import 'models/app_state.dart';
import 'models/page_view_model.dart';
import 'reducers.dart';
import 'web_socket_client.dart';

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

  //final store = Store<AppState>(appReducer, initialState: AppState.initial());
  //ws.store = store;

  String sessionId = SessionStore.get("sessionId") ?? "";

  // connect to a page
  //store.dispatch(PageLoadAction(pageUri, sessionId));

  runApp(FletApp(title: 'Flet', pageUrl: pageUrl, sessionId: sessionId));
}
