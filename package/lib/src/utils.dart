import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import 'utils/desktop.dart';

Future setupDesktop() async {
  if (isDesktop()) {
    WidgetsFlutterBinding.ensureInitialized();
    await windowManager.ensureInitialized();

    WindowOptions windowOptions = WindowOptions(
      size: Size(800, 600),
      center: true,
      backgroundColor: Colors.transparent,
      skipTaskbar: false,
      titleBarStyle: TitleBarStyle.hidden,
    );

    await windowManager.waitUntilReadyToShow(null, () async {
      //await windowManager.show();
      //await windowManager.focus();
      Future.delayed(Duration(seconds: 5)).then((value) async {
        await windowManager.setTitleBarStyle(TitleBarStyle.hidden,
            windowButtonVisibility: false);
        await windowManager.show();
        await windowManager.focus();
      });
    });
  }
}
