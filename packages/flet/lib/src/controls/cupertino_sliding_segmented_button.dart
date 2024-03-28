import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class CupertinoSlidingSegmentedButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool? parentAdaptive;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CupertinoSlidingSegmentedButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentAdaptive,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoSlidingSegmentedButtonControl> createState() =>
      _CupertinoSlidingSegmentedButtonControlState();
}

class _CupertinoSlidingSegmentedButtonControlState
    extends State<CupertinoSlidingSegmentedButtonControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "CupertinoSlidingSegmentedButtonControl build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    var thumbColor = widget.control.attrColor("thumbColor", context) ??
        const CupertinoDynamicColor.withBrightness(
          color: Color(0xFFFFFFFF),
          darkColor: Color(0xFF636366),
        );
    var bgColor = widget.control.attrColor("bgColor", context) ??
        CupertinoColors.tertiarySystemFill;
    List<Control> ctrls = widget.children.where((c) => c.isVisible).toList();
    int? selectedIndex = widget.control.attrInt("selectedIndex");
    var padding =
        (parseEdgeInsets(widget.control, "padding") as EdgeInsetsGeometry?) ??
            const EdgeInsets.symmetric(vertical: 2, horizontal: 3);

    if (ctrls.length < 2) {
      return const ErrorControl("When allow_empty_selection is False, "
          "the selected property must contain at least one value.");
    }
    Map<int, Widget> children = ctrls.asMap().map((i, c) => MapEntry(
        i,
        createControl(widget.control, c.id, disabled,
            parentAdaptive: adaptive)));

    return constrainedControl(
        context,
        CupertinoSlidingSegmentedControl(
          children: children,
          groupValue: selectedIndex,
          onValueChanged: (int? index) {
            if (!disabled) {
              widget.backend.updateControlState(widget.control.id,
                  {"selectedIndex": index != null ? index.toString() : ""});
              widget.backend.triggerControlEvent(widget.control.id, "change",
                  index != null ? index.toString() : "");
            }
          },
          thumbColor: thumbColor,
          backgroundColor: bgColor,
          padding: padding,
        ),
        widget.parent,
        widget.control);
  }
}
