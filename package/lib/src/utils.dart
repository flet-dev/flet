import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import 'utils/desktop.dart';

Future setupDesktop() async {
  if (isDesktop()) {
    WidgetsFlutterBinding.ensureInitialized();
    await windowManager.ensureInitialized();

    Map<String, String> env = Platform.environment;
    var hideWindowOnStart = env["FLET_HIDE_WINDOW_ON_START"];
    debugPrint("hideWindowOnStart: $hideWindowOnStart");

    await windowManager.waitUntilReadyToShow(null, () async {
      if (hideWindowOnStart == null) {
        await windowManager.show();
        await windowManager.focus();
      }
    });
  }
}
