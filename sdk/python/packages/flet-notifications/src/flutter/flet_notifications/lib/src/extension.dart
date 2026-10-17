import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'notifications_service.dart';

class Extension extends FletExtension {
  @override
  void ensureInitialized() {
    // Plugin initialization is driven by the LocalNotifications service
    // control, which carries the per-app settings. Nothing happens here.
  }

  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "LocalNotifications":
        return LocalNotificationsService(control: control);
      default:
        return null;
    }
  }

  @override
  Widget? createWidget(Key? key, Control control) {
    return null;
  }
}
