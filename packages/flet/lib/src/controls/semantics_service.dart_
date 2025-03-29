import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/others.dart';

class SemanticsServiceControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const SemanticsServiceControl(
      {super.key, this.parent, required this.control, required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("SemanticsService build: ${control.id}");

    backend.subscribeMethods(control.id, (methodName, args) async {
      var message = args["message"].toString();
      switch (methodName) {
        case "announce_message":
          debugPrint("SemanticsService.announceMessage($message)");
          var rtl = args["rtl"] == "true";
          var assertiveness = parseAssertiveness(
              args["assertiveness"].toString(), Assertiveness.polite)!;
          SemanticsService.announce(
              message, rtl ? TextDirection.rtl : TextDirection.ltr,
              assertiveness: assertiveness);
          break;
        case "announce_tooltip":
          debugPrint("SemanticsService.announceTooltip($message)");
          SemanticsService.tooltip(message);
          break;
      }
      return null;
    });

    return const SizedBox.shrink();
  }
}
