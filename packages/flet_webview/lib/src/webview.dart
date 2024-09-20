import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'webview_mobile_and_mac.dart';
import 'webview_web.dart' if (dart.library.io) "webview_web_vain.dart";
import 'webview_windows_and_linux.dart'
    if (dart.library.html) "webview_windows_and_linux_vain.dart";

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
    if (isMobilePlatform() || isMacOSDesktop()) {
      var bgcolor =
          parseColor(Theme.of(context), control.attrString("bgcolor"));
      view = WebviewMobileAndMac(
          control: control, backend: backend, bgcolor: bgcolor);
    } else if (isWebPlatform()) {
      view = WebviewWeb(control: control, backend: backend);
    } else if (isWindowsDesktop() || isLinuxDesktop()) {
      view = WebviewDesktop(url: url);
    }

    return constrainedControl(context, view, parent, control);
  }
}
