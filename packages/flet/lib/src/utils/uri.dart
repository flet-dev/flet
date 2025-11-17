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
