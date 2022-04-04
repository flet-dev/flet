import 'package:flutter/material.dart';

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
          debugPrint("builder Loading");
          MediaQueryData media = MediaQuery.of(context);
          debugPrint("Screen size: ${media.size}");

          ws.registerWebClient(
              pageName: pageName,
              pageHash: "",
              sessionId: sessionId,
              winWidth: media.size.width.toInt().toString(),
              winHeight: media.size.height.toInt().toString());

          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }));
  }
}
