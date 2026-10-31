import 'package:flet/flet.dart';

import 'quick_actions_service.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "QuickActions": 
        return QuickActionsService(control: control);
      default:
        return null;
    }
  }
}