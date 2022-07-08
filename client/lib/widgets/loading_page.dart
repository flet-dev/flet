import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/page_load_view_model.dart';
import '../utils/desktop.dart';
import '../utils/platform_utils.dart'
    if (dart.library.io) "../utils/platform_utils_io.dart"
    if (dart.library.js) "../utils/platform_utils_js.dart";
import '../utils/uri.dart';
import '../web_socket_client.dart';

class LoadingPage extends StatelessWidget {
  final String title;

  const LoadingPage({Key? key, required this.title}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: title,
        home: Builder(builder: (context) {
          return StoreConnector<AppState, PageLoadViewModel>(
              distinct: true,
              converter: (store) => PageLoadViewModel.fromStore(store),
              builder: (context, viewModel) {
                MediaQueryData media = MediaQuery.of(context);
                if (media.size != viewModel.sizeViewModel.size) {
                  getWindowMediaData().then((wmd) {
                    viewModel.sizeViewModel
                        .dispatch(PageSizeChangeAction(media.size));

                    if (viewModel.pageUri != null) {
                      String pageName = getWebPageName(viewModel.pageUri!);
                      String? sessionId = viewModel.sessionId;

                      ws.registerWebClient(
                          pageName: pageName,
                          pageHash: "",
                          sessionId: sessionId,
                          pageWidth: media.size.width.toString(),
                          pageHeight: media.size.height.toString(),
                          windowWidth:
                              wmd.width != null ? wmd.width.toString() : "",
                          windowHeight:
                              wmd.height != null ? wmd.height.toString() : "",
                          windowTop: wmd.top != null ? wmd.top.toString() : "",
                          windowLeft:
                              wmd.left != null ? wmd.left.toString() : "",
                          isPWA: isProgressiveWebApp().toString());
                    }
                  });
                } else {
                  debugPrint("Page size did not change on load.");
                }
                return const Scaffold(
                  body: Center(child: CircularProgressIndicator()),
                );
              });
        }));
  }
}
