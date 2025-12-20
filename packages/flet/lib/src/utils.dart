import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import 'utils/platform.dart';

Future setupDesktop({bool hideWindowOnStart = false}) async {
  if (isDesktopPlatform()) {
    WidgetsFlutterBinding.ensureInitialized();
    await windowManager.ensureInitialized();

    Map<String, String> env = Platform.environment;
    var hideWindowOnStartEnv = env["FLET_HIDE_WINDOW_ON_START"];
    debugPrint("hideWindowOnStart: $hideWindowOnStart");
    debugPrint("hideWindowOnStartEnv: $hideWindowOnStartEnv");

    await windowManager.waitUntilReadyToShow(null, () async {
      if (hideWindowOnStartEnv == null && !hideWindowOnStart) {
        await windowManager.show();
        await windowManager.focus();
      }
    });
  }
}
