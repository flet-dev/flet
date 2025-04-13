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
    var contentStr = control.getString("content") ??
        control.getString("text") ?? // todo(0.73.0): remove "text"
        "";

    return CupertinoContextMenuAction(
      isDefaultAction: control.getBool("is_default_action", false)!,
      isDestructiveAction: control.getBool("is_destructive_action", false)!,
      onPressed: () {
        if (!control.disabled) {
          control.triggerEvent("click");
          Navigator.of(context).pop(); // Close the context menu
        }
      },
      trailingIcon: control.getIcon("trailing_icon"),
      child: control.buildWidget("content") ??
          Text(contentStr, overflow: TextOverflow.ellipsis),
    );
  }
}
