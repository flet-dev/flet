import 'package:flet/src/flet_app_errors_handler.dart';
import 'package:flutter/material.dart';
import 'package:redux/redux.dart';

import 'actions.dart';
import 'models/app_state.dart';
import 'reducers.dart';
import 'web_socket_client.dart';

class FletAppServices extends InheritedWidget {
  final String pageUrl;
  final FletAppErrorsHandler? errorsHandler;
  late final WebSocketClient ws;
  late final Store<AppState> store;

  FletAppServices(
      {Key? key,
      required Widget child,
      required this.pageUrl,
      this.errorsHandler})
      : super(key: key, child: child) {
    store = Store<AppState>(appReducer, initialState: AppState.initial());
    ws = WebSocketClient(store);
    if (errorsHandler != null) {
      errorsHandler!.addListener(() {
        if (store.state.isRegistered) {
          ws.pageEventFromWeb(
              eventTarget: "page",
              eventName: "error",
              eventData: errorsHandler!.error!);
        }
      });
    }
    // connect to a page
    var pageUri = Uri.parse(pageUrl);
    store.dispatch(PageLoadAction(pageUri, ws));
  }

  @override
  bool updateShouldNotify(covariant InheritedWidget oldWidget) {
    return false;
  }

  static FletAppServices of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<FletAppServices>()!;
}
