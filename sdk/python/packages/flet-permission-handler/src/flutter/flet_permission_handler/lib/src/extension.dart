import 'package:flet/flet.dart';

import 'permission_handler.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "PermissionHandler":
        return PermissionHandlerService(control: control);
      default:
        return null;
    }
  }
}
