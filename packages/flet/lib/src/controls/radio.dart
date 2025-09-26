import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class RadioControl extends StatefulWidget {
  final Control control;

  RadioControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<RadioControl> createState() => _RadioControlState();
}

class _RadioControlState extends State<RadioControl> {
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
    debugPrint("Radio build: ${widget.control.id}");

    final radioGroup = RadioGroup.maybeOf<String>(context);
    if (radioGroup == null) {
      return const ErrorControl("Radio must be enclosed within RadioGroup");
    }

    var value = widget.control.getString("value", "")!;
    var label = widget.control.getString("label", "")!;
    var labelPosition =
        widget.control.getLabelPosition("label_position", LabelPosition.right)!;
    var labelStyle =
        widget.control.getTextStyle("label_style", Theme.of(context));
    if (widget.control.disabled && labelStyle != null) {
      labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
    }

    var radio = Radio<String>(
      autofocus: widget.control.getBool("autofocus", false)!,
      focusNode: _focusNode,
      mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
      value: value,
      activeColor: widget.control.getColor("active_color", context),
      focusColor: widget.control.getColor("focus_color", context),
      hoverColor: widget.control.getColor("hover_color", context),
      splashRadius: widget.control.getDouble("splash_radius"),
      toggleable: widget.control.getBool("toggleable", false)!,
      fillColor:
          widget.control.getWidgetStateColor("fill_color", Theme.of(context)),
      overlayColor: widget.control
          .getWidgetStateColor("overlay_color", Theme.of(context)),
      visualDensity: widget.control.getVisualDensity("visual_density"),
    );

    Widget result = radio;
    if (label != "") {
      var labelWidget = widget.control.disabled
          ? Text(label, style: labelStyle)
          : MouseRegion(
              cursor: SystemMouseCursors.click,
              child: Text(label, style: labelStyle));
      result = MergeSemantics(
          child: GestureDetector(
              onTap: !widget.control.disabled
                  ? () => radioGroup.onChanged(value)
                  : null,
              child: labelPosition == LabelPosition.right
                  ? Row(children: [radio, labelWidget])
                  : Row(children: [labelWidget, radio])));
    }

    return LayoutControl(control: widget.control, child: result);
  }
}
