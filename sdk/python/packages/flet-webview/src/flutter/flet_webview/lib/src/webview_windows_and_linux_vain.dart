import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class WebviewDesktop extends StatefulWidget {
  const WebviewDesktop({Key? key}) : super(key: key);

  @override
  State<WebviewDesktop> createState() => _WebviewDesktopState();
}

class _WebviewDesktopState extends State<WebviewDesktop> {
  @override
  Widget build(BuildContext context) {
    return const ErrorControl("Webview is not yet supported on this Platform.");
  }
}
