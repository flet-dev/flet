import 'package:flutter/widgets.dart';

import '../flet_service.dart';
import 'file_storage_backend_web.dart'
    if (dart.library.io) 'file_storage_backend_io.dart';
import 'file_storage_space.dart';

/// `ft.FileStorage`: files an app keeps between runs, in a folder of its own.
///
/// The host does the file work - in OPFS on web, in the app support
/// directory elsewhere - so an app embedded with `FletApp` gets only its own
/// folder (named from its [FletBackend.storagePrefix]) and its own quota
/// ([FletBackend.fileStorageQuota]), whatever it asks for. Locks it holds are
/// released when it goes away.
class FileStorageService extends FletService {
  FileStorageService({required super.control});

  late final FileStorageSpace _space = FileStorageSpace(
      createFileStorageBackend(), control.backend.storagePrefix,
      quota: control.backend.fileStorageQuota);

  @override
  void init() {
    super.init();
    debugPrint("FileStorageService(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) =>
      _space.invoke(name, args);

  @override
  void dispose() {
    debugPrint("FileStorageService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _space.releaseLocks();
    super.dispose();
  }
}
