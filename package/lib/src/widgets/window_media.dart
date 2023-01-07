import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:window_manager/window_manager.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../utils/desktop.dart';

class WindowMedia extends StatefulWidget {
  const WindowMedia({Key? key}) : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
  WindowMediaState createState() => WindowMediaState();
}

class WindowMediaState extends State<WindowMedia> with WindowListener {
  Timer? _debounce;
  Function? _dispatch;

  @override
  void initState() {
    super.initState();
    windowManager.addListener(this);
  }

  @override
  void dispose() {
    windowManager.removeListener(this);
    _debounce?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          _dispatch = dispatch;
          return const SizedBox.shrink();
        });
  }

  @override
  void onWindowEvent(String eventName) {
    //debugPrint('START [WindowManager] onWindowEvent: $eventName');

    if (eventName == "resize" || eventName == "move") {
      return;
    }

    send() {
      debugPrint('[WindowManager] onWindowEvent: $eventName');
      getWindowMediaData().then((wmd) {
        debugPrint("WindowMediaData: $wmd");
        _dispatch!(WindowEventAction(
            eventName, wmd, FletAppServices.of(context).server));
      });
    }

    if (eventName == "resized" || eventName == "moved") {
      if (_debounce?.isActive ?? false) _debounce!.cancel();
      _debounce = Timer(const Duration(milliseconds: 300), () {
        send();
      });
    } else {
      send();
    }
  }
}
