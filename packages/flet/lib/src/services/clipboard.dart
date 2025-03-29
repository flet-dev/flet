import 'package:flutter/cupertino.dart';

import '../flet_service.dart';
import '../utils/clipboard.dart';

class ClipboardService extends FletService {
  ClipboardService(super.control, super.backend);

  @override
  void init() {
    super.init();
    debugPrint("ClipboardService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void update() {
    debugPrint("ClipboardService(${control.id}).update: ${control.properties}");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("ClipboardService.$name($args)");
    switch (name) {
      case "set":
        setClipboard(args["data"]);
      case "get":
        return getClipboard();
      default:
        throw Exception("Unknown Clipboard method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("ClipboardService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
