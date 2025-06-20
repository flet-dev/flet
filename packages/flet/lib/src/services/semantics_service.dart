import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';

import '../flet_service.dart';
import '../utils/misc.dart';

class SemanticsServiceControl extends FletService {
  SemanticsServiceControl({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("SemanticsService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    debugPrint("SemanticsService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("SemanticsService.$name($args)");
    var message = args["message"].toString();
    switch (name) {
      case "announce_message":
        return SemanticsService.announce(
            message, args["rtl"] ? TextDirection.rtl : TextDirection.ltr,
            assertiveness: control.getAssertiveness(
                args["assertiveness"], Assertiveness.polite)!);
      case "announce_tooltip":
        return SemanticsService.tooltip(message);
      default:
        throw Exception("Unknown SemanticsService method: $name");
    }
  }
}
