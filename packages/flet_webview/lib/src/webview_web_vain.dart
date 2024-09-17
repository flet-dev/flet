import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class WebviewWeb extends StatefulWidget {
  final String url;

  const WebviewWeb({Key? key, required this.url}) : super(key: key);

  @override
  State<WebviewWeb> createState() => _WebviewWebState(url: url);
}

class _WebviewWebState extends State<WebviewWeb> {
  late String url;

  _WebviewWebState({required this.url});

  @override
  Widget build(BuildContext context) {
    return const ErrorControl("Webview is not yet supported on this platform.");
  }
}
