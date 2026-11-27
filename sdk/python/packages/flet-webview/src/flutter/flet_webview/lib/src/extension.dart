import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'webview.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "WebView":
        // Keyed by control id so that another WebView put in the same place
        // gets its own state and native webview instead of reusing these.
        return WebViewControl(
          key: key ?? ValueKey(control.id),
          control: control,
        );
      default:
        return null;
    }
  }
}
