import 'dart:io' show Platform;
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateless_mixin.dart';

class WebViewControl extends StatelessWidget with FletControlStatelessMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const WebViewControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.parentDisabled});

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
              sendControlEvent(context, control.id, "page_started", url);
            },
            onPageFinished: (String url) {
              sendControlEvent(context, control.id, "page_ended", url);
            },
            onWebResourceError: (WebResourceError error) {
              sendControlEvent(
                  context, control.id, "web_resource_error", error.toString());
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
