import 'package:flutter/material.dart';

import '../flet_service.dart';

class TesterService extends FletService {
  TesterService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("Tester(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    debugPrint("Tester(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Tester.$name($args)");
    switch (name) {
      case "pump_and_settle":
        await control.backend.tester?.pumpAndSettle();
      case "count_by_text":
        return control.backend.tester?.countByText(args["text"]);
      case "teardown":
        control.backend.tester?.teardown();
      default:
        throw Exception("Unknown Tester method: $name");
    }
  }
}
