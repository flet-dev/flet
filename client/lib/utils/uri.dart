import 'strings.dart';

String getWebPageName(Uri uri) {
  return trim(uri.path, "/");
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
