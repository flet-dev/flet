import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class CupertinoContextMenuControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoContextMenuControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<CupertinoContextMenuControl> createState() =>
      _CupertinoContextMenuControlState();
}

class _CupertinoContextMenuControlState
    extends State<CupertinoContextMenuControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoContextMenu build ($hashCode): ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.isVisible);

    if (actionCtrls.isEmpty) {
      return const ErrorControl(
          "CupertinoContextMenu.actions must be provided and at least one action must be visible");
    }
    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "CupertinoContextMenu.content must be provided and visible");
    }

    return CupertinoContextMenu(
      enableHapticFeedback:
          widget.control.attrBool("enableHapticFeedback", false)!,
      actions: actionCtrls.map((c) {
        return createControl(widget.control, c.id, disabled,
            parentAdaptive: adaptive);
      }).toList(),
      child: createControl(widget.control, contentCtrls.first.id, disabled,
          parentAdaptive: adaptive),
    );
  }
}
