import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoPickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoPickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentAdaptive,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoPickerControl> createState() => _CupertinoPickerControlState();
}

class _CupertinoPickerControlState extends State<CupertinoPickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoPicker build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    double? itemExtent = widget.control.attrDouble("itemExtent");
    if (itemExtent == null) {
      return ErrorControl("CupertinoPicker.item_extent must be specified.");
    }

    List<Widget> ctrls = widget.children.where((c) => c.isVisible).map((c) {
      return createControl(widget.control, c.id, disabled,
          parentAdaptive: widget.parentAdaptive);
    }).toList();

    int? selectedIndex = widget.control.attrInt("selectedIndex");
    double diameterRatio = widget.control.attrDouble("diameterRatio", 1.07)!;
    double magnification = widget.control.attrDouble("magnification", 1.0)!;
    double squeeze = widget.control.attrDouble("squeeze", 1.45)!;
    double offAxisFraction = widget.control.attrDouble("offAxisFraction", 0.0)!;
    bool showMagnifier = widget.control.attrBool("showMagnifier", false)!;
    bool loop = widget.control.attrBool("loop", false)!;
    Color? backgroundColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgColor", "")!);

    return constrainedControl(
        context,
        CupertinoPicker(
          backgroundColor: backgroundColor,
          diameterRatio: diameterRatio,
          magnification: magnification,
          squeeze: squeeze,
          offAxisFraction: offAxisFraction,
          itemExtent: itemExtent,
          useMagnifier: showMagnifier,
          looping: loop,
          onSelectedItemChanged: (int index) {
            widget.backend.updateControlState(
                widget.control.id, {"selectedIndex": index.toString()});
            widget.backend.triggerControlEvent(
                widget.control.id, "change", index.toString());
          },
          scrollController: selectedIndex != null
              ? FixedExtentScrollController(initialItem: selectedIndex)
              : null,
          children: ctrls,
        ),
        widget.parent,
        widget.control);
  }
}
