import 'uri.dart';

bool isProgressiveWebApp() {
  return false;
}

String getWebsocketEndpointPath(String uriPath) {
  return getWebsocketEndpointPathFromUriPath(uriPath);
}

String getFletRouteUrlStrategy() {
  return "";
}

String getAssetsDir() {
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

bool isGestureGatedDialogBlocked() {
  return false;
}
