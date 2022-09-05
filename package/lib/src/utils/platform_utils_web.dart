import 'dart:html';
import 'dart:math';

bool isProgressiveWebApp() {
  return window.matchMedia('(display-mode: standalone)').matches ||
      window.matchMedia('(display-mode: fullscreen)').matches ||
      window.matchMedia('(display-mode: minimal-ui)').matches;
}

String getFletRouteUrlStrategy() {
  var meta =
      document.head?.querySelector("meta[name='flet-route-url-strategy']");
  return meta != null ? meta.attributes["content"]! : "";
}

void openPopupBrowserWindow(
    String url, String windowName, int minWidth, int minHeight) {
  int screenWidth = window.screen!.width!;
  int screenHeight = window.screen!.height!;
  final dualScreenLeft = window.screenLeft! < 0 ? -screenWidth : 0;
  var toolbarHeight = window.outerHeight - window.innerHeight!;
  var width = max(minWidth, screenWidth - 300);
  var height = max(minHeight, screenHeight - 300);
  var left = (screenWidth / 2) - (width / 2) + dualScreenLeft;
  var top = (screenHeight / 2) - (height / 2) - toolbarHeight;
  window.open(url, windowName,
      "top=$top,left=$left,width=$width,height=$height,scrollbars=yes");
}
