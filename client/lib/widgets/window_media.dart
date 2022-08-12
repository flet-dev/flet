import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:window_manager/window_manager.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../utils/desktop.dart';

class WindowMedia extends StatefulWidget {
  const WindowMedia({Key? key}) : super(key: key);

  @override
  _WindowMediaState createState() => _WindowMediaState();
}

class _WindowMediaState extends State<WindowMedia> with WindowListener {
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
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 200), () {
      debugPrint('[WindowManager] onWindowEvent: $eventName');
      getWindowMediaData().then((wmd) {
        debugPrint("WindowMediaData: $wmd");
        _dispatch!(WindowEventAction(eventName, wmd));
      });
    });
  }
}
