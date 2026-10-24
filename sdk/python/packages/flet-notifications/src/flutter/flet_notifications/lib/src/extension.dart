import 'package:flet/flet.dart';

import 'notifications_service.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "Notifications":
        return NotificationsService(control: control);
      default:
        return null;
    }
  }
}
