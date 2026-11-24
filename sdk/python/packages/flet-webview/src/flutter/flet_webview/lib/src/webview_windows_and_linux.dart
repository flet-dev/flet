import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

class WebviewDesktop extends StatelessWidget {
  const WebviewDesktop({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const ErrorControl("Webview is not yet supported on this Platform.");
  }
}
