import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:url_launcher/url_launcher.dart';

import '../utils/platform_utils_non_web.dart'
    if (dart.library.js) "../utils/platform_utils_web.dart";

import '../models/control.dart';

class LaunchUrlControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const LaunchUrlControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<LaunchUrlControl> createState() => _LaunchUrlControlState();
}

class _LaunchUrlControlState extends State<LaunchUrlControl> {
  String? _launchUrlJson;
  String? _closeInAppWebViewJson;

  @override
  Widget build(BuildContext context) {
    debugPrint("Launch URL build: ${widget.control.id}");

    var launchUrlJson = widget.control.attrString("launchUrl");
    if (launchUrlJson != null && launchUrlJson != _launchUrlJson) {
      debugPrint("Launch URL JSON value: $launchUrlJson");
      _launchUrlJson = launchUrlJson;

      var jv = json.decode(launchUrlJson);
      var url = jv["url"];
      var webWindowName = jv["web_window_name"];
      var webPopupWindow = jv["web_popup_window"] as bool;
      if (webPopupWindow) {
        openPopupBrowserWindow(url, webWindowName, 1200, 800);
      } else {
        launchUrl(Uri.parse(url), webOnlyWindowName: webWindowName);
      }
    }

    var closeInAppWebViewJson = widget.control.attrString("closeInAppWebView");
    if (closeInAppWebViewJson != null &&
        closeInAppWebViewJson != _closeInAppWebViewJson) {
      debugPrint(
          "Launch URL Close In app web view JSON value: $closeInAppWebViewJson");
      _closeInAppWebViewJson = closeInAppWebViewJson;

      if (!kIsWeb &&
          (defaultTargetPlatform == TargetPlatform.android ||
              defaultTargetPlatform == TargetPlatform.iOS)) {
        closeInAppWebView();
      }
    }

    return const SizedBox.shrink();
  }
}
