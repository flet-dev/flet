import 'strings.dart';

String getWebPageName(Uri uri) {
  var urlPath = uri.path.trimSymbol("/");
  if (urlPath != "") {
    var pathParts = urlPath.split("/");
    if (pathParts.length > 1) {
      urlPath = pathParts.sublist(0, 2).join("/");
    }
  }
  return urlPath;
}

/// Derives the WebSocket endpoint path of a Flet app from its own URL path:
/// `""` → `"ws"`, `"/sub1"` → `"sub1/ws"`.
///
/// Mirrors the io implementation of `getWebsocketEndpointPath`. Used for
/// embedded apps ([FletApp]) on web, whose endpoint cannot come from the host
/// document's configuration: that configuration describes the host app and is
/// the same for every app embedded on the page.
String getWebSocketEndpointPathFromUriPath(String uriPath) {
  var pagePath = uriPath.trimSymbol("/");
  return pagePath == "" ? "ws" : "$pagePath/ws";
}

Uri getAssetUri(Uri pageUri, String assetPath) {
  return Uri(
      scheme: pageUri.scheme,
      host: pageUri.host,
      port: pageUri.port,
      pathSegments: [...pageUri.pathSegments, ...assetPath.split("/")]);
}

Uri getBaseUri(Uri pageUri) {
  return Uri(scheme: pageUri.scheme, host: pageUri.host, port: pageUri.port);
}

bool isLocalhost(Uri uri) {
  return uri.host == "localhost" || uri.host == "127.0.0.1";
}

bool isUdsPath(Uri address) {
  return !address.hasScheme;
}

bool isUrl(String value) {
  final urlPattern = RegExp(r'^(https?:\/\/|www\.)');
  return urlPattern.hasMatch(value);
}
