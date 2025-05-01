import 'package:flutter/cupertino.dart';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart';

import '../flet_service.dart';
import '../utils/platform.dart';

class StoragePaths extends FletService {
  StoragePaths({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("StoragePaths(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("StoragePaths.$name($args)");
    // path_provider doesn't support web
    if (!isWebPlatform()) {
      switch (name) {
        case "get_application_cache_directory":
          return (await getApplicationCacheDirectory()).path;
        case "get_application_documents_directory":
          return (await getApplicationDocumentsDirectory()).path;
        case "get_application_support_directory":
          return (await getApplicationSupportDirectory()).path;
        case "get_downloads_directory":
          return (await getDownloadsDirectory())?.path;
        case "get_external_cache_directories":
          return isAndroidMobile()
              ? (await getExternalCacheDirectories())
                  ?.map((e) => e.path)
                  .toList()
              : null;
        case "get_external_storage_directories":
          return isAndroidMobile()
              ? (await getExternalStorageDirectories())
                  ?.map((e) => e.path)
                  .toList()
              : null;
        case "get_library_directory":
          return isApplePlatform() ? (await getLibraryDirectory()).path : null;
        case "get_external_cache_directory":
          return isAndroidMobile()
              ? (await getExternalStorageDirectory())?.path
              : null;
        case "get_temporary_directory":
          return (await getTemporaryDirectory()).path;
        case "get_console_log_filename":
          return path.join(
              (await getApplicationCacheDirectory()).path, "console.log");
        default:
          throw Exception("Unknown StoragePaths method: $name");
      }
    }
  }

  @override
  void dispose() {
    debugPrint("StoragePaths(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
