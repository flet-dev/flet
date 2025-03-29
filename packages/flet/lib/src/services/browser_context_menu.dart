import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';

import '../flet_service.dart';

class BrowserContextMenuService extends FletService {
  BrowserContextMenuService(super.control, super.backend);

  @override
  void init() {
    super.init();
    debugPrint(
        "BrowserContextMenuService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void update() {
    debugPrint(
        "BrowserContextMenuService(${control.id}).update: ${control.properties}");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("BrowserContextMenuService.$name($args)");
    switch (name) {
      case "disable_menu":
        return BrowserContextMenu.disableContextMenu();
      case "enable_menu":
        return BrowserContextMenu.enableContextMenu();
      default:
        throw Exception("Unknown BrowserContextMenu method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("BrowserContextMenuService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
