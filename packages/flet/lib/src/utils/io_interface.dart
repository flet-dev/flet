import 'dart:io';
import 'dart:typed_data';

import 'desktop.dart' as desktop show setWindowFullScreen;

Future<ByteData> fetchFontFromFile(String path) async {
  File file = File(path);
  Uint8List bytes = await file.readAsBytes();
  return ByteData.view(bytes.buffer);
}

Future setWindowFullScreen(bool fullScreen) async {
  await desktop.setWindowFullScreen(fullScreen);
}
