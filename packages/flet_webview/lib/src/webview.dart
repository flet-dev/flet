import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'webview_desktop.dart'
    if (dart.library.html) "webview_desktop_vain.dart";
import 'webview_mobile.dart';
import 'webview_web.dart' if (dart.library.io) "webview_web_vain.dart";

class WebViewControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const WebViewControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${control.id}");
    String url = control.attrString("url", "https://flet.dev")!;
    Widget view =
        const ErrorControl("Webview is not yet supported on this platform.");
    if (isMobile()) {
      view = WebviewMobile(control: control, backend: backend);
    } else if (isWeb()) {
      view = WebviewWeb(url: url);
    } else if (isDesktop()) {
      view = WebviewDesktop(url: url);
    }

    return constrainedControl(context, view, parent, control);
  }
}
