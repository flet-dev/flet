// ignore: avoid_web_libraries_in_flutter
import 'dart:js_interop';
import 'dart:ui_web';

import 'package:web/web.dart' as web;

import 'strings.dart';

bool isProgressiveWebApp() {
  return web.window.matchMedia('(display-mode: standalone)').matches ||
      web.window.matchMedia('(display-mode: fullscreen)').matches ||
      web.window.matchMedia('(display-mode: minimal-ui)').matches;
}

String getWebsocketEndpointPath(String uriPath) {
  return trim(fletJS?.webSocketEndpoint ?? "ws", "/");
}

String getFletRouteUrlStrategy() {
  return fletJS?.routeUrlStrategy ?? "";
}

bool isFletWebPyodideMode() {
  return fletJS?.pyodide == true;
}

bool isMultiView() {
  return fletJS?.multiView == true;
}

String? getHeadMetaContent(String metaName) {
  var meta = web.document.head?.querySelector("meta[name='$metaName']");
  return meta?.attributes.getNamedItem("content")?.value;
}

Map<dynamic, dynamic> getViewInitialData(int viewId) {
  return (views.getInitialData(viewId)?.dartify() ?? {}) as Map;
}

@JS()
@anonymous
@staticInterop
class FletJS {
  external factory FletJS();
}

extension FletJSExtension on FletJS {
  external bool get pyodide;
  external bool get multiView;
  external bool get noCdn;
  external String get webSocketEndpoint;
  external String get routeUrlStrategy;
  external String get canvasKitBaseUrl;
  external String get pyodideUrl;
  external String get webRenderer;
  external bool get appPackageUrl;
}

@JS('flet')
external FletJS? get fletJS;

void openPopupBrowserWindow(
    String url, String windowName, int width, int height) {
  int screenWidth = web.window.screen.width;
  int screenHeight = web.window.screen.height;
  final dualScreenLeft = web.window.screenLeft < 0 ? -screenWidth : 0;
  var toolbarHeight = web.window.outerHeight - web.window.innerHeight;
  //var width = max(minWidth, screenWidth - 300);
  //var height = max(minHeight, screenHeight - 300);
  var left = (screenWidth / 2) - (width / 2) + dualScreenLeft;
  var top = (screenHeight / 2) - (height / 2) - toolbarHeight;
  web.window.open(url, windowName,
      "top=$top,left=$left,width=$width,height=$height,scrollbars=yes");
}
