import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/icons.dart';

class CupertinoContextMenuActionControl extends StatelessWidget {
  final Control control;

  const CupertinoContextMenuActionControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoContextMenuAction build ($hashCode): ${control.id}");
    String contentStr =
        control.getString("content") ?? control.getString("text") ?? ""; // todo(0.70.3): remove "text"

    return CupertinoContextMenuAction(
      isDefaultAction: control.getBool("is_default_action", false)!,
      isDestructiveAction: control.getBool("is_destructive_action", false)!,
      onPressed: () {
        if (!control.disabled) {
          FletBackend.of(context).triggerControlEvent(control, "click");
          Navigator.of(context).pop(); // Close the context menu
        }
      },
      trailingIcon: parseIcon(control.getString("trailing_icon")),
      child: control.buildWidget("content") ??
          Text(contentStr, overflow: TextOverflow.ellipsis),
    );
  }
}
