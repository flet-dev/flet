import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class CupertinoContextMenuActionControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoContextMenuActionControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<CupertinoContextMenuActionControl> createState() =>
      _CupertinoContextMenuActionControlState();
}

class _CupertinoContextMenuActionControlState
    extends State<CupertinoContextMenuActionControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "CupertinoContextMenuAction build ($hashCode): ${widget.control.id}");

    bool disabled = widget.control.disabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.getBool("adaptive") ?? widget.parentAdaptive;
    String text = widget.control.getString("text", "")!;
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.visible);
    IconData? trailingIcon =
        parseIcon(widget.control.getString("trailingIcon"));

    return CupertinoContextMenuAction(
      isDefaultAction: widget.control.getBool("isDefaultAction", false)!,
      isDestructiveAction:
          widget.control.getBool("isDestructiveAction", false)!,
      onPressed: () {
        if (!disabled) {
          widget.backend.triggerControlEvent(widget.control.id, "click");
          Navigator.of(context).pop();
        }
      },
      trailingIcon: trailingIcon,
      child: contentCtrls.isNotEmpty
          ? createControl(widget.control, contentCtrls.first.id, disabled,
              parentAdaptive: adaptive)
          : Text(text, overflow: TextOverflow.ellipsis),
    );
  }
}
