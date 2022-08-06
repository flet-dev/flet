import 'strings.dart';

String getWebPageName(Uri uri) {
  var urlPath = trim(uri.path, "/");
  if (urlPath != "") {
    var pathParts = urlPath.split("/");
    if (pathParts.length > 1) {
      urlPath = pathParts.sublist(0, 2).join("/");
    }
  }
  return urlPath;
}

String getWebSocketEndpoint(Uri uri) {
  final wsScheme = uri.scheme == "https" ? "wss" : "ws";
  return "$wsScheme://${uri.authority}/ws";
}

Uri getAssetUri(Uri pageUri, String assetPath) {
  return Uri(
      scheme: pageUri.scheme,
      host: pageUri.host,
      port: pageUri.port,
      path: assetPath);
}

Uri getBaseUri(Uri pageUri) {
  return Uri(scheme: pageUri.scheme, host: pageUri.host, port: pageUri.port);
}
