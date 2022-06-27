import 'package:flet_view/actions.dart';
import 'package:flet_view/models/page_load_view_model.dart';
import 'package:flet_view/utils/desktop.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
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
                  getWindowSize().then((windowSize) {
                    viewModel.sizeViewModel
                        .dispatch(PageSizeChangeAction(media.size, windowSize));

                    if (viewModel.pageUri != null) {
                      String pageName = getWebPageName(viewModel.pageUri!);
                      String? sessionId = viewModel.sessionId;

                      ws.registerWebClient(
                          pageName: pageName,
                          pageHash: "",
                          sessionId: sessionId,
                          pageWidth: media.size.width.toString(),
                          pageHeight: media.size.height.toString(),
                          windowWidth: windowSize.width.toString(),
                          windowHeight: windowSize.height.toString());
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
