import 'package:flutter/foundation.dart';
import 'package:package_info_plus/package_info_plus.dart';

import 'platform_utils_web.dart'
    if (dart.library.io) "platform_utils_non_web.dart";

/// Returns the running application's package information as a Map.
///
/// On the web, the plugin reads `version.json` from the app's base URL, given
/// as an absolute URL: from a path-only `assetBase` such as `"/"`, the plugin
/// can't build one and throws ("Cannot use origin without a scheme"). A web app
/// without a `version.json` gets empty values.
Future<Map<String, dynamic>> getPackageInfo() async {
  PackageInfo info;
  try {
    info = await PackageInfo.fromPlatform(baseUrl: getWebAppBaseUrl());
  } catch (_) {
    if (!kIsWeb) rethrow;
    info = PackageInfo(appName: "", packageName: "", version: "", buildNumber: "");
  }
  return {
    "app_name": info.appName,
    "package_name": info.packageName,
    "version": info.version,
    "build_number": info.buildNumber,
    "build_signature": info.buildSignature,
    "installer_store": info.installerStore,
    "install_time": info.installTime,
    "update_time": info.updateTime,
  };
}
