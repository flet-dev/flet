import 'dart:typed_data';
import 'dart:io';

Future<ByteData> fetchFontFromFile(String path) async {
  File file = File(path);
  Uint8List bytes = await file.readAsBytes();
  return ByteData.view(bytes.buffer);
}
