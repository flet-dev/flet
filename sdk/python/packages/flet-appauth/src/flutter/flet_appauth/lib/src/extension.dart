import 'package:flet/flet.dart';

import 'app_auth.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "AppAuth":
        return AppAuthService(control: control);
      default:
        return null;
    }
  }
}
