import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import '../models/window_media_data.dart';

Future setWindowTitle(String title) async {
  if (isDesktop()) {
    debugPrint("setWindowTitle()");
    await windowManager.setTitle(title);
  }
}

Future setWindowSize(double? width, double? height) async {
  if (isDesktop()) {
    debugPrint("setWindowSize()");
    var currentSize = await windowManager.getSize();
    await windowManager.setSize(
        Size(width ?? currentSize.width, height ?? currentSize.height),
        animate: defaultTargetPlatform != TargetPlatform.macOS);
  }
}

Future setWindowMinSize(double? minWidth, double? minHeight) async {
  if (isDesktop()) {
    debugPrint("setWindowMinSize()");
    await windowManager.setMinimumSize(Size(minWidth ?? 0, minHeight ?? 0));
  }
}

Future setWindowMaxSize(double? maxWidth, double? maxHeight) async {
  if (isDesktop()) {
    debugPrint("setWindowMaxSize()");
    await windowManager.setMaximumSize(Size(maxWidth ?? -1, maxHeight ?? -1));
  }
}

Future setWindowPosition(double? top, double? left) async {
  if (isDesktop()) {
    debugPrint("setWindowPosition()");
    var currentPos = await windowManager.getPosition();
    await windowManager.setPosition(
        Offset(left ?? currentPos.dx, top ?? currentPos.dy),
        animate: defaultTargetPlatform != TargetPlatform.macOS);
  }
}

Future setWindowOpacity(double opacity) async {
  if (isDesktop()) {
    debugPrint("setWindowOpacity()");
    await windowManager.setOpacity(opacity);
  }
}

Future setWindowMinimizability(bool minimizable) async {
  if (isDesktop()) {
    debugPrint("setWindowMinimizability()");
    await windowManager.setMinimizable(minimizable);
  }
}

Future setWindowResizability(bool resizable) async {
  if (isDesktop()) {
    debugPrint("setWindowResizability()");
    await windowManager.setResizable(resizable);
  }
}

Future setWindowMovability(bool movable) async {
  if (isDesktop()) {
    debugPrint("setWindowMovability()");
    await windowManager.setMovable(movable);
  }
}

Future setWindowFullScreen(bool fullScreen) async {
  if (isDesktop() && await windowManager.isFullScreen() != fullScreen) {
    debugPrint("setWindowFullScreen()");
    await windowManager.setFullScreen(fullScreen);
  }
}

Future setWindowAlwaysOnTop(bool alwaysOnTop) async {
  if (isDesktop() && await windowManager.isAlwaysOnTop() != alwaysOnTop) {
    debugPrint("setWindowAlwaysOnTop()");
    await windowManager.setAlwaysOnTop(alwaysOnTop);
  }
}

Future setWindowPreventClose(bool preventClose) async {
  if (isDesktop()) {
    debugPrint("setWindowPreventClose()");
    await windowManager.setPreventClose(preventClose);
  }
}

Future setWindowTitleBarVisibility(
    bool titleBarHidden, bool titleBarButtonsHidden) async {
  if (isDesktop()) {
    debugPrint("setWindowTitleBarVisibility()");
    await windowManager.setTitleBarStyle(
        titleBarHidden ? TitleBarStyle.hidden : TitleBarStyle.normal,
        windowButtonVisibility: !titleBarButtonsHidden);
  }
}

Future setWindowSkipTaskBar(bool skipTaskBar) async {
  if (isDesktop()) {
    debugPrint("setWindowSkipTaskBar()");
    await windowManager.setSkipTaskbar(skipTaskBar);
  }
}

Future setWindowFrameless() async {
  if (isDesktop()) {
    debugPrint("setWindowFrameless()");
    await windowManager.setAsFrameless();
  }
}

Future setWindowProgressBar(double progress) async {
  if (isDesktop()) {
    debugPrint("setWindowProgressBar()");
    await windowManager.setProgressBar(progress);
  }
}

Future minimizeWindow() async {
  if (isDesktop() && !await windowManager.isMinimized()) {
    debugPrint("minimizeWindow()");
    await windowManager.minimize();
  }
}

Future restoreWindow() async {
  if (isDesktop() && await windowManager.isMinimized()) {
    debugPrint("restoreWindow()");
    await windowManager.restore();
  }
}

Future maximizeWindow() async {
  if (isDesktop() && !await windowManager.isMaximized()) {
    debugPrint("maximizeWindow()");
    await windowManager.maximize();
  }
}

Future unmaximizeWindow() async {
  if (isDesktop() && await windowManager.isMaximized()) {
    debugPrint("unmaximizeWindow()");
    await windowManager.unmaximize();
  }
}

Future showWindow() async {
  if (isDesktop() && !await windowManager.isVisible()) {
    debugPrint("showWindow()");
    await windowManager.show();
  }
}

Future hideWindow() async {
  if (isDesktop() && await windowManager.isVisible()) {
    debugPrint("hideWindow()");
    await windowManager.hide();
  }
}

Future focusWindow() async {
  if (isDesktop() &&
      !await windowManager.isFocused() &&
      !await windowManager.isMinimized()) {
    debugPrint("focusWindow()");
    await windowManager.focus();
  }
}

Future blurWindow() async {
  if (isDesktop() &&
      (defaultTargetPlatform == TargetPlatform.windows ||
          defaultTargetPlatform == TargetPlatform.macOS) &&
      await windowManager.isFocused()) {
    debugPrint("blurWindow()");
    await windowManager.blur();
  }
}

Future destroyWindow() async {
  if (isDesktop()) {
    debugPrint("destroyWindow()");
    await windowManager.destroy();
  }
}

Future centerWindow() async {
  if (isDesktop()) {
    debugPrint("centerWindow()");
    await windowManager.center();
  }
}

Future closeWindow() async {
  if (isDesktop()) {
    debugPrint("closeWindow()");
    await windowManager.close();
  }
}

Future isFocused() async {
  if (isDesktop() &&
      (defaultTargetPlatform == TargetPlatform.windows ||
          defaultTargetPlatform == TargetPlatform.macOS)) {
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
    m.isFullScreen = await windowManager.isFullScreen();
    m.isVisible = await windowManager.isVisible();
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

bool isDesktop() {
  return !kIsWeb &&
      (defaultTargetPlatform == TargetPlatform.windows ||
          defaultTargetPlatform == TargetPlatform.macOS ||
          defaultTargetPlatform == TargetPlatform.linux);
}
