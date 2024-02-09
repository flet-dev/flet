import 'dart:io' show Platform;
import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

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

    Widget? result;

    String url = control.attrString("url", "")!;
    if (url == "") {
      return const ErrorControl("WebView.url cannot be empty.");
    }

    bool javascriptEnabled = control.attrBool("javascriptEnabled", false)!;
    var bgcolor = HexColor.fromString(
        Theme.of(context), control.attrString("bgcolor", "")!);
    String preventLink = control.attrString("preventLink", "")!;

    if (Platform.isIOS || Platform.isAndroid) {
      var controller = WebViewController()
        ..setJavaScriptMode(javascriptEnabled
            ? JavaScriptMode.unrestricted
            : JavaScriptMode.disabled)
        ..setNavigationDelegate(
          NavigationDelegate(
            onProgress: (int progress) {},
            onPageStarted: (String url) {
              backend.triggerControlEvent(control.id, "page_started", url);
            },
            onPageFinished: (String url) {
              backend.triggerControlEvent(control.id, "page_ended", url);
            },
            onWebResourceError: (WebResourceError error) {
              backend.triggerControlEvent(
                  control.id, "web_resource_error", error.toString());
            },
            onNavigationRequest: (NavigationRequest request) {
              if (preventLink != "" && request.url.startsWith(preventLink)) {
                return NavigationDecision.prevent;
              }
              return NavigationDecision.navigate;
            },
          ),
        );
      if (bgcolor != null) {
        controller.setBackgroundColor(bgcolor);
      }
      controller.loadRequest(Uri.parse(url));
      result = WebViewWidget(controller: controller);
    } else {
      result = const ErrorControl(
          "WebView control is not supported on this platform yet.");
    }

    return constrainedControl(context, result, parent, control);
  }
}
