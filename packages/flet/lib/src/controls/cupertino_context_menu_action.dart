import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/icons.dart';
import '../utils/numbers.dart';

class CupertinoContextMenuActionControl extends StatelessWidget {
  final Control control;

  const CupertinoContextMenuActionControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoContextMenuAction build ($hashCode): ${control.id}");
    var content = control.buildTextOrWidget("content",
        textStyle: const TextStyle(overflow: TextOverflow.ellipsis));
    if (content == null) {
      return ErrorWidget(
          "content (string or visible Control) must be provided");
    }
    return CupertinoContextMenuAction(
        isDefaultAction: control.getBool("default", false)!,
        isDestructiveAction: control.getBool("destructive", false)!,
        onPressed: () {
          if (!control.disabled) {
            control.triggerEvent("click");
            Navigator.of(context).pop(); // Close the context menu
          }
        },
        trailingIcon: control.getIconData("trailing_icon"),
        child: content);
  }
}
