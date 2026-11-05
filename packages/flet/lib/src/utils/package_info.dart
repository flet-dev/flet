import 'package:package_info_plus/package_info_plus.dart';

/// Returns the running application's package information as a Map.
Future<Map<String, dynamic>> getPackageInfo() async {
  final info = await PackageInfo.fromPlatform();
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
