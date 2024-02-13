import 'package:flet/flet.dart';

import 'webview.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "webview":
      return WebViewControl(
          parent: args.parent,
          control: args.control,
          parentDisabled: args.parentDisabled,
          backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to do
}
