import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

const double windowWidth = 480;
const double windowHeight = 854;

void setWindowTitle(String title) {
  if (isDesktop()) {
    windowManager.setTitle(title);
  }
}

void setWindowSize(double? width, double? height) {
  if (isDesktop()) {
    windowManager.getSize().then((currentSize) {
      windowManager.setSize(
          Size(width ?? currentSize.width, height ?? currentSize.height),
          animate: true);
    });
  }
}

Future<Size> getWindowSize(Size defaultSize) {
  if (isDesktop()) {
    return windowManager.getSize();
  } else {
    return Future.value(defaultSize);
  }
}

Future setupDesktop() async {
  if (isDesktop()) {
    WidgetsFlutterBinding.ensureInitialized();
    // Must add this line.
    await windowManager.ensureInitialized();
  }
}

bool isDesktop() {
  return !kIsWeb &&
      (Platform.isWindows || Platform.isLinux || Platform.isMacOS);
}
