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

Uri getAssetUri(Uri pageUri, String assetPath) {
  return Uri(
      scheme: pageUri.scheme,
      host: pageUri.host,
      port: pageUri.port,
      path: pageUri.path +
          (assetPath.startsWith("/") ? assetPath.substring(1) : assetPath));
}

Uri getBaseUri(Uri pageUri) {
  return Uri(scheme: pageUri.scheme, host: pageUri.host, port: pageUri.port);
}

bool isLocalhost(Uri uri) {
  return uri.host == "localhost" || uri.host == "127.0.0.1";
}

bool isUdsPath(String address) {
  var uri = Uri.tryParse(address);
  return uri == null || !uri.hasScheme;
}
