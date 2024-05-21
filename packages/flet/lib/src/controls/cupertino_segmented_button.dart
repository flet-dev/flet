import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class CupertinoSegmentedButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool? parentAdaptive;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CupertinoSegmentedButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentAdaptive,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoSegmentedButtonControl> createState() =>
      _CupertinoSegmentedButtonControlState();
}

class _CupertinoSegmentedButtonControlState
    extends State<CupertinoSegmentedButtonControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoSegmentedButtonControl build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    var borderColor = widget.control.attrColor("borderColor", context);
    var selectedColor = widget.control.attrColor("selectedColor", context);
    var unselectedColor = widget.control.attrColor("unselectedColor", context);
    var clickColor = widget.control.attrColor("clickColor", context);
    List<Control> ctrls = widget.children.where((c) => c.isVisible).toList();
    int? selectedIndex = widget.control.attrInt("selectedIndex");

    if (ctrls.length < 2) {
      return const ErrorControl(
          "CupertinoSegmentedButton must have at least two controls.");
    }
    var children = ctrls.asMap().map((i, c) => MapEntry(
        i,
        createControl(widget.control, c.id, disabled,
            parentAdaptive: adaptive)));

    return constrainedControl(
        context,
        CupertinoSegmentedControl(
          children: children,
          groupValue: selectedIndex,
          onValueChanged: (int index) {
            if (!disabled) {
              widget.backend.updateControlState(
                  widget.control.id, {"selectedIndex": index.toString()});
              widget.backend.triggerControlEvent(
                  widget.control.id, "change", index.toString());
              setState(() {
                selectedIndex = index;
              });
            }
          },
          borderColor: borderColor,
          selectedColor: selectedColor,
          unselectedColor: unselectedColor,
          pressedColor: clickColor,
          padding: parseEdgeInsets(widget.control, "padding"),
        ),
        widget.parent,
        widget.control);
  }
}
