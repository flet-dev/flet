import 'strings.dart';

bool isProgressiveWebApp() {
  return false;
}

String getWebsocketEndpointPath(String uriPath) {
  var pagePath = uriPath.trimSymbol("/");
  if (pagePath != "") {
    pagePath = "$pagePath/";
  }
  return "${pagePath}ws";
}

String getFletRouteUrlStrategy() {
  return "";
}

bool isPyodideMode() {
  return false;
}

bool isMultiView() {
  return false;
}

Map<dynamic, dynamic> getViewInitialData(int viewId) {
  return {};
}

void openPopupBrowserWindow(
    String url, String windowName, int minWidth, int minHeight) {}
