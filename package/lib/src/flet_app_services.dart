import 'package:flutter/material.dart';
import 'package:redux/redux.dart';

import 'actions.dart';
import 'flet_app_errors_handler.dart';
import 'flet_server.dart';
import 'models/app_state.dart';
import 'models/control.dart';
import 'models/control_view_model.dart';
import 'reducers.dart';

class FletAppServices extends InheritedWidget {
  final String pageUrl;
  final String assetsDir;
  final FletAppErrorsHandler? errorsHandler;
  final Map<String, Widget Function(Control?, ControlViewModel)>?
      controlsMapping;
  late final FletServer server;
  late final Store<AppState> store;

  FletAppServices(
      {Key? key,
      required Widget child,
      required this.pageUrl,
      required this.assetsDir,
      this.controlsMapping,
      this.errorsHandler})
      : super(key: key, child: child) {
    store = Store<AppState>(appReducer, initialState: AppState.initial());
    server = FletServer(store);
    if (errorsHandler != null) {
      errorsHandler!.addListener(() {
        if (store.state.isRegistered) {
          server.sendPageEvent(
              eventTarget: "page",
              eventName: "error",
              eventData: errorsHandler!.error!);
        }
      });
    }
    // connect to a page
    var pageUri = Uri.parse(pageUrl);
    store.dispatch(PageLoadAction(pageUri, assetsDir, server, controlsMapping));
  }

  @override
  bool updateShouldNotify(covariant InheritedWidget oldWidget) {
    return false;
  }

  void close() {
    server.disconnect();
  }

  static FletAppServices of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<FletAppServices>()!;
}
