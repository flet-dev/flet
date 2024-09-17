import 'package:flutter/material.dart';
import 'package:webview_flutter_platform_interface/webview_flutter_platform_interface.dart';
import 'package:webview_flutter_web/webview_flutter_web.dart';

class WebviewWeb extends StatefulWidget {
  final String url;

  const WebviewWeb({Key? key, required this.url}) : super(key: key);

  @override
  State<WebviewWeb> createState() => _WebviewWebState(url: url);
}

class _WebviewWebState extends State<WebviewWeb> {
  late String url;

  _WebviewWebState({required this.url});

  @override
  void initState() {
    super.initState();
    WebViewPlatform.instance = WebWebViewPlatform();
  }

  @override
  Widget build(BuildContext context) {
    final PlatformWebViewController controller = PlatformWebViewController(
      const PlatformWebViewControllerCreationParams(),
    )..loadRequest(
        LoadRequestParams(
          uri: Uri.parse(url),
        ),
      );
    return PlatformWebViewWidget(
      PlatformWebViewWidgetCreationParams(controller: controller),
    ).build(context);
  }
}
