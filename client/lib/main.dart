import 'dart:developer';
import 'dart:io';

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

  final store = Store<AppState>(appReducer, initialState: AppState.initial());

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

  String pageName = getWebPageName(pageUri);
  String? sessionId = SessionStore.get("sessionId");

  // connect WS
  ws.connect(serverUrl: getWebSocketEndpoint(pageUri), store: store);

  runApp(FletApp(
    title: 'Flet',
    store: store,
    pageName: pageName,
    sessionId: sessionId,
  ));
}

class FletApp extends StatelessWidget {
  final Store<AppState> store;
  final String title;
  final String pageName;
  final String? sessionId;

  const FletApp({
    Key? key,
    required this.store,
    required this.title,
    required this.pageName,
    required this.sessionId,
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
              pageName: pageName,
              sessionId: sessionId,
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
