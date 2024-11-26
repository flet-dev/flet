import 'dart:io';

import 'package:flet/src/utils/platform.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';
import 'package:window_to_front/window_to_front.dart';

import '../models/window_media_data.dart';

Future setWindowTitle(String title) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowTitle($title)");
    await windowManager.setTitle(title);
  }
}

Future setWindowBackgroundColor(Color bgcolor) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowBackgroundColor($bgcolor)");
    await windowManager.setBackgroundColor(bgcolor);
  }
}

Future setWindowSize(double? width, double? height) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowSize($width, $height)");
    var currentSize = await windowManager.getSize();
    await windowManager.setSize(
        Size(width ?? currentSize.width, height ?? currentSize.height),
        animate: defaultTargetPlatform != TargetPlatform.macOS);
  }
}

Future setWindowMinSize(double? minWidth, double? minHeight) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowMinSize($minWidth, $minHeight)");
    await windowManager.setMinimumSize(Size(minWidth ?? 0, minHeight ?? 0));
  }
}

Future setWindowMaxSize(double? maxWidth, double? maxHeight) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowMaxSize($maxWidth, $maxHeight)");
    await windowManager.setMaximumSize(Size(maxWidth ?? -1, maxHeight ?? -1));
  }
}

Future setWindowPosition(double? top, double? left) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowPosition($top, $left)");
    var currentPos = await windowManager.getPosition();
    await windowManager.setPosition(
        Offset(left ?? currentPos.dx, top ?? currentPos.dy),
        animate: defaultTargetPlatform != TargetPlatform.macOS);
  }
}

Future setWindowOpacity(double opacity) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowOpacity($opacity)");
    await windowManager.setOpacity(opacity);
  }
}

Future setWindowMinimizability(bool minimizable) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowMinimizability($minimizable)");
    await windowManager.setMinimizable(minimizable);
  }
}

Future setWindowMaximizability(bool maximizable) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowMaximizability($maximizable)");
    await windowManager.setMaximizable(maximizable);
  }
}

Future setWindowResizability(bool resizable) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowResizability($resizable)");
    await windowManager.setResizable(resizable);
  }
}

Future setWindowMovability(bool movable) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowMovability($movable)");
    await windowManager.setMovable(movable);
  }
}

Future setWindowFullScreen(bool fullScreen) async {
  if (isDesktopPlatform() && await windowManager.isFullScreen() != fullScreen) {
    debugPrint("setWindowFullScreen($fullScreen)");
    await windowManager.setFullScreen(fullScreen);
  }
}

Future setWindowAlwaysOnTop(bool alwaysOnTop) async {
  if (isDesktopPlatform() &&
      await windowManager.isAlwaysOnTop() != alwaysOnTop) {
    debugPrint("setWindowAlwaysOnTop($alwaysOnTop)");
    await windowManager.setAlwaysOnTop(alwaysOnTop);
  }
}

Future setWindowAlwaysOnBottom(bool alwaysOnBottom) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowAlwaysOnBottom($alwaysOnBottom)");
    await windowManager.setAlwaysOnBottom(alwaysOnBottom);
  }
}

Future setWindowPreventClose(bool preventClose) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowPreventClose($preventClose)");
    await windowManager.setPreventClose(preventClose);
  }
}

Future setWindowTitleBarVisibility(
    bool titleBarHidden, bool titleBarButtonsHidden) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowTitleBarVisibility()");
    await windowManager.setTitleBarStyle(
        titleBarHidden ? TitleBarStyle.hidden : TitleBarStyle.normal,
        windowButtonVisibility: !titleBarButtonsHidden);
  }
}

Future setWindowSkipTaskBar(bool skipTaskBar) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowSkipTaskBar($skipTaskBar)");
    await windowManager.setSkipTaskbar(skipTaskBar);
  }
}

Future setWindowFrameless() async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowFrameless()");
    await windowManager.setAsFrameless();
  }
}

Future setWindowProgressBar(double progress) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowProgressBar($progress)");
    await windowManager.setProgressBar(progress);
  }
}

Future setWindowShadow(bool hasShadow) async {
  if (isDesktopPlatform()) {
    debugPrint("setWindowHasShadow($hasShadow)");
    debugPrint("${windowManager.hasShadow()}");
    await windowManager.setHasShadow(hasShadow);
  }
}

Future setWindowBadgeLabel(String label) async {
  if (isDesktopPlatform()) {
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
  if (isDesktopPlatform()) {
    debugPrint("setWindowAlignment($alignment, animate: $animate)");
    await windowManager.setAlignment(alignment, animate: animate);
  }
}

Future minimizeWindow() async {
  if (isDesktopPlatform() && !await windowManager.isMinimized()) {
    debugPrint("minimizeWindow()");
    await windowManager.minimize();
  }
}

Future restoreWindow() async {
  if (isDesktopPlatform() && await windowManager.isMinimized()) {
    debugPrint("restoreWindow()");
    await windowManager.restore();
  }
}

Future maximizeWindow() async {
  if (isDesktopPlatform() && !await windowManager.isMaximized()) {
    debugPrint("maximizeWindow()");
    await windowManager.maximize();
  }
}

Future unmaximizeWindow() async {
  if (isDesktopPlatform() && await windowManager.isMaximized()) {
    debugPrint("unmaximizeWindow()");
    await windowManager.unmaximize();
  }
}

Future showWindow() async {
  if (isDesktopPlatform() && !await windowManager.isVisible()) {
    debugPrint("showWindow()");
    await windowManager.show();
  }
}

Future hideWindow() async {
  if (isDesktopPlatform() && await windowManager.isVisible()) {
    debugPrint("hideWindow()");
    await windowManager.hide();
  }
}

Future focusWindow() async {
  if (isDesktopPlatform() &&
      !await windowManager.isFocused() &&
      !await windowManager.isMinimized()) {
    debugPrint("focusWindow()");
    await windowManager.focus();
  }
}

Future windowToFront() async {
  if (isDesktopPlatform()) {
    await WindowToFront.activate();
  }
}

Future blurWindow() async {
  if (isDesktopPlatform() &&
      (defaultTargetPlatform == TargetPlatform.windows ||
          defaultTargetPlatform == TargetPlatform.macOS) &&
      await windowManager.isFocused()) {
    debugPrint("blurWindow()");
    await windowManager.blur();
  }
}

Future destroyWindow() async {
  if (isDesktopPlatform() || isMobilePlatform()) {
    debugPrint("destroyWindow()");
  }
  if (isDesktopPlatform()) {
    await windowManager.destroy();
  } else if (defaultTargetPlatform == TargetPlatform.iOS) {
    exit(0);
  } else if (defaultTargetPlatform == TargetPlatform.android) {
    SystemNavigator.pop();
  }
}

Future waitUntilReadyToShow() async {
  if (isDesktopPlatform()) {
    debugPrint("waitUntilReadyToShow()");
    await windowManager.waitUntilReadyToShow();
  }
}

Future centerWindow() async {
  if (isDesktopPlatform()) {
    debugPrint("centerWindow()");
    await windowManager.center();
  }
}

Future closeWindow() async {
  if (isDesktopPlatform()) {
    debugPrint("closeWindow()");
    await windowManager.close();
  }
}

Future isFocused() async {
  if (isDesktopPlatform() &&
      (defaultTargetPlatform == TargetPlatform.windows ||
          defaultTargetPlatform == TargetPlatform.macOS)) {
    return await windowManager.isFocused();
  } else {
    return false;
  }
}

Future<WindowMediaData> getWindowMediaData() async {
  var m = WindowMediaData();
  if (isDesktopPlatform()) {
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