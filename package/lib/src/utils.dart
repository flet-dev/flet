import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import 'utils/desktop.dart';

Future setupDesktop() async {
  if (isDesktop()) {
    WidgetsFlutterBinding.ensureInitialized();
    // Must add this line.
    await windowManager.ensureInitialized();
  }
}
