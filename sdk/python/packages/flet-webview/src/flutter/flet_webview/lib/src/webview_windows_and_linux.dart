import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:webview_all_linux/webview_all_linux.dart';
import 'package:webview_all_windows/webview_all_windows.dart';
import 'package:webview_platform_interface/webview_platform_interface.dart';

import 'utils/webview_desktop.dart';

/// WebView for Windows (WebView2) and Linux (WebKitGTK).
///
/// Built directly on `webview_platform_interface` rather than through the
/// `webview_all` umbrella, the same way [WebviewWeb] drives
/// `webview_flutter_web`'s platform classes. `WebViewPlatform.instance` is set
/// by Flutter's generated Dart plugin registrant, which calls
/// `WindowsWebViewPlatform.registerWith()` on Windows and
/// `LinuxWebViewPlatform.registerWith()` on Linux.
///
/// This file is compiled for every platform that has `dart:io` — Android and
/// the Apple platforms included — so it must not reference anything that fails
/// to compile there. It is only ever constructed on Windows and Linux.
class WebviewDesktop extends StatefulWidget {
  final Control control;

  const WebviewDesktop({super.key, required this.control});

  @override
  State<WebviewDesktop> createState() => _WebviewDesktopState();
}

class _WebviewDesktopState extends State<WebviewDesktop> {
  PlatformWebViewController? controller;
  PlatformWebViewWidget? _view;
  String? _initError;
  Future<void>? _ready;
  bool _alertHandlerRegistered = false;

  bool _shouldPreventNavigation(String url) {
    final links = widget.control.get<List>("prevent_links");
    if (links == null || links.isEmpty) return false;
    return links.any((link) => link is String && url.startsWith(link));
  }

  /// Creation params for the current desktop platform.
  ///
  /// Linux needs `allowFileAccessFromFileUrls` for pages opened with
  /// [loadFile]: WebKitGTK reads it once, when the document's security context
  /// is created, so it has to be set before the first load. Without it a local
  /// page still resolves sibling images, stylesheets and classic scripts, but
  /// `fetch`, XHR, ES modules, `@font-face` and `localStorage` all fail because
  /// the origin serialises as "null". `allowUniversalAccessFromFileUrls` stays
  /// off — it would give the local page access to every origin, http(s)
  /// included.
  PlatformWebViewControllerCreationParams _creationParams() {
    if (isLinuxDesktop()) {
      return const LinuxWebViewControllerCreationParams(
        allowFileAccessFromFileUrls: true,
        allowUniversalAccessFromFileUrls: false,
      );
    }
    return const PlatformWebViewControllerCreationParams();
  }

  /// Loads [url], routing `file:` URLs through
  /// [PlatformWebViewController.loadFile].
  ///
  /// Two different failures have to fall through to [loadRequest] here:
  /// [Uri.toFilePath] throws an [UnsupportedError] for a `file:` URL carrying a
  /// fragment, a query or a non-`localhost` authority, and — unlike the mobile
  /// controller, which throws [UnsupportedError] — both desktop controllers
  /// throw an [ArgumentError] for a relative or non-existent path.
  Future<void> _load(String url, LoadRequestMethod method) async {
    final c = controller;
    if (c == null) return;
    final uri = Uri.parse(url);
    if (uri.scheme == "file") {
      try {
        await c.loadFile(uri.toFilePath());
        return;
      } on UnsupportedError catch (e) {
        debugPrint("WebView: $url cannot be converted to a file path: $e");
      } on ArgumentError catch (e) {
        debugPrint("WebView: $url is not a valid local file path: $e");
      }
    }
    await c.loadRequest(LoadRequestParams(uri: uri, method: method));
  }

  /// Registers the navigation callbacks.
  ///
  /// Unlike `webview_flutter`, these are not constructor arguments: each one
  /// has its own async setter on the platform delegate.
  Future<void> _setNavigationDelegate(PlatformWebViewController c) async {
    final delegate = PlatformNavigationDelegate(
      const PlatformNavigationDelegateCreationParams(),
    );
    await delegate.setOnProgress((int progress) {
      widget.control.triggerEvent("progress", progress);
    });
    await delegate.setOnUrlChange((UrlChange change) {
      widget.control.triggerEvent("url_change", change.url);
    });
    await delegate.setOnPageStarted((String url) {
      widget.control.triggerEvent("page_started", url);
    });
    await delegate.setOnPageFinished((String url) {
      widget.control.triggerEvent("page_ended", url);
    });
    await delegate.setOnWebResourceError((WebResourceError error) {
      widget.control.triggerEvent("web_resource_error", error.description);
    });
    await delegate.setOnNavigationRequest((NavigationRequest request) {
      return _shouldPreventNavigation(request.url)
          ? NavigationDecision.prevent
          : NavigationDecision.navigate;
    });
    await c.setPlatformNavigationDelegate(delegate);
  }

  /// Registers the console and scroll handlers.
  ///
  /// These two are attached unconditionally and awaited before the first load,
  /// rather than lazily from `build` as the mobile implementation does: on
  /// Windows both bridges are installed once as document-start user scripts, so
  /// a handler attached after the first navigation would stay dead until the
  /// next one. Whether Python actually subscribed is checked inside each
  /// callback instead.
  ///
  /// The alert handler deliberately stays out of here — see
  /// [_setOptionalEventHandlers].
  Future<void> _setEventHandlers(PlatformWebViewController c) async {
    await c.setOnScrollPositionChange((ScrollPositionChange position) {
      if (!widget.control.hasEventHandler("scroll")) return;
      widget.control.triggerEvent("scroll", {"x": position.x, "y": position.y});
    });

    await c.setOnConsoleMessage((JavaScriptConsoleMessage message) {
      if (!widget.control.hasEventHandler("console_message")) return;
      widget.control.triggerEvent("console_message", {
        "message": message.message,
        "severity_level": message.level.name,
      });
    });
  }

  /// Registers the JavaScript alert handler, but only once Python subscribes.
  ///
  /// On Linux, *setting* this callback tells WebKitGTK that the app owns script
  /// dialogs, which suppresses the built-in one. Registering it unconditionally
  /// would therefore make every `window.alert()` vanish for apps that never
  /// asked to handle alerts — the page would continue as though the user had
  /// dismissed it. Attaching lazily, as the mobile implementation does, keeps
  /// the native dialog for apps with no handler.
  void _setOptionalEventHandlers() {
    final c = controller;
    if (c == null || _alertHandlerRegistered) return;
    if (!widget.control.hasEventHandler("javascript_alert_dialog")) return;
    _alertHandlerRegistered = true;
    c.setOnJavaScriptAlertDialog((JavaScriptAlertDialogRequest request) async {
      widget.control.triggerEvent(
        "javascript_alert_dialog",
        {"message": request.message, "url": request.url},
      );
    }).catchError((Object e) {
      _alertHandlerRegistered = false;
      debugPrint("WebView.on_javascript_alert_dialog is not available: $e");
    });
  }

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);

    if (WebViewPlatform.instance == null) {
      _initError = "WebView platform implementation was not registered.";
      return;
    }

    final c = PlatformWebViewController(_creationParams());
    controller = c;
    _view = PlatformWebViewWidget(
      PlatformWebViewWidgetCreationParams(controller: c),
    );

    _ready = () async {
      await _setNavigationDelegate(c);
      await _setEventHandlers(c);
      await c.setJavaScriptMode(JavaScriptMode.unrestricted);
      await _load(
        widget.control.getString("url", "https://flet.dev")!,
        parseDesktopLoadRequestMethod(
            widget.control.getString("method"), LoadRequestMethod.get)!,
      );
    }();
    // Attaching a listener marks the error as handled; `_invokeMethod` still
    // awaits the original future and rethrows it to Python.
    _ready!.catchError((Object e) {
      debugPrint("WebView initialization failed: $e");
    });
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("WebView.$name($args)");
    final c = controller;
    if (c == null) {
      throw Exception("WebView is not available on this platform.");
    }
    // A method invoked right after `page.add()` would otherwise race the
    // initial `url` load and be overwritten by it.
    await _ready;
    switch (name) {
      case "reload":
        await c.reload();
        break;
      case "can_go_back":
        return c.canGoBack();
      case "can_go_forward":
        return c.canGoForward();
      case "go_back":
        if (await c.canGoBack()) {
          await c.goBack();
        }
        break;
      case "go_forward":
        if (await c.canGoForward()) {
          await c.goForward();
        }
        break;
      case "enable_zoom":
        await c.enableZoom(true);
        break;
      case "disable_zoom":
        await c.enableZoom(false);
        break;
      case "clear_cache":
        await c.clearCache();
        break;
      case "clear_local_storage":
        await c.clearLocalStorage();
        break;
      case "get_current_url":
        return await c.currentUrl();
      case "get_title":
        return await c.getTitle();
      case "get_user_agent":
        return await c.getUserAgent();
      case "load_file":
        await c.loadFile(args["path"]);
        break;
      case "load_html":
        await c.loadHtmlString(args["value"], baseUrl: args["base_url"]);
        break;
      case "load_request":
        var url = args["url"];
        if (url != null) {
          await _load(
              url,
              parseDesktopLoadRequestMethod(
                  args["method"], LoadRequestMethod.get)!);
        }
        break;
      case "run_javascript":
        var javascript = args["value"];
        if (javascript != null) {
          await c.runJavaScript(javascript);
        }
        break;
      case "scroll_to":
        var x = parseInt(args["x"]);
        var y = parseInt(args["y"]);
        if (x != null && y != null) {
          await c.scrollTo(x, y);
        }
        break;
      case "scroll_by":
        var x = parseInt(args["x"]);
        var y = parseInt(args["y"]);
        if (x != null && y != null) {
          await c.scrollBy(x, y);
        }
        break;
      case "set_javascript_mode":
        var mode = parseDesktopJavaScriptMode(args["mode"]);
        if (mode != null) {
          await c.setJavaScriptMode(mode);
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
    // Dropping the widget does not release the native WebView: Windows leaks a
    // browser and renderer process set per undisposed controller, Linux a
    // GtkWidget plus a WebKit web process. `dispose` is not on the platform
    // interface, so it has to be reached through the concrete controller, and
    // it rethrows a failed initialization — which must not escape as an
    // unhandled async error while a route is being popped.
    final c = controller;
    Future<void>? disposed;
    if (c is WindowsWebViewController) {
      disposed = c.dispose();
    } else if (c is LinuxWebViewController) {
      disposed = c.dispose();
    }
    disposed?.catchError((Object e) {
      debugPrint("WebView disposal failed: $e");
    });
    controller = null;
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${widget.control.id}");
    final view = _view;
    if (view == null) {
      return ErrorControl(_initError ?? "WebView could not be created.");
    }

    _setOptionalEventHandlers();

    var bgcolor = widget.control.getColor("bgcolor", context);
    if (bgcolor != null) {
      controller?.setBackgroundColor(bgcolor).catchError((Object e) {
        debugPrint("WebView.bgcolor could not be applied: $e");
      });
    }
    return view.build(context);
  }
}
