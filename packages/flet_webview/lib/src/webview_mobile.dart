import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class WebviewMobile extends StatefulWidget {
  final Control control;
  final FletControlBackend backend;

  const WebviewMobile(
      {super.key, required this.control, required this.backend});

  @override
  State<WebviewMobile> createState() => _WebviewMobileState();
}

class _WebviewMobileState extends State<WebviewMobile> {
  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${widget.control.id}");
    var params = const PlatformWebViewControllerCreationParams();
    final WebViewController controller =
        WebViewController.fromPlatformCreationParams(params);

    var preventLink = widget.control.attrString("preventLink")?.trim();
    var enableJavascript = widget.control.attrBool("enableJavascript") ??
        widget.control.attrBool(
            "javascriptEnabled", false)!; // javascriptEnabled is DEPRECATED
    var bgcolor =
        parseColor(Theme.of(context), widget.control.attrString("bgcolor"));
    if (bgcolor != null) {
      controller.setBackgroundColor(bgcolor);
    }
    controller
      ..setJavaScriptMode(enableJavascript
          ? JavaScriptMode.unrestricted
          : JavaScriptMode.disabled)
      ..setNavigationDelegate(
        NavigationDelegate(
          onProgress: (int progress) {
            debugPrint('WebViewControl is loading (progress : $progress%)');
            widget.backend.triggerControlEvent(
                widget.control.id, "progress", progress.toString());
          },
          onUrlChange: (UrlChange url) {
            debugPrint('WebViewControl URL changed: ${url.url}');
            widget.backend.triggerControlEvent(
                widget.control.id, "url_change", url.url ?? "");
          },
          onPageStarted: (String url) {
            debugPrint('WebViewControl page started loading: $url');
            widget.backend
                .triggerControlEvent(widget.control.id, "page_started", url);
          },
          onPageFinished: (String url) {
            debugPrint('WebViewControl page finished loading: $url');
            widget.backend
                .triggerControlEvent(widget.control.id, "page_ended", url);
          },
          onWebResourceError: (WebResourceError error) {
            debugPrint('''
Page resource error:
  code: ${error.errorCode}
  description: ${error.description}
  errorType: ${error.errorType}
  isForMainFrame: ${error.isForMainFrame}
          ''');
            widget.backend.triggerControlEvent(widget.control.id,
                "web_resource_error", "WebView error: ${error.description}");
          },
          onNavigationRequest: (NavigationRequest request) {
            if (preventLink != null && request.url.startsWith(preventLink)) {
              return NavigationDecision.prevent;
            }
            return NavigationDecision.navigate;
          },
        ),
      )
      ..addJavaScriptChannel(
        'Toaster',
        onMessageReceived: (JavaScriptMessage message) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(message.message)),
          );
        },
      )
      ..loadRequest(
          Uri.parse(widget.control.attrString("url", "https://flet.dev")!));

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "reload":
            await controller.reload();
            break;
          case "can_go_back":
            return await controller.canGoBack().toString();
          case "can_go_forward":
            return await controller.canGoForward().toString();
          case "go_back":
            if (await controller.canGoBack()) {
              await controller.goBack();
            }
          case "go_forward":
            if (await controller.canGoForward()) {
              await controller.goForward();
            }
            break;
        }
        return null;
      });
    }();

    return WebViewWidget(controller: controller);
  }
}
