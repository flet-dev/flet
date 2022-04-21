import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:window_size/window_size.dart' as desktop;

const double windowWidth = 480;
const double windowHeight = 854;

void setWindowTitle(String title) {
  if (!kIsWeb && (Platform.isWindows || Platform.isLinux || Platform.isMacOS)) {
    desktop.setWindowTitle(title);
  }
}

void setupDesktop() {
  if (!kIsWeb && (Platform.isWindows || Platform.isLinux || Platform.isMacOS)) {
    WidgetsFlutterBinding.ensureInitialized();
    // setWindowMinSize(const Size(windowWidth, windowHeight));
    // setWindowMaxSize(const Size(windowWidth, windowHeight));
    // getCurrentScreen().then((screen) {
    //   setWindowFrame(Rect.fromCenter(
    //     center: screen!.frame.center,
    //     width: windowWidth,
    //     height: windowHeight,
    //   ));
    // });
  }
}
