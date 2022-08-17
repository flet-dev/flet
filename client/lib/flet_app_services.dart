import 'package:flet_view/reducers.dart';
import 'package:flet_view/web_socket_client.dart';
import 'package:flutter/material.dart';
import 'package:redux/redux.dart';

import 'actions.dart';
import 'models/app_state.dart';

class FletAppServices extends InheritedWidget {
  final String pageUrl;
  final String sessionId;
  late final WebSocketClient ws;
  late final Store<AppState> store;

  FletAppServices(
      {Key? key,
      required Widget child,
      required this.pageUrl,
      required this.sessionId})
      : super(key: key, child: child) {
    ws = WebSocketClient();
    store = Store<AppState>(appReducer, initialState: AppState.initial());
    ws.store = store;
    // connect to a page
    var pageUri = Uri.parse(pageUrl);
    store.dispatch(PageLoadAction(pageUri, sessionId, ws));
  }

  @override
  bool updateShouldNotify(covariant InheritedWidget oldWidget) {
    return true;
  }

  static FletAppServices of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<FletAppServices>()!;
}
