import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';

class CupertinoActionSheetControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoActionSheetControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<CupertinoActionSheetControl> createState() =>
      _CupertinoActionSheetControlState();
}

class _CupertinoActionSheetControlState
    extends State<CupertinoActionSheetControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActionSheetControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var titleCtrls =
        widget.children.where((c) => c.name == "title" && c.isVisible);
    var messageCtrls =
        widget.children.where((c) => c.name == "message" && c.isVisible);
    var cancelButtonCtrls =
        widget.children.where((c) => c.name == "cancel" && c.isVisible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.isVisible);

    var sheet = CupertinoActionSheet(
      title: titleCtrls.isNotEmpty
          ? createControl(widget.control, titleCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      message: messageCtrls.isNotEmpty
          ? createControl(widget.control, messageCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      cancelButton: cancelButtonCtrls.isNotEmpty
          ? createControl(widget.control, cancelButtonCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      actions: actionCtrls.isNotEmpty
          ? actionCtrls
              .map((c) => createControl(widget.control, c.id, disabled,
                  parentAdaptive: widget.parentAdaptive))
              .toList()
          : null,
    );

    return constrainedControl(context, sheet, widget.parent, widget.control);
  }
}
