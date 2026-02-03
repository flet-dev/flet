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
  bool _scrollHandlerRegistered = false;
  bool _consoleHandlerRegistered = false;
  bool _alertHandlerRegistered = false;

  bool _shouldPreventNavigation(String url) {
    final links = widget.control.get<List>("prevent_links");
    if (links == null || links.isEmpty) return false;
    return links.any((link) => link is String && url.startsWith(link));
  }

  void _setOptionalEventHandlers() {
    // macOS currently does not surface scroll callbacks via webview_flutter.
    if (!isMacOSDesktop() &&
        !_scrollHandlerRegistered &&
        widget.control.hasEventHandler("scroll")) {
      try {
        controller.setOnScrollPositionChange((ScrollPositionChange position) {
          widget.control
              .triggerEvent("scroll", {"x": position.x, "y": position.y});
        });
        _scrollHandlerRegistered = true;
      } catch (e) {
        debugPrint("WebView.on_scroll is not available on this platform: $e");
      }
    }

    if (!_consoleHandlerRegistered &&
        widget.control.hasEventHandler("console_message")) {
      try {
        controller.setOnConsoleMessage((JavaScriptConsoleMessage message) {
          widget.control.triggerEvent("console_message", {
            "message": message.message,
            "severity_level": message.level.name,
          });
        });
        _consoleHandlerRegistered = true;
      } catch (e) {
        debugPrint(
            "WebView.on_console_message is not available on this platform: $e");
      }
    }

    if (!_alertHandlerRegistered &&
        widget.control.hasEventHandler("javascript_alert_dialog")) {
      try {
        controller.setOnJavaScriptAlertDialog(
            (JavaScriptAlertDialogRequest request) async {
          widget.control.triggerEvent(
            "javascript_alert_dialog",
            {"message": request.message, "url": request.url},
          );
        });
        _alertHandlerRegistered = true;
      } catch (e) {
        debugPrint(
            "WebView.on_javascript_alert_dialog is not available on this platform: $e");
      }
    }
  }

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
          return _shouldPreventNavigation(request.url)
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

    _setOptionalEventHandlers();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("WebView.$name($args)");
    switch (name) {
      case "reload":
        await controller.reload();
        break;
      case "can_go_back":
        return controller.canGoBack();
      case "can_go_forward":
        return controller.canGoForward();
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

    _setOptionalEventHandlers();

    var bgcolor = widget.control.getColor("bgcolor", context);

    if (bgcolor != null) {
      controller.setBackgroundColor(bgcolor);
    }
    return WebViewWidget(controller: controller);
  }
}
