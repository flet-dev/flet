import 'dart:html';

bool isProgressiveWebApp() {
  return window.matchMedia('(display-mode: standalone)').matches ||
      window.matchMedia('(display-mode: fullscreen)').matches ||
      window.matchMedia('(display-mode: minimal-ui)').matches;
}

String getRouteUrlStrategy() {
  var meta =
      document.head?.querySelector("meta[name='flet-route-url-strategy']");
  return meta != null ? meta.attributes["content"]! : "";
}
