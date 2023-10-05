import 'dart:io' show Platform;
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_tree_view_model.dart';
import '../utils/colors.dart';
import 'create_control.dart';


import 'package:webview_flutter/webview_flutter.dart';

class WebView extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const WebView(
      {Key? key,
      required this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    var result = StoreConnector<AppState, ControlTreeViewModel>(
        distinct: true,
        converter: (store) => ControlTreeViewModel.fromStore(store, control),
        builder: (context, viewModel) {
          debugPrint("MobileWebViewer build: ${control.id}");

          String url = control.attrString("url") ?? "https://flet.dev/";
          bool javascriptEnabled = control.attrBool("javascriptEnabled") ?? false;
          var bgcolor = HexColor.fromString(Theme.of(context),
              control.attrString("bgcolor") ?? "white")!;
          String preventLink = control.attrString("preventLink") ?? "none";


          var jsMode = JavaScriptMode.unrestricted;
          if (javascriptEnabled){
            jsMode = JavaScriptMode.unrestricted;
          }else{
            jsMode = JavaScriptMode.disabled;
          }

          if (Platform.isIOS || Platform.isAndroid){
            var controller = WebViewController()
            ..setJavaScriptMode(jsMode)
            ..setBackgroundColor(bgcolor)
            ..setNavigationDelegate(
              NavigationDelegate(
                onProgress: (int progress) {},
                onPageStarted: (String url) {
                  FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: control.id,
                    eventName: "page_started",
                    eventData: url);
                },
                onPageFinished: (String url) {
                  FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: control.id,
                    eventName: "page_ended",
                    eventData: url);
                },
                onWebResourceError: (WebResourceError error) {
                  FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: control.id,
                    eventName: "web_resource_error",
                    eventData: error.toString());
                },
                onNavigationRequest: (NavigationRequest request) {
                  if (request.url.startsWith(preventLink)) {
                    return NavigationDecision.prevent;
                  }
                  return NavigationDecision.navigate;
                },
              ),
            )
            ..loadRequest(Uri.parse(url));
            return WebViewWidget(
              controller: controller
            );
          }else if (Platform.isMacOS){
            return const Text("'MobileWbBrowser' is not supported on macOS yet.");
          }else if (Platform.isWindows){
            return const Text("'MobileWbBrowser' is not supported on windows yey.");
          }else if (Platform.isLinux){
            return const Text("'MobileWbBrowser' is not supported on this platform.");
          }else{
            return const Text("'MobileWbBrowser' is not supported on this platform.");
          }
        });

    return constrainedControl(context, result, parent, control);
  }
}
