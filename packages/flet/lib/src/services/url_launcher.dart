import 'package:flutter/cupertino.dart';
import 'package:url_launcher/url_launcher.dart';

import '../flet_service.dart';
import '../utils/enums.dart';
import '../utils/launch_url.dart';
import '../utils/numbers.dart';

class UrlLauncherService extends FletService {
  UrlLauncherService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("UrlLauncherService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void update() {
    debugPrint(
        "UrlLauncherService(${control.id}).update: ${control.properties}");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("UrlLauncherService.$name($args)");
    switch (name) {
      case "launch_url":
        return openWebBrowser(parseUrl(args["url"]!)!,
            mode: _parseLaunchMode(args["mode"]),
            webViewConfiguration:
                _parseWebViewConfiguration(args["web_view_configuration"]),
            browserConfiguration:
                _parseBrowserConfiguration(args["browser_configuration"]),
            webOnlyWindowName: args["web_only_window_name"]);
      case "can_launch_url":
        return canLaunchUrl(Uri.parse(parseUrl(args["url"]!)!.url));
      case "close_in_app_web_view":
        return closeInAppWebView();
      case "open_window":
        return openWindow(parseUrl(args["url"]!)!,
            title: args["title"],
            width: parseDouble(args["width"]),
            height: parseDouble(args["height"]));
      case "supports_launch_mode":
        return supportsLaunchMode(_parseLaunchMode(args["mode"]));
      case "supports_close_for_launch_mode":
        return supportsCloseForLaunchMode(_parseLaunchMode(args["mode"]));
      default:
        throw Exception("Unknown UrlLauncher method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("UrlLauncherService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}

LaunchMode _parseLaunchMode(dynamic value) {
  return parseEnum(LaunchMode.values, value, LaunchMode.platformDefault)!;
}

WebViewConfiguration? _parseWebViewConfiguration(dynamic value) {
  if (value is Map) {
    var enableJavaScript = parseBool(value["enable_javascript"], true)!;
    var enableDomStorage = parseBool(value["enable_dom_storage"], true)!;
    var headersValue = value["headers"];
    var headers = headersValue is Map
        ? headersValue.map((key, headerValue) =>
            MapEntry(key.toString(), headerValue.toString()))
        : <String, String>{};
    return WebViewConfiguration(
        enableJavaScript: enableJavaScript,
        enableDomStorage: enableDomStorage,
        headers: headers);
  }
  return null;
}

BrowserConfiguration? _parseBrowserConfiguration(dynamic value) {
  if (value is Map) {
    var showTitle = parseBool(value["show_title"], false)!;
    return BrowserConfiguration(showTitle: showTitle);
  }
  return null;
}
