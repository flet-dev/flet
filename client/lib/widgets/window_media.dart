import 'dart:async';

import 'package:flet_view/utils/desktop.dart';
import 'package:flutter/cupertino.dart';
import 'package:window_manager/window_manager.dart';

class WindowMedia extends StatefulWidget {
  const WindowMedia({Key? key}) : super(key: key);

  @override
  _WindowMediaState createState() => _WindowMediaState();
}

class _WindowMediaState extends State<WindowMedia> with WindowListener {
  Timer? _debounce;

  @override
  void initState() {
    windowManager.addListener(this);
    super.initState();
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
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 500), () {
      debugPrint('[WindowManager] onWindowEvent: $eventName');
      getWindowMediaData().then((wmd) {
        debugPrint("WindowMediaData: $wmd");
        //dispatch(PageSizeChangeAction(newSize, windowSize));
      });
    });
  }

  @override
  void onWindowClose() {
    // do something
  }

  @override
  void onWindowFocus() {
    debugPrint('[WindowManager] onWindowFocus');
  }

  @override
  void onWindowBlur() {
    debugPrint('[WindowManager] onWindowBlur');
  }

  @override
  void onWindowMaximize() {
    // do something
  }

  @override
  void onWindowUnmaximize() {
    // do something
  }

  @override
  void onWindowMinimize() {
    // do something
  }

  @override
  void onWindowRestore() {
    // do something
  }

  @override
  void onWindowResize() {
    // do something
  }

  @override
  void onWindowMove() {
    // do something
  }

  @override
  void onWindowEnterFullScreen() {
    // do something
  }

  @override
  void onWindowLeaveFullScreen() {
    // do something
  }
}
