import 'dart:io' show Platform;
import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class WebViewControl extends StatefulWidget {
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
  State<WebViewControl> createState() => _WebViewControlState();
}

class _WebViewControlState extends State<WebViewControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${widget.control.id}");

    Widget? result;

    String url = widget.control.attrString("url", "")!;
    if (url == "") {
      return const ErrorControl("WebView.url cannot be empty.");
    }

    bool javascriptEnabled =
        widget.control.attrBool("javascriptEnabled", false)!;
    var bgcolor =
        parseColor(Theme.of(context), widget.control.attrString("bgcolor"));
    String preventLink = widget.control.attrString("preventLink", "")!;

    if (Platform.isIOS || Platform.isAndroid) {
      var controller = WebViewController()
        ..setJavaScriptMode(javascriptEnabled
            ? JavaScriptMode.unrestricted
            : JavaScriptMode.disabled)
        ..setNavigationDelegate(
          NavigationDelegate(
            onProgress: (int progress) {},
            onPageStarted: (String url) {
              widget.backend
                  .triggerControlEvent(widget.control.id, "page_started", url);
            },
            onPageFinished: (String url) {
              widget.backend
                  .triggerControlEvent(widget.control.id, "page_ended", url);
            },
            onWebResourceError: (WebResourceError error) {
              widget.backend.triggerControlEvent(
                  widget.control.id, "web_resource_error", error.toString());
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

    return constrainedControl(context, result, widget.parent, widget.control);
  }
}
