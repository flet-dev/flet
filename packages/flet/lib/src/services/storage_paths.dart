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
    updateValues();
  }

  @override
  void update() {
    debugPrint("StoragePaths(${control.id}).update: ${control.properties}");
    updateValues();
  }

  void updateValues() async {
    // path_provider doesn't support web
    if (!isWebPlatform()) {
      var applicationCacheDirectory =
          (await getApplicationCacheDirectory()).path;
      var consoleLogFilename =
          path.join(applicationCacheDirectory, "console.log");
      var applicationDocumentsDirectory =
          (await getApplicationDocumentsDirectory()).path;
      var applicationSupportDirectory =
          (await getApplicationSupportDirectory()).path;
      var downloadsDirectory = (await getDownloadsDirectory())?.path;
      var externalCacheDirectories = isAndroidMobile()
          ? (await getExternalCacheDirectories())?.map((e) => e.path).toList()
          : null;
      var externalStorageDirectories = isAndroidMobile()
          ? (await getExternalStorageDirectories())?.map((e) => e.path).toList()
          : null;
      var libraryDirectory =
          isApplePlatform() ? (await getLibraryDirectory()).path : null;
      var externalCacheDirectory = isAndroidMobile()
          ? (await getExternalStorageDirectory())?.path
          : null;
      var temporaryDirectory = (await getTemporaryDirectory()).path;

      control.updateProperties({
        "application_cache_directory": applicationCacheDirectory,
        "application_documents_directory": applicationDocumentsDirectory,
        "application_support_directory": applicationSupportDirectory,
        "downloads_directory": downloadsDirectory,
        "external_cache_directories": externalCacheDirectories,
        "external_storage_directories": externalStorageDirectories,
        "library_directory": libraryDirectory,
        "external_cache_directory": externalCacheDirectory,
        "temporary_directory": temporaryDirectory,
        "console_log_filename": consoleLogFilename,
      });
    }
  }
}
