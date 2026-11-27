import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:webview_flutter_platform_interface/webview_flutter_platform_interface.dart';
import 'package:webview_flutter_web/webview_flutter_web.dart';

/// On web a `WebView` is an `<iframe>` in the app's own page.
///
/// - A URL whose scheme [isOpenableWebUrl] rejects isn't loaded: a
///   `javascript:` URL, or a `blob:` URL the app made, would run with the
///   page's own origin.
/// - In an app embedded with `FletApp`, the frame is sandboxed without
///   `allow-same-origin`: whatever it shows, even a page from the host's own
///   site, runs with an opaque origin, apart from the host's page.
class WebviewWeb extends StatefulWidget {
  final Control control;

  const WebviewWeb({super.key, required this.control});

  @override
  State<WebviewWeb> createState() => _WebviewWebState();
}

/// What an embedded app's frame may do: run scripts, submit forms, open
/// popups and show dialogs - not use its real origin, and not navigate the
/// host's page.
const _embeddedSandbox = "allow-scripts allow-forms allow-popups "
    "allow-popups-to-escape-sandbox allow-modals allow-downloads "
    "allow-presentation";

class _WebviewWebState extends State<WebviewWeb> {
  late PlatformWebViewController controller;
  @override
  void initState() {
    super.initState();
    WebViewPlatform.instance = WebWebViewPlatform();

    controller = PlatformWebViewController(
      const PlatformWebViewControllerCreationParams(),
    );
    if (widget.control.backend.isEmbedded) {
      // The plugin offers no other way to reach its iframe; it's pinned to an
      // exact version in pubspec.yaml, so this field can't move under us.
      var params = controller.params as WebWebViewControllerCreationParams;
      // ignore: invalid_use_of_visible_for_testing_member
      params.iFrame.setAttribute("sandbox", _embeddedSandbox);
    }
    var url = widget.control.getString("url", "https://flet.dev")!;
    if (isOpenableWebUrl(url)) {
      controller.loadRequest(LoadRequestParams(uri: Uri.parse(url)));
    } else {
      debugPrint("WebView: not loading $url: its scheme can't be loaded on web.");
    }
  }

  @override
  Widget build(BuildContext context) {
    return PlatformWebViewWidget(
      PlatformWebViewWidgetCreationParams(controller: controller),
    ).build(context);
  }
}
