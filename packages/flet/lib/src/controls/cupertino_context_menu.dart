import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';

class CupertinoContextMenuControl extends StatefulWidget {
  final Control control;

  CupertinoContextMenuControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoContextMenuControl> createState() =>
      _CupertinoContextMenuControlState();
}

class _CupertinoContextMenuControlState
    extends State<CupertinoContextMenuControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoContextMenu build ($hashCode): ${widget.control.id}");

    var content = widget.control.buildWidget("content");
    var actions = widget.control.buildWidgets("actions");

    if (actions.isEmpty) {
      return const ErrorControl(
          "at least one action in CupertinoContextMenu.actions must be visible");
    }
    if (content == null) {
      return const ErrorControl("CupertinoContextMenu.content must be visible");
    }

    return CupertinoContextMenu(
      enableHapticFeedback:
          widget.control.getBool("enable_haptic_feedback", false)!,
      actions: actions,
      child: content,
    );
  }
}
