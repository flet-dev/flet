import 'dart:developer';
import 'dart:io';

import 'package:flet_view/actions.dart';
import 'package:flet_view/widgets/loading_page.dart';
import 'package:flutter/foundation.dart';
import 'package:window_size/window_size.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';
import 'models/app_state.dart';
import 'models/page_view_model.dart';
import 'reducers.dart';
import 'utils/uri.dart';
import 'web_socket_client.dart';
import 'controls/create_control.dart';

import 'session_store/session_store.dart'
    if (dart.library.io) "session_store/session_store_io.dart"
    if (dart.library.js) "session_store/session_store_js.dart";

void main([List<String>? args]) async {
  //setupWindow();

  var pageUri = Uri.base;

  if (kDebugMode) {
    pageUri = Uri.parse("http://localhost:8550/p/test1");
  }

  if (kIsWeb) {
    debugPrint("Flet View is running in Web mode");
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
          if (viewModel.isLoading) {
            return LoadingPage(
              title: title,
            );
          } else if (viewModel.error != "") {
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

const double windowWidth = 480;
const double windowHeight = 854;

void setupWindow() {
  if (!kIsWeb && (Platform.isWindows || Platform.isLinux || Platform.isMacOS)) {
    WidgetsFlutterBinding.ensureInitialized();
    setWindowTitle('Navigation and routing');
    setWindowMinSize(const Size(windowWidth, windowHeight));
    setWindowMaxSize(const Size(windowWidth, windowHeight));
    getCurrentScreen().then((screen) {
      setWindowFrame(Rect.fromCenter(
        center: screen!.frame.center,
        width: windowWidth,
        height: windowHeight,
      ));
    });
  }
}
