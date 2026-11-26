@TestOn('browser')
library;

import 'package:flet/src/services/file_storage_backend_web.dart';
import 'package:flutter_test/flutter_test.dart';

import 'file_storage_backend_contract.dart';

/// The OPFS backend in a real browser: `flutter test --platform chrome`.
void main() {
  fileStorageBackendContract(createFileStorageBackend);
}
