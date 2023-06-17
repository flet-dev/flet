import 'package:flutter/material.dart';
import 'package:redux/redux.dart';

import 'actions.dart';
import 'flet_app_errors_handler.dart';
import 'flet_server.dart';
import 'flet_server_protocol.dart';
import 'models/app_state.dart';
import 'reducers.dart';

class FletAppServices extends InheritedWidget {
  final FletAppServices? parentAppServices;
  final String? controlId;
  final int? reconnectIntervalMs;
  final int? reconnectTimeoutMs;
  final String pageUrl;
  final String assetsDir;
  final FletAppErrorsHandler? errorsHandler;
  late final FletServer server;
  late final Store<AppState> store;
  final Map<String, GlobalKey> globalKeys = {};
  final Map<String, ControlInvokeMethodCallback> controlInvokeMethods = {};

  FletAppServices(
      {Key? key,
      required Widget child,
      required this.pageUrl,
      required this.assetsDir,
      this.errorsHandler,
      this.parentAppServices,
      this.controlId,
      this.reconnectIntervalMs,
      this.reconnectTimeoutMs})
      : super(key: key, child: child) {
    store = Store<AppState>(appReducer, initialState: AppState.initial());
    server = FletServer(store, controlInvokeMethods,
        reconnectIntervalMs: reconnectIntervalMs,
        reconnectTimeoutMs: reconnectTimeoutMs,
        errorsHandler: errorsHandler);
    if (errorsHandler != null) {
      if (controlId == null) {
        // root error handler
        errorsHandler!.addListener(() {
          if (store.state.isRegistered) {
            server.sendPageEvent(
                eventTarget: "page",
                eventName: "error",
                eventData: errorsHandler!.error!);
          }
        });
      } else if (controlId != null && parentAppServices != null) {
        // parent error handler
        errorsHandler?.addListener(() {
          parentAppServices?.server.sendPageEvent(
              eventTarget: controlId!,
              eventName: "error",
              eventData: errorsHandler!.error!);
        });
      }
    }
    // connect to a page
    var pageUri = Uri.parse(pageUrl);
    store.dispatch(PageLoadAction(pageUri, assetsDir, server));
  }

  @override
  bool updateShouldNotify(covariant InheritedWidget oldWidget) {
    return false;
  }

  void close() {
    server.disconnect();
  }

  static FletAppServices? maybeOf(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<FletAppServices>();

  static FletAppServices of(BuildContext context) => maybeOf(context)!;
}
