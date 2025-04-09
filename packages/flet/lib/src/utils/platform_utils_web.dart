// ignore: avoid_web_libraries_in_flutter
import 'package:web/web.dart' as web;

import 'strings.dart';

bool isProgressiveWebApp() {
  return web.window.matchMedia('(display-mode: standalone)').matches ||
      web.window.matchMedia('(display-mode: fullscreen)').matches ||
      web.window.matchMedia('(display-mode: minimal-ui)').matches;
}

String getWebsocketEndpointPath(String uriPath) {
  var meta = web.document.head
      ?.querySelector("meta[name='flet-websocket-endpoint-path']");
  return trim(meta?.attributes.getNamedItem("content")?.value ?? "ws", "/");
}

String getFletRouteUrlStrategy() {
  var meta =
      web.document.head?.querySelector("meta[name='flet-route-url-strategy']");
  if (meta != null) {
    var metaAttr = meta.attributes.getNamedItem("content");
    return (metaAttr != null) ? metaAttr.value : "";
  }
  return "";
}

bool isFletWebPyodideMode() {
  var meta = web.document.head?.querySelector("meta[name='flet-web-pyodide']");
  return meta != null
      ? meta.attributes.getNamedItem("content")?.value.toLowerCase() == "true"
      : false;
}

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
