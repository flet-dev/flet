// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;

import 'strings.dart';

bool isProgressiveWebApp() {
  return html.window.matchMedia('(display-mode: standalone)').matches ||
      html.window.matchMedia('(display-mode: fullscreen)').matches ||
      html.window.matchMedia('(display-mode: minimal-ui)').matches;
}

String getWebsocketEndpointPath(String uriPath) {
  var meta = html.document.head
      ?.querySelector("meta[name='flet-websocket-endpoint-path']");
  return trim(meta?.attributes["content"] ?? "ws", "/");
}

String getFletRouteUrlStrategy() {
  var meta =
      html.document.head?.querySelector("meta[name='flet-route-url-strategy']");
  return meta != null ? meta.attributes["content"]! : "";
}

bool isFletWebPyodideMode() {
  var meta = html.document.head?.querySelector("meta[name='flet-web-pyodide']");
  return meta != null
      ? meta.attributes["content"]?.toLowerCase() == "true"
      : false;
}

void openPopupBrowserWindow(
    String url, String windowName, int width, int height) {
  int screenWidth = html.window.screen!.width!;
  int screenHeight = html.window.screen!.height!;
  final dualScreenLeft = html.window.screenLeft! < 0 ? -screenWidth : 0;
  var toolbarHeight = html.window.outerHeight - html.window.innerHeight!;
  //var width = max(minWidth, screenWidth - 300);
  //var height = max(minHeight, screenHeight - 300);
  var left = (screenWidth / 2) - (width / 2) + dualScreenLeft;
  var top = (screenHeight / 2) - (height / 2) - toolbarHeight;
  html.window.open(url, windowName,
      "top=$top,left=$left,width=$width,height=$height,scrollbars=yes");
}
