import 'package:flutter/cupertino.dart';
import 'package:path_provider/path_provider.dart';

import '../flet_service.dart';
import '../utils/platform.dart';

class PathProviderService extends FletService {
  PathProviderService({required super.control, required super.backend});

  @override
  void init() {
    super.init();
    debugPrint(
        "PathProviderService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
    updateValues();
  }

  @override
  void update() {
    debugPrint(
        "PathProviderService(${control.id}).update: ${control.properties}");
    updateValues();
  }

  void updateValues() async {
    var applicationCacheDirectory = (await getApplicationCacheDirectory()).path;
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
    var externalCacheDirectory =
        isAndroidMobile() ? (await getExternalStorageDirectory())?.path : null;
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
    });
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("PathProviderService.$name($args)");
    switch (name) {
      default:
        throw Exception("Unknown PathProviderService method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("PathProviderService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
