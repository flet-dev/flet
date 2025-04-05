import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class ReorderableDraggableControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final bool? parentAdaptive;

  const ReorderableDraggableControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  State<ReorderableDraggableControl> createState() => _ListViewControlState();
}

class _ListViewControlState extends State<ReorderableDraggableControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("ReorderableDraggableControl build: ${widget.control.id}");

    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    var index = widget.control.attrInt("index");
    if (index == null) {
      return const ErrorControl("ReorderableDraggable.index is invalid");
    }
    var content = widget.children.where((c) => c.isVisible).firstOrNull;
    if (content == null) {
      return const ErrorControl(
          "ReorderableDraggable.content must be set and visible");
    }

    return ReorderableDragStartListener(
        index: index,
        child: createControl(widget.control, content.id, widget.parentDisabled,
            parentAdaptive: adaptive));
  }
}
