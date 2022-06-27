import 'dart:io';

import 'package:flet_view/models/window_media_data.dart';
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

Future<Size> getWindowSize() {
  if (isDesktop()) {
    return windowManager.getSize();
  } else {
    return Future.value(const Size(0, 0));
  }
}

Future<WindowMediaData> getWindowMediaData() async {
  var m = WindowMediaData();
  if (isDesktop()) {
    m.isMaximized = await windowManager.isMaximized();
    m.isMinimized = await windowManager.isMinimized();
    m.isMinimizable = await windowManager.isMinimizable();
    m.isFullScreen = await windowManager.isFullScreen();
    m.isResizable = await windowManager.isResizable();
    m.isMovable = await windowManager.isClosable();
    m.isAlwaysOnTop = await windowManager.isAlwaysOnTop();
    m.isFocused = await windowManager.isFocused();
    m.isTitleBarHidden = false;
    var size = await windowManager.getSize();
    m.width = size.width;
    m.height = size.height;
    var pos = await windowManager.getPosition();
    m.left = pos.dx;
    m.top = pos.dy;
    m.opacity = await windowManager.getOpacity();
    return m;
  } else {
    return Future.value(m);
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
