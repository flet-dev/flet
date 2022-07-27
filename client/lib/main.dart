import 'dart:io';

import 'package:flet_view/actions.dart';
import 'package:flet_view/utils/desktop.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';
import 'package:url_strategy/url_strategy.dart';

import '../utils/platform_utils_non_web.dart'
    if (dart.library.js) "../utils/platform_utils_web.dart";
import '../utils/session_store_non_web.dart'
    if (dart.library.js) "../utils/session_store_web.dart";
import 'controls/create_control.dart';
import 'models/app_state.dart';
import 'models/page_view_model.dart';
import 'reducers.dart';
import 'web_socket_client.dart';

const bool isProduction = bool.fromEnvironment('dart.vm.product');

void main([List<String>? args]) async {
  if (isProduction) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  }

  await setupDesktop();

  var pageUri = Uri.base;
  //debugPrint("Uri.base: ${Uri.base}");

  if (kDebugMode) {
    pageUri = Uri.parse("http://localhost:8550");
  }

  if (kIsWeb) {
    debugPrint("Flet View is running in Web mode");
    var routeUrlStrategy = getRouteUrlStrategy();
    debugPrint("URL Strategy: $routeUrlStrategy");
    if (routeUrlStrategy == "path") {
      setPathUrlStrategy();
    }
  } else if ((Platform.isWindows || Platform.isMacOS || Platform.isLinux) &&
      !kDebugMode) {
    debugPrint("Flet View is running in Desktop mode");
    // first argument must be
    if (args!.isEmpty) {
      throw Exception('Page URL must be provided as a first argument.');
    }
    pageUri = Uri.parse(args[0]);
  }

  debugPrint("Page URL: $pageUri");

  final store = Store<AppState>(appReducer, initialState: AppState.initial());
  ws.store = store;

  String sessionId = SessionStore.get("sessionId") ?? "";

  // connect to a page
  store.dispatch(PageLoadAction(pageUri, sessionId));

  runApp(FletApp(
    title: 'Flet',
    store: store,
  ));
}

class FletApp extends StatelessWidget {
  final Store<AppState> store;
  final String title;

  const FletApp({
    Key? key,
    required this.store,
    required this.title,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return StoreProvider<AppState>(
      store: store,
      child: StoreConnector<AppState, PageViewModel>(
        distinct: true,
        converter: (store) => PageViewModel.fromStore(store),
        builder: (context, viewModel) {
          if (viewModel.error != "") {
            return MaterialApp(
                title: title,
                home: Scaffold(
                  body: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.error_outline,
                          color: Colors.red, size: 25),
                      Text(viewModel.error,
                          style: const TextStyle(color: Colors.red))
                    ],
                  ),
                ));
          } else {
            return createControl(null, "page", false);
          }
        },
      ),
    );
  }
}
