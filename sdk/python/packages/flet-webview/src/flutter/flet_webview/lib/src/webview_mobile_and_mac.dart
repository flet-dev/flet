import 'package:flet/flet.dart';
import 'package:flet_webview/src/utils/webview.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class WebviewMobileAndMac extends StatefulWidget {
  final Control control;

  const WebviewMobileAndMac({super.key, required this.control});

  @override
  State<WebviewMobileAndMac> createState() => _WebviewMobileAndMacState();
}

class _WebviewMobileAndMacState extends State<WebviewMobileAndMac> {
  late WebViewController controller;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);

    var params = const PlatformWebViewControllerCreationParams();
    controller = WebViewController.fromPlatformCreationParams(params);

    controller.setNavigationDelegate(
      NavigationDelegate(
        onProgress: (int progress) {
          widget.control.triggerEvent("progress", progress);
        },
        onUrlChange: (UrlChange url) {
          widget.control.triggerEvent("url_change", url.url);
        },
        onPageStarted: (String url) {
          widget.control.triggerEvent("page_started", url);
        },
        onPageFinished: (String url) {
          widget.control.triggerEvent("page_ended", url);
        },
        onWebResourceError: (WebResourceError error) {
          widget.control.triggerEvent("web_resource_error", error.description);
        },
        onNavigationRequest: (NavigationRequest request) {
          var links = widget.control.get("prevent_link");
          var prevent = links is List &&
              links.isNotEmpty &&
              links.any((l) => request.url.startsWith(l));
          return prevent
              ? NavigationDecision.prevent
              : NavigationDecision.navigate;
        },
      ),
    );

    // request
    controller.loadRequest(
        Uri.parse(widget.control.getString("url", "https://flet.dev")!),
        method: parseLoadRequestMethod(
            widget.control.getString("method"), LoadRequestMethod.get)!);

    // scroll
    if (!isMacOSDesktop()) {
      controller.setOnScrollPositionChange((ScrollPositionChange position) {
        widget.control
            .triggerEvent("scroll", {"x": position.x, "y": position.y});
      });
    }

    // console
    controller.setOnConsoleMessage((JavaScriptConsoleMessage message) {
      widget.control.triggerEvent("console_message",
          {"message": message.message, "level": message.level.name});
    });

    // alert
    controller.setOnJavaScriptAlertDialog(
        (JavaScriptAlertDialogRequest request) async {
      widget.control.triggerEvent("javascript_alert_dialog",
          {"message": request.message, "url": request.url});
    });
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("WebView.$name($args)");
    switch (name) {
      case "reload":
        await controller.reload();
        break;
      case "can_go_back":
        return controller.canGoBack().toString();
      case "can_go_forward":
        return controller.canGoForward().toString();
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
        await controller.loadFile(args["path"]);
        break;
      case "load_html":
        await controller.loadHtmlString(args["value"],
            baseUrl: args["base_url"]);
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
        var mode = parseJavaScriptMode(args["mode"]);
        if (mode != null) {
          await controller.setJavaScriptMode(mode);
        }
        break;
      default:
        throw Exception("Unknown WebView method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("WebViewControl dispose: ${widget.control.id}");
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${widget.control.id}");

    var bgcolor = widget.control.getColor("bgcolor", context);

    if (bgcolor != null) {
      controller.setBackgroundColor(bgcolor);
    }
    return WebViewWidget(controller: controller);
  }
}
