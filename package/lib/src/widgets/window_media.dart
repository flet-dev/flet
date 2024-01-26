import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../utils/desktop.dart';

class WindowMedia extends StatefulWidget {
  final dynamic dispatch;
  const WindowMedia({super.key, required this.dispatch});

  @override
  // ignore: library_private_types_in_public_api
  WindowMediaState createState() => WindowMediaState();
}

class WindowMediaState extends State<WindowMedia> with WindowListener {
  @override
  void initState() {
    super.initState();
    windowManager.addListener(this);
  }

  @override
  void dispose() {
    windowManager.removeListener(this);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return const SizedBox.shrink();
  }

  @override
  void onWindowEvent(String eventName) {
    //debugPrint('START [WindowManager] onWindowEvent: $eventName');

    if (eventName == "resize" || eventName == "move") {
      return;
    }

    debugPrint('[WindowManager] onWindowEvent: $eventName');
    getWindowMediaData().then((wmd) {
      debugPrint("WindowMediaData: $wmd");
      widget.dispatch!(WindowEventAction(
          eventName, wmd, FletAppServices.of(context).server));
    });
  }
}
