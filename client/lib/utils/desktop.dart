import 'dart:io';

import 'package:flet_view/models/window_media_data.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

const double windowWidth = 480;
const double windowHeight = 854;

Future setWindowTitle(String title) async {
  if (isDesktop()) {
    await windowManager.setTitle(title);
  }
}

Future setWindowSize(double? width, double? height) async {
  if (isDesktop()) {
    var currentSize = await windowManager.getSize();
    await windowManager.setSize(
        Size(width ?? currentSize.width, height ?? currentSize.height),
        animate: !Platform.isMacOS);
  }
}

Future setWindowMinSize(double? minWidth, double? minHeight) async {
  if (isDesktop()) {
    await windowManager.setMinimumSize(Size(minWidth ?? 0, minHeight ?? 0));
  }
}

Future setWindowMaxSize(double? maxWidth, double? maxHeight) async {
  if (isDesktop()) {
    await windowManager.setMaximumSize(Size(maxWidth ?? -1, maxHeight ?? -1));
  }
}

Future setWindowPosition(double? top, double? left) async {
  if (isDesktop()) {
    var currentPos = await windowManager.getPosition();
    await windowManager.setPosition(
        Offset(left ?? currentPos.dx, top ?? currentPos.dy),
        animate: true);
  }
}

Future setWindowOpacity(double opacity) async {
  if (isDesktop()) {
    await windowManager.setOpacity(opacity);
  }
}

Future setWindowMinimizability(bool minimizable) async {
  if (isDesktop()) {
    await windowManager.setMinimizable(minimizable);
  }
}

Future setWindowResizability(bool resizable) async {
  if (isDesktop()) {
    await windowManager.setResizable(resizable);
  }
}

Future setWindowMovability(bool movable) async {
  if (isDesktop()) {
    await windowManager.setMovable(movable);
  }
}

Future setWindowFullScreen(bool fullScreen) async {
  if (isDesktop()) {
    await windowManager.setFullScreen(fullScreen);
  }
}

Future setWindowAlwaysOnTop(bool alwaysOnTop) async {
  if (isDesktop()) {
    await windowManager.setAlwaysOnTop(alwaysOnTop);
  }
}

Future setWindowPreventClose(bool preventClose) async {
  if (isDesktop()) {
    await windowManager.setPreventClose(preventClose);
  }
}

Future minimizeWindow() async {
  if (isDesktop() && !await windowManager.isMinimized()) {
    await windowManager.minimize();
  }
}

Future restoreWindow() async {
  if (isDesktop() && await windowManager.isMinimized()) {
    await windowManager.restore();
  }
}

Future maximizeWindow() async {
  if (isDesktop() && !await windowManager.isMaximized()) {
    await windowManager.maximize();
  }
}

Future unmaximizeWindow() async {
  if (isDesktop() && await windowManager.isMaximized()) {
    await windowManager.unmaximize();
  }
}

Future focusWindow() async {
  if (isDesktop() &&
      (Platform.isWindows || Platform.isMacOS) &&
      !await windowManager.isFocused()) {
    await windowManager.focus();
  }
}

Future blurWindow() async {
  if (isDesktop() &&
      (Platform.isWindows || Platform.isMacOS) &&
      await windowManager.isFocused()) {
    await windowManager.blur();
  }
}

Future destroyWindow() async {
  if (isDesktop()) {
    await windowManager.destroy();
  }
}

Future centerWindow() async {
  if (isDesktop()) {
    await windowManager.center();
  }
}

Future isFocused() async {
  if (isDesktop() && (Platform.isWindows || Platform.isMacOS)) {
    return await windowManager.isFocused();
  } else {
    return false;
  }
}

Future<WindowMediaData> getWindowMediaData() async {
  var m = WindowMediaData();
  if (isDesktop()) {
    m.isMaximized = await windowManager.isMaximized();
    m.isMinimized = await windowManager.isMinimized();
    m.isFocused = await isFocused();
    m.isTitleBarHidden = false;
    var size = await windowManager.getSize();
    m.width = size.width;
    m.height = size.height;
    var pos = await windowManager.getPosition();
    m.left = pos.dx;
    m.top = pos.dy;
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
