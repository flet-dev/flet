import 'package:flet/src/utils/platform.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';
import 'package:window_to_front/window_to_front.dart';

import '../models/window_media_data.dart';

Future setWindowTitle(String title) async {
  if (isDesktop()) {
    debugPrint("setWindowTitle($title)");
    await windowManager.setTitle(title);
  }
}

Future setWindowBackgroundColor(Color bgcolor) async {
  if (isDesktop()) {
    debugPrint("setWindowBackgroundColor($bgcolor)");
    await windowManager.setBackgroundColor(bgcolor);
  }
}

Future setWindowSize(double? width, double? height) async {
  if (isDesktop()) {
    debugPrint("setWindowSize($width, $height)");
    var currentSize = await windowManager.getSize();
    await windowManager.setSize(
        Size(width ?? currentSize.width, height ?? currentSize.height),
        animate: defaultTargetPlatform != TargetPlatform.macOS);
  }
}

Future setWindowMinSize(double? minWidth, double? minHeight) async {
  if (isDesktop()) {
    debugPrint("setWindowMinSize($minWidth, $minHeight)");
    await windowManager.setMinimumSize(Size(minWidth ?? 0, minHeight ?? 0));
  }
}

Future setWindowMaxSize(double? maxWidth, double? maxHeight) async {
  if (isDesktop()) {
    debugPrint("setWindowMaxSize($maxWidth, $maxHeight)");
    await windowManager.setMaximumSize(Size(maxWidth ?? -1, maxHeight ?? -1));
  }
}

Future setWindowPosition(double? top, double? left) async {
  if (isDesktop()) {
    debugPrint("setWindowPosition($top, $left)");
    var currentPos = await windowManager.getPosition();
    await windowManager.setPosition(
        Offset(left ?? currentPos.dx, top ?? currentPos.dy),
        animate: defaultTargetPlatform != TargetPlatform.macOS);
  }
}

Future setWindowOpacity(double opacity) async {
  if (isDesktop()) {
    debugPrint("setWindowOpacity($opacity)");
    await windowManager.setOpacity(opacity);
  }
}

Future setWindowMinimizability(bool minimizable) async {
  if (isDesktop()) {
    debugPrint("setWindowMinimizability($minimizable)");
    await windowManager.setMinimizable(minimizable);
  }
}

Future setWindowMaximizability(bool maximizable) async {
  if (isDesktop()) {
    debugPrint("setWindowMaximizability($maximizable)");
    await windowManager.setMaximizable(maximizable);
  }
}

Future setWindowResizability(bool resizable) async {
  if (isDesktop()) {
    debugPrint("setWindowResizability($resizable)");
    await windowManager.setResizable(resizable);
  }
}

Future setWindowMovability(bool movable) async {
  if (isDesktop()) {
    debugPrint("setWindowMovability($movable)");
    await windowManager.setMovable(movable);
  }
}

Future setWindowFullScreen(bool fullScreen) async {
  if (isDesktop() && await windowManager.isFullScreen() != fullScreen) {
    debugPrint("setWindowFullScreen($fullScreen)");
    await windowManager.setFullScreen(fullScreen);
  }
}

Future setWindowAlwaysOnTop(bool alwaysOnTop) async {
  if (isDesktop() && await windowManager.isAlwaysOnTop() != alwaysOnTop) {
    debugPrint("setWindowAlwaysOnTop($alwaysOnTop)");
    await windowManager.setAlwaysOnTop(alwaysOnTop);
  }
}

Future setWindowAlwaysOnBottom(bool alwaysOnBottom) async {
  if (isDesktop()) {
    debugPrint("setWindowAlwaysOnBottom($alwaysOnBottom)");
    await windowManager.setAlwaysOnBottom(alwaysOnBottom);
  }
}

Future setWindowPreventClose(bool preventClose) async {
  if (isDesktop()) {
    debugPrint("setWindowPreventClose($preventClose)");
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
    debugPrint("setWindowSkipTaskBar($skipTaskBar)");
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
    debugPrint("setWindowProgressBar($progress)");
    await windowManager.setProgressBar(progress);
  }
}

Future setWindowShadow(bool hasShadow) async {
  if (isDesktop()) {
    debugPrint("setWindowHasShadow($hasShadow)");
    debugPrint("${windowManager.hasShadow()}");
    await windowManager.setHasShadow(hasShadow);
  }
}

Future setWindowBadgeLabel(String label) async {
  if (isDesktop()) {
    debugPrint("setWindowBadgeLabel($label)");
    await windowManager.setBadgeLabel(label);
  }
}

Future setWindowIcon(String iconPath) async {
  if (isWindowsDesktop()) {
    debugPrint("setWindowIcon($iconPath)");
    await windowManager.setIcon(iconPath);
  }
}

Future setWindowAlignment(Alignment alignment, [bool animate = true]) async {
  if (isDesktop()) {
    debugPrint("setWindowAlignment($alignment, animate: $animate)");
    await windowManager.setAlignment(alignment, animate: animate);
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

Future windowToFront() async {
  if (isDesktop()) {
    await WindowToFront.activate();
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

Future waitUntilReadyToShow() async {
  if (isDesktop()) {
    debugPrint("waitUntilReadyToShow()");
    await windowManager.waitUntilReadyToShow();
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