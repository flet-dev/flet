import 'package:flutter/material.dart';

import 'page_media.dart';

class LoadingPage extends StatelessWidget {
  final String title;
  final String message;

  const LoadingPage({Key? key, required this.title, required this.message})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Stack(children: [
      Center(
          child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(),
          const SizedBox(height: 10),
          Text(
            message,
            style: Theme.of(context).textTheme.bodySmall,
          )
        ],
      )),
      const PageMedia()
    ]));
  }
}
