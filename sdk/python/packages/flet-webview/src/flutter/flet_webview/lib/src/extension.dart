import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';

import 'webview.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "WebView":
        return WebViewControl(control: control);
      default:
        return null;
    }
  }
}
