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
  return trim(getHeadMetaContent("flet-websocket-endpoint-path") ?? "ws", "/");
}

String getFletRouteUrlStrategy() {
  return getHeadMetaContent("flet-route-url-strategy") ?? "";
}

bool isFletWebPyodideMode() {
  return getHeadMetaContent("flet-web-pyodide")?.toLowerCase() == "true";
}

bool isMultiView() {
  return fletConfig?.multiView == true;
}

String? getHeadMetaContent(String metaName) {
  var meta = web.document.head?.querySelector("meta[name='$metaName']");
  return meta?.attributes.getNamedItem("content")?.value;
}

Map<dynamic, dynamic> getViewInitialData(int viewId) {
  return (views.getInitialData(viewId)?.dartify() ?? {}) as Map;
}

@JS('fletConfig')
@staticInterop
class FletConfig {}

extension FletConfigExtension on FletConfig {
  external String get webRenderer;
  external bool get useColorEmoji;
  external bool get multiView;
}

@JS()
external FletConfig? get fletConfig;

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
