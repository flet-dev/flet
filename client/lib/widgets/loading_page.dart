import 'package:flet_view/actions.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/page_size_view_model.dart';
import '../web_socket_client.dart';

class LoadingPage extends StatelessWidget {
  final String title;
  final String pageName;
  final String? sessionId;

  const LoadingPage(
      {Key? key,
      required this.title,
      required this.pageName,
      required this.sessionId})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: title,
        home: Builder(builder: (context) {
          return StoreConnector<AppState, PageSizeViewModel>(
              distinct: true,
              converter: (store) => PageSizeViewModel.fromStore(store),
              builder: (context, viewModel) {
                MediaQueryData media = MediaQuery.of(context);
                if (media.size != viewModel.size) {
                  viewModel.dispatch(PageSizeChangeAction(media.size));
                  ws.registerWebClient(
                      pageName: pageName,
                      pageHash: "",
                      sessionId: sessionId,
                      winWidth: media.size.width.toInt().toString(),
                      winHeight: media.size.height.toInt().toString());
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
