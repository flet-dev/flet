@TestOn('vm')
library;

import 'dart:io';
import 'dart:typed_data';

import 'package:flet/src/services/file_storage_backend_io.dart';
import 'package:flutter_test/flutter_test.dart';

import 'file_storage_backend_contract.dart';

void main() {
  final base = Directory.systemTemp.createTempSync("flet_file_storage_");
  tearDownAll(() => base.deleteSync(recursive: true));

  fileStorageBackendContract(() => createFolderFileStorageBackend(base.path));

  test("leaves no temporary files behind", () async {
    final b = createFolderFileStorageBackend(base.path);
    await b.write(["flet", "tmp", "a.bin"], Uint8List.fromList("abc".codeUnits));
    final names = base
        .listSync(recursive: true)
        .whereType<File>()
        .map((f) => f.path.split(Platform.pathSeparator).last);
    expect(names, ["a.bin"]);
  });
}
