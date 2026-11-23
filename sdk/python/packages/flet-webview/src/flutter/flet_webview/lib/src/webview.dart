import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:webview_all/webview_all.dart';

import 'utils/platform_controller_vain.dart'
    if (dart.library.io) 'utils/platform_controller.dart';
import 'utils/webview.dart';

/// WebView for every platform, on top of the app-facing `webview_all` API.
///
/// The platform implementation (Android WebView, WKWebView, Edge WebView2,
/// WebKitGTK or an iframe on the web) is registered by Flutter's generated
/// plugin registrant.
class WebViewControl extends StatefulWidget {
  final Control control;

  const WebViewControl({super.key, required this.control});

  @override
  State<WebViewControl> createState() => _WebViewControlState();
}

class _WebViewControlState extends State<WebViewControl> {
  WebViewController? _controller;

  /// Completes once the handlers are attached and the initial `url` load has
  /// started, or initialization has failed.
  ///
  /// Invoked methods await it, so that a method called right after the
  /// control is added is not overwritten by the initial load. It never
  /// completes with an error: a failed initialization is logged instead, so
  /// that it cannot make every later method call fail with the same error.
  Future<void>? _ready;
  bool _initialized = false;

  /// The last property update, which each update waits for, so that updates
  /// are applied in order and a method call sees the latest one.
  Future<void> _propertiesApplied = Future.value();

  /// The `url` value last loaded.
  String? _url;
  bool? _navigationRequestsEnabled;
  bool _scrollHandlerRegistered = false;
  bool _consoleHandlerRegistered = false;
  bool _alertHandlerRegistered = false;
  Color? _bgcolor;

  List<String> get _preventLinks =>
      widget.control.get<List>("prevent_links")?.whereType<String>().toList() ??
      const [];

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
    if (WebViewPlatform.instance == null) return;

    final controller = WebViewController.fromPlatformCreationParams(
      createPlatformCreationParams(),
    );
    _controller = controller;
    _ready = _initialize(controller)
        .catchError((Object e) {
          debugPrint("WebView initialization failed: $e");
        })
        .whenComplete(() {
          if (mounted) setState(() => _initialized = true);
        });
  }

  /// Attaches the delegate and handlers, then starts loading `url`.
  ///
  /// The handlers Python subscribed to are attached before the first load:
  /// the console bridge on Windows, iOS and macOS, and the scroll bridge on
  /// Windows, are scripts injected as each document is created, so they only
  /// reach documents loaded after they are added.
  ///
  /// On macOS, zoom is explicitly turned off first: WKWebView starts with
  /// magnification off while the controller assumes zoom is on, which would
  /// turn the first `enableZoom(true)` into a no-op.
  ///
  /// JavaScript is enabled before the first load because Android's
  /// `WebSettings.javaScriptEnabled` defaults to `false`, unlike every other
  /// platform. `set_javascript_mode` can turn it back off.
  ///
  /// A `url` that cannot be loaded is reported with `on_web_resource_error`.
  Future<void> _initialize(WebViewController controller) async {
    await _applyProperties(controller);
    if (isMacOSDesktop()) {
      await controller.enableZoom(false);
    }
    await controller.setJavaScriptMode(JavaScriptMode.unrestricted);
    await _loadUrl(
      controller,
      widget.control.getString("url", "https://flet.dev")!,
    );
  }

  /// Loads the `url` property value [url] and reports a failure with
  /// `on_web_resource_error`.
  Future<void> _loadUrl(WebViewController controller, String url) async {
    _url = url;
    try {
      await _load(controller, url, LoadRequestMethod.get);
    } catch (e) {
      widget.control.triggerEvent(
        "web_resource_error",
        "Could not load $url: $e",
      );
    }
  }

  /// Applies `prevent_links`, the event subscriptions and, once the initial
  /// load has started, a changed `url` to [controller].
  ///
  /// Each call runs after the previous one, and failures are logged or
  /// reported, so the returned future never completes with an error.
  Future<void> _applyProperties(WebViewController controller) {
    return _propertiesApplied = _propertiesApplied.then((_) async {
      try {
        await _updateNavigationDelegate(controller);
      } catch (e) {
        debugPrint("WebView.prevent_links could not be applied: $e");
      }
      await _updateEventHandlers(controller);
      final url = widget.control.getString("url");
      if (_url != null && url != null && url != _url) {
        await _loadUrl(controller, url);
      }
    });
  }

  /// Sets a navigation delegate that intercepts navigation requests only
  /// while `prevent_links` is not empty.
  ///
  /// On Windows an intercepted navigation is cancelled and, once allowed,
  /// started again as a plain GET, which drops the body of a submitted form.
  ///
  /// A certificate error is reported with `on_web_resource_error`, and the
  /// load is cancelled.
  Future<void> _updateNavigationDelegate(WebViewController controller) async {
    final enabled = _preventLinks.isNotEmpty;
    if (enabled == _navigationRequestsEnabled) return;
    _navigationRequestsEnabled = enabled;
    try {
      await controller.setNavigationDelegate(
        NavigationDelegate(
          onProgress: (progress) =>
              widget.control.triggerEvent("progress", progress),
          onUrlChange: (change) =>
              widget.control.triggerEvent("url_change", change.url),
          onPageStarted: (url) =>
              widget.control.triggerEvent("page_started", url),
          onPageFinished: (url) =>
              widget.control.triggerEvent("page_ended", url),
          onWebResourceError: (error) => widget.control.triggerEvent(
            "web_resource_error",
            error.description,
          ),
          onSslAuthError: (error) {
            widget.control.triggerEvent(
              "web_resource_error",
              error.platform.description,
            );
            error.cancel();
          },
          onNavigationRequest: enabled
              ? (request) =>
                    _preventLinks.any((link) => request.url.startsWith(link))
                    ? NavigationDecision.prevent
                    : NavigationDecision.navigate
              : null,
        ),
      );
    } catch (e) {
      _navigationRequestsEnabled = null;
      rethrow;
    }
  }

  /// Attaches the handlers of the events Python subscribed to.
  ///
  /// The alert handler in particular must stay unset until then: setting it
  /// tells Android, WebKitGTK and the web implementation that the app shows
  /// alerts itself, which suppresses their built-in dialog. The scroll handler
  /// is skipped on macOS, where WKWebView reports no scroll position, and is
  /// removed again when Python unsubscribes, since observing scrolling costs
  /// a listener in every page.
  ///
  /// A handler that fails to attach is logged rather than rethrown, so that it
  /// cannot keep the initial `url` from loading.
  Future<void> _updateEventHandlers(WebViewController controller) async {
    final scroll =
        !isMacOSDesktop() && widget.control.hasEventHandler("scroll");
    if (scroll != _scrollHandlerRegistered) {
      _scrollHandlerRegistered = scroll;
      await _attachHandler(
        "scroll",
        () => controller.setOnScrollPositionChange(
          scroll
              ? (position) {
                  widget.control.triggerEvent("scroll", {
                    "x": position.x,
                    "y": position.y,
                  });
                }
              : null,
        ),
      );
    }
    if (!_consoleHandlerRegistered &&
        widget.control.hasEventHandler("console_message")) {
      _consoleHandlerRegistered = true;
      retainJavaScriptChannelCallbacks();
      await _attachHandler(
        "console_message",
        () => controller.setOnConsoleMessage((message) {
          widget.control.triggerEvent("console_message", {
            "message": message.message,
            "severity_level": message.level.name,
          });
        }),
      );
    }
    if (!_alertHandlerRegistered &&
        widget.control.hasEventHandler("javascript_alert_dialog")) {
      _alertHandlerRegistered = true;
      await _attachHandler(
        "javascript_alert_dialog",
        () => controller.setOnJavaScriptAlertDialog((request) async {
          widget.control.triggerEvent("javascript_alert_dialog", {
            "message": request.message,
            "url": request.url,
          });
        }),
      );
    }
  }

  Future<void> _attachHandler(
    String event,
    Future<void> Function() attach,
  ) async {
    try {
      await attach();
    } catch (e) {
      debugPrint("WebView.on_$event is not available on this platform: $e");
    }
  }

  /// Loads [url], routing `file:` URLs through [loadLocalFile].
  ///
  /// `loadFile` is the only entry point that grants the webview access to the
  /// local filesystem: on Android it enables `WebSettings.allowFileAccess`,
  /// which defaults to `false` when targeting API 30+, and on iOS/macOS it
  /// grants read access to the file's directory so that sibling assets
  /// resolve too.
  ///
  /// A `file:` URL falls through to [WebViewController.loadRequest] when
  /// [Uri.toFilePath] rejects it with an [UnsupportedError] (a query, a
  /// fragment or, outside Windows, any authority), or when [loadLocalFile]
  /// throws an [ArgumentError] for a relative or missing path on Windows or
  /// Linux. The web has no local files.
  ///
  /// A [url] matching `prevent_links` is not loaded. The navigation delegate
  /// does not see these loads on Android, where `loadUrl` skips
  /// `shouldOverrideUrlLoading`.
  Future<void> _load(
    WebViewController controller,
    String url,
    LoadRequestMethod method,
  ) async {
    if (_preventLinks.any(url.startsWith)) return;
    final uri = Uri.parse(url);
    if (uri.scheme == "file" && !kIsWeb) {
      try {
        await loadLocalFile(controller, uri.toFilePath());
        return;
      } on UnsupportedError catch (e) {
        debugPrint("WebView: $url is not a loadable local file: $e");
      } on ArgumentError catch (e) {
        debugPrint("WebView: $url is not a valid local file path: $e");
      }
    }
    await controller.loadRequest(uri, method: method);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("WebView.$name($args)");
    final controller = _controller;
    if (controller == null) {
      throw Exception("WebView is not available on this platform.");
    }
    await _ready;
    if (!mounted) {
      throw Exception("WebView was removed from the page.");
    }
    await _applyProperties(controller);
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
        return controller.currentUrl();
      case "get_title":
        return controller.getTitle();
      case "get_user_agent":
        return controller.getUserAgent();
      case "load_file":
        await loadLocalFile(controller, args["path"]);
        break;
      case "load_html":
        var baseUrl = args["base_url"];
        if (baseUrl != null && Uri.tryParse(baseUrl)?.scheme == "file") {
          await allowFileAccess(controller);
        }
        await controller.loadHtmlString(args["value"], baseUrl: baseUrl);
        break;
      case "load_request":
        var url = args["url"];
        if (url != null) {
          await _load(
            controller,
            url,
            parseLoadRequestMethod(args["method"], LoadRequestMethod.get)!,
          );
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
    final controller = _controller;
    if (controller != null) {
      disposePlatformController(controller).catchError((Object e) {
        debugPrint("WebView disposal failed: $e");
      });
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${widget.control.id}");
    final controller = _controller;
    if (controller == null) {
      return LayoutControl(
        control: widget.control,
        child: const ErrorControl(
          "WebView is not supported on this platform or in this build.",
        ),
      );
    }

    if (_initialized) {
      _applyProperties(controller);
    }

    var bgcolor = widget.control.getColor("bgcolor", context);
    if (bgcolor != null && bgcolor != _bgcolor) {
      _bgcolor = bgcolor;
      controller.setBackgroundColor(bgcolor).catchError((Object e) {
        debugPrint("WebView.bgcolor could not be applied: $e");
      });
    }

    return LayoutControl(
      control: widget.control,
      child: WebViewWidget(controller: controller),
    );
  }
}
