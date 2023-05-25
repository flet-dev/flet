import 'dart:io';

import 'package:archive/archive.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

Future<String> extractZipArchive(String assetPath, String destDirName) async {
  final documentsDir = await getApplicationDocumentsDirectory();
  final destDir = Directory(p.join(documentsDir.path, destDirName));

  // re-create dir
  if (await destDir.exists()) {
    if (kDebugMode) {
      // always re-create in debug mode
      await destDir.delete(recursive: true);
    } else {
      debugPrint("App archived already unpacked");
      return destDir.path;
    }
  }
  await destDir.create();

  // unpack from asset
  debugPrint("Start unpacking app archive");
  final bytes = await rootBundle.load(assetPath);
  final archive = ZipDecoder().decodeBytes(bytes.buffer.asUint8List());
  for (final file in archive) {
    final filename = p.join(destDir.path, file.name);
    if (file.isFile) {
      final outFile = await File(filename).create(recursive: true);
      await outFile.writeAsBytes(file.content);
    } else {
      await Directory(filename).create(recursive: true);
    }
  }
  debugPrint("Finished unpacking app archive");
  return destDir.path;
}
