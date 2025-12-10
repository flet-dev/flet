import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';

import '../flet_service.dart';

class ClipboardService extends FletService {
  ClipboardService({required super.control});

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
        await Clipboard.setData(ClipboardData(text: args["data"]));
      case "get":
        var data = await Clipboard.getData(Clipboard.kTextPlain);
        return data?.text;
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
