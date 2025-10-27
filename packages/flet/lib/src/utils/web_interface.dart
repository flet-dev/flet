import 'dart:typed_data';

import 'package:web/web.dart' as web show window;

Future<ByteData> fetchFontFromFile(String path) async {
  throw UnimplementedError();
}

Future setWindowFullScreen(bool fullScreen) async {
  if (fullScreen) {
    web.window.document.documentElement?.requestFullscreen();
  } else {
    web.window.document.exitFullscreen();
  }
}
