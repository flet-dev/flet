import 'page_media.dart';
import 'package:flutter/material.dart';

class LoadingPage extends StatelessWidget {
  final String title;

  const LoadingPage({Key? key, required this.title}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Stack(children: const [
      Center(child: CircularProgressIndicator()),
      PageMedia()
    ]));
  }
}
