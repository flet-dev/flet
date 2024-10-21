import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flet_webview/src/utils/webview.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class WebviewMobileAndMac extends StatefulWidget {
  final Control control;
  final FletControlBackend backend;
  final Color? bgcolor;

  const WebviewMobileAndMac(
      {super.key, required this.control, required this.backend, this.bgcolor});

  @override
  State<WebviewMobileAndMac> createState() => _WebviewMobileAndMacState();
}

class _WebviewMobileAndMacState extends State<WebviewMobileAndMac> {
  late WebViewController controller;

  @override
  void initState() {
    super.initState();

    var params = const PlatformWebViewControllerCreationParams();
    controller = WebViewController.fromPlatformCreationParams(params);

    var preventLink = widget.control.attrString("preventLink")?.trim();
    if (widget.bgcolor != null) {
      controller.setBackgroundColor(widget.bgcolor!);
    }

    controller.setNavigationDelegate(
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
          widget.backend.triggerControlEvent(widget.control.id,
              "web_resource_error", "WebView error: ${error.description}");
        },
        onNavigationRequest: (NavigationRequest request) {
          if (preventLink != null && request.url.startsWith(preventLink!)) {
            return NavigationDecision.prevent;
          }
          return NavigationDecision.navigate;
        },
      ),
    );

    controller.loadRequest(
        Uri.parse(widget.control.attrString("url", "https://flet.dev")!),
        method: parseLoadRequestMethod(
            widget.control.attrString("method"), LoadRequestMethod.get)!);
    controller.setOnScrollPositionChange((ScrollPositionChange position) {
      widget.backend.triggerControlEvent(
          widget.control.id,
          "scroll",
          jsonEncode({
            "x": position.x.toString(),
            "y": position.y.toString(),
          }));
    });
    controller.setOnConsoleMessage((JavaScriptConsoleMessage message) {
      widget.backend.triggerControlEvent(
          widget.control.id,
          "console_message",
          jsonEncode({
            "message": message.message,
            "level": message.level.name,
          }));
    });
    controller.setOnJavaScriptAlertDialog(
        (JavaScriptAlertDialogRequest request) async {
      widget.backend.triggerControlEvent(
          widget.control.id,
          "javascript_alert_dialog",
          jsonEncode({
            "message": request.message,
            "url": request.url,
          }));
    });

    // Subscribe to backend methods
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
          break;
        case "go_forward":
          if (await controller.canGoForward()) {
            await controller.goForward();
          }
          break;
        case "enable_zoom":
          await controller.enableZoom(true);
          break;
        case "disable_zoom":
          await controller.enableZoom(false);
          break;
        case "clear_cache":
          await controller.clearCache();
          break;
        case "clear_local_storage":
          await controller.clearLocalStorage();
          break;
        case "get_current_url":
          return await controller.currentUrl();
        case "get_title":
          return await controller.getTitle();
        case "get_user_agent":
          return await controller.getUserAgent();
        case "load_file":
          var path = args["path"];
          if (path != null) {
            await controller.loadFile(path);
          }
          break;
        case "load_html":
          var html = args["value"];
          if (html != null) {
            await controller.loadHtmlString(html, baseUrl: args["base_url"]);
          }
          break;
        case "load_request":
          var url = args["url"];
          if (url != null) {
            await controller.loadRequest(Uri.parse(url),
                method: parseLoadRequestMethod(
                    args["method"], LoadRequestMethod.get)!);
          }
          break;
        case "run_javascript":
          var javascript = args["value"];
          if (javascript != null) {
            await controller.runJavaScript(javascript);
          }
          break;
        case "scroll_to":
          var x = parseInt(args["x"]);
          var y = parseInt(args["y"]);
          if (x != null && y != null) {
            await controller.scrollTo(x, y);
          }
          break;
        case "scroll_by":
          var x = parseInt(args["x"]);
          var y = parseInt(args["y"]);
          if (x != null && y != null) {
            await controller.scrollBy(x, y);
          }
          break;
        case "set_javascript_mode":
          var value = parseBool(args["value"]);
          if (value != null) {
            await controller.setJavaScriptMode(
                value ? JavaScriptMode.unrestricted : JavaScriptMode.disabled);
          }
          break;
      }
      return null;
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${widget.control.id}");

    return WebViewWidget(controller: controller);
  }
}
