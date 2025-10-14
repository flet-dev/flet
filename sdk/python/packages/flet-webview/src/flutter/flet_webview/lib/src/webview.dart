import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'webview_mobile_and_mac.dart';
import 'webview_web.dart' if (dart.library.io) "webview_web_vain.dart";
import 'webview_windows_and_linux.dart'
    if (dart.library.html) "webview_windows_and_linux_vain.dart";

class WebViewControl extends StatelessWidget {
  final Control control;

  const WebViewControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${control.id}");
    Widget view =
        const ErrorControl("Webview is not yet supported on this platform.");
    if (isWebPlatform()) {
      view = WebviewWeb(control: control);
    } else if (isMobilePlatform() || isMacOSDesktop()) {
      view = WebviewMobileAndMac(control: control);
    } else if (isWindowsDesktop() || isLinuxDesktop()) {
      view = const WebviewDesktop();
    }

    return ConstrainedControl(control: control, child: view);
  }
}
