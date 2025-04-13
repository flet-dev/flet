import 'package:flutter/cupertino.dart';

import '../controls/control_widget.dart';
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

    var content = control.get("content");
    var text = control.getString("text"); // todo(0.73.0): remove "text"
    if (content == null && text == null) {
      return const ErrorControl(
          "CupertinoActionSheetAction.content must be set and visible");
    }

    final actionSheet = CupertinoActionSheetAction(
      isDefaultAction: control.getBool("is_default_action", false)!,
      isDestructiveAction: control.getBool("is_destructive_action", false)!,
      onPressed: () {
        if (!control.disabled) {
          control.triggerEvent("click");
        }
      },
      mouseCursor: control.getMouseCursor("mouse_cursor"),
      child: content is Control
          ? ControlWidget(control: content)
          : content is String
              ? Text(content)
              : text is String
                  ? Text(text)
                  : const SizedBox.shrink(),
    );

    return ConstrainedControl(control: control, child: actionSheet);
  }
}
