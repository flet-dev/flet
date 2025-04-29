import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class CupertinoActionSheetActionControl extends StatelessWidget {
  final Control control;

  const CupertinoActionSheetActionControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActionSheetActionControl build: ${control.id}");

    var content = control.buildTextOrWidget("content");
    if (content == null) {
      return const ErrorControl(
          "CupertinoActionSheetAction.content must be a string or visible Control");
    }

    final actionSheet = CupertinoActionSheetAction(
      isDefaultAction: control.getBool("default", false)!,
      isDestructiveAction: control.getBool("destructive", false)!,
      onPressed: () {
        if (!control.disabled) {
          control.triggerEvent("click");
        }
      },
      mouseCursor: control.getMouseCursor("mouse_cursor"),
      child: content,
    );

    return ConstrainedControl(control: control, child: actionSheet);
  }
}
