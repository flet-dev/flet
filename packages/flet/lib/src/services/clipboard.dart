import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:pasteboard/pasteboard.dart';

import '../flet_service.dart';
import '../utils/images.dart';

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
      case "set_image":
        await Pasteboard.writeImage(convertToUint8List(args["data"]));
      case "get_image":
        return await Pasteboard.image;
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
