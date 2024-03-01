import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';

class SemanticsServiceControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const SemanticsServiceControl(
      {super.key, this.parent, required this.control, required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("SemanticsService build: ${control.id}");

    var method = control.attrString("method");

    if (method != null) {
      debugPrint("SemanticsService JSON method: $method");

      void resetMethod() {
        backend.updateControlState(control.id, {"method": ""});
      }

      var mj = json.decode(method);
      var name = mj["n"] as String;
      var params = Map<String, dynamic>.from(mj["p"] as Map);

      var message = params["text"].toString();
      if (name == "announce") {
        debugPrint("SemanticsService.announceMessage($message)");
        WidgetsBinding.instance.addPostFrameCallback((_) {
          resetMethod();
          var rtl = params["rtl"];
          var assertiveness = Assertiveness.values.firstWhere(
              (e) => e.name == params["assertiveness"].toString().toLowerCase(),
              orElse: () => Assertiveness.polite);
          SemanticsService.announce(
              message, rtl ? TextDirection.rtl : TextDirection.ltr,
              assertiveness: assertiveness);
        });
      } else if (name == "tooltip") {
        debugPrint("SemanticsService.announceTooltip($message)");
        WidgetsBinding.instance.addPostFrameCallback((_) {
          resetMethod();
          SemanticsService.tooltip(message);
        });
      }
    }

    return const SizedBox.shrink();
  }
}
