import 'dart:io';

import 'package:archive/archive.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

Future<String> extractZipArchive(String assetPath, String destDirName) async {
  final documentsDir = await getApplicationDocumentsDirectory();
  final tempDir =
      await Directory(p.join(documentsDir.path, destDirName)).create();
  final bytes = await rootBundle.load(assetPath);
  final archive = ZipDecoder().decodeBytes(bytes.buffer.asUint8List());
  for (final file in archive) {
    final filename = p.join(tempDir.path, file.name);
    if (file.isFile) {
      final outFile = await File(filename).create(recursive: true);
      await outFile.writeAsBytes(file.content);
    } else {
      await Directory(filename).create(recursive: true);
    }
  }
  return tempDir.path;
}
