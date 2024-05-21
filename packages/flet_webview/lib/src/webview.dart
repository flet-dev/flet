import 'dart:io' show Platform;
import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:webview_windows/webview_windows.dart' as web_windows;

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
  web_windows.WebviewController winController = web_windows.WebviewController();
  bool windowsWebInitialized = false;
  Widget? result;
  Color? bgcolor;
  String url = "";

  @override
  void initState() {
    super.initState();

    url = widget.control.attrString("url", "")!;
    if (url == "") {
      result = const ErrorControl("WebView.url cannot be empty.");
    }

    if (Platform.isWindows) {
      winController.initialize().then((value) {
        winController.loadingState.listen((event) {
          if (event == web_windows.LoadingState.loading) {
            widget.backend
                .triggerControlEvent(widget.control.id, "page_started", url);
          } else if (event == web_windows.LoadingState.navigationCompleted) {
            widget.backend
                .triggerControlEvent(widget.control.id, "page_ended", url);
          }
        });
        winController.onLoadError.listen((error) {
          widget.backend.triggerControlEvent(
              widget.control.id, "web_resource_error", error.toString());
        });
        winController.loadUrl(url);
        setState(() {
          windowsWebInitialized = true;
        });
      });
    }
    debugPrint("WebViewControl Initialized: ${widget.control.id}");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${widget.control.id}");

    if (result != null) {
      return result!;
    }

    bgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgcolor", "")!);

    bool javascriptEnabled =
        widget.control.attrBool("javascriptEnabled", false)!;
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
        controller.setBackgroundColor(bgcolor!);
      }
      controller.loadRequest(Uri.parse(url));

      return constrainedControl(context, WebViewWidget(controller: controller),
          widget.parent, widget.control);
    } else if (Platform.isWindows) {
      winController.setBackgroundColor(bgcolor ?? Colors.transparent);
      return Visibility(
        visible: windowsWebInitialized,
        replacement: constrainedControl(
            context,
            Container(
              color: bgcolor,
            ),
            widget.parent,
            widget.control),
        child: constrainedControl(context, web_windows.Webview(winController),
            widget.parent, widget.control),
      );
    } else {
      result = const ErrorControl(
          "WebView control is not supported on this platform yet.");

      return constrainedControl(
          context, result!, widget.parent, widget.control);
    }
  }

  @override
  void dispose() {
    // Dispose of the web view controller for Windows if initialized
    if (Platform.isWindows && windowsWebInitialized) {
      winController.dispose();
    }

    // You might also need to dispose other controllers or streams
    // if they are being used on other platforms or in other scenarios.

    super.dispose();
  }
}
