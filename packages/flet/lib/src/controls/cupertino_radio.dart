import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';

class CupertinoRadioControl extends StatefulWidget {
  final Control control;

  CupertinoRadioControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoRadioControl> createState() => _CupertinoRadioControlState();
}

class _CupertinoRadioControlState extends State<CupertinoRadioControl>
    with FletStoreMixin {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoRadio build: ${widget.control.id}");

    final radioGroup = RadioGroup.maybeOf<String>(context);
    if (radioGroup == null) {
      return const ErrorControl(
          "CupertinoRadio must be enclosed within RadioGroup");
    }

    var value = widget.control.getString("value", "")!;

    var cupertinoRadio = CupertinoRadio<String>(
      autofocus: widget.control.getBool("autofocus", false)!,
      focusNode: _focusNode,
      value: value,
      useCheckmarkStyle: widget.control.getBool("use_checkmark_style", false)!,
      fillColor: widget.control.getColor("fill_color", context),
      focusColor: widget.control.getColor("focus_color", context),
      toggleable: widget.control.getBool("toggleable", false)!,
      mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
      activeColor: widget.control.getColor(
          "active_color", context, Theme.of(context).colorScheme.primary)!,
      inactiveColor: widget.control.getColor("inactive_color", context),
    );

    Widget result = cupertinoRadio;

    var label = widget.control.getString("label", "")!;
    if (label != "") {
      var labelPosition = widget.control
          .getLabelPosition("label_position", LabelPosition.right)!;
      var labelWidget = widget.control.disabled
          ? Text(label,
              style: TextStyle(color: Theme.of(context).disabledColor))
          : MouseRegion(cursor: SystemMouseCursors.click, child: Text(label));
      result = MergeSemantics(
          child: GestureDetector(
              onTap: !widget.control.disabled
                  ? () => radioGroup.onChanged(value)
                  : null,
              child: labelPosition == LabelPosition.right
                  ? Row(children: [cupertinoRadio, labelWidget])
                  : Row(children: [labelWidget, cupertinoRadio])));
    }

    return LayoutControl(control: widget.control, child: result);
  }
}
