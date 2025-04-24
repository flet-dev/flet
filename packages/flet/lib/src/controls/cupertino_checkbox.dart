import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'base_controls.dart';
import 'list_tile.dart';

class CupertinoCheckboxControl extends StatefulWidget {
  final Control control;

  const CupertinoCheckboxControl({super.key, required this.control});

  @override
  State<CupertinoCheckboxControl> createState() => _CheckboxControlState();
}

class _CheckboxControlState extends State<CupertinoCheckboxControl> {
  bool? _value;
  bool _tristate = false;
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

  void _toggleValue() {
    bool? newValue;
    if (!_tristate) {
      newValue = !_value!;
    } else if (_tristate && _value == null) {
      newValue = false;
    } else if (_tristate && _value == false) {
      newValue = true;
    }
    _onChange(newValue);
  }

  void _onChange(bool? value) {
    _value = value;
    widget.control.updateProperties({"value": value}, notify: true);
    widget.control.triggerEvent("change", data: value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoCheckBox build: ${widget.control.id}");

    _tristate = widget.control.getBool("tristate", false)!;
    var value = widget.control.getBool("value", _tristate ? null : false);
    if (_value != value) {
      _value = value;
    }

    var cupertinoCheckbox = CupertinoCheckbox(
        autofocus: widget.control.getBool("autofocus", false)!,
        focusNode: _focusNode,
        value: _value,
        activeColor: widget.control.getColor(
            "active_color", context, Theme.of(context).colorScheme.primary)!,
        checkColor: widget.control.getColor("check_color", context),
        focusColor: widget.control.getColor("focus_color", context),
        shape: widget.control.getShape("shape", Theme.of(context)),
        mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
        semanticLabel: widget.control.getString("semantics_label"),
        side: widget.control
            .getWidgetStateBorderSide("border_side", Theme.of(context)),
        fillColor:
            widget.control.getWidgetStateColor("fill_color", Theme.of(context)),
        tristate: _tristate,
        onChanged: !widget.control.disabled
            ? (bool? value) => _onChange(value)
            : null);

    // Add listener to ListTile clicks
    ListTileClicks.of(context)?.notifier.addListener(() {
      _toggleValue();
    });

    Widget result = cupertinoCheckbox;

    var labelStyle =
        widget.control.getTextStyle("label_style", Theme.of(context));
    if (widget.control.disabled && labelStyle != null) {
      labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
    }
    var label =
        widget.control.buildTextOrWidget("label", textStyle: labelStyle);
    if (label != null) {
      label = widget.control.disabled
          ? label
          : MouseRegion(cursor: SystemMouseCursors.click, child: label);
      var labelPosition = widget.control
          .getLabelPosition("label_position", LabelPosition.right)!;
      result = MergeSemantics(
          child: GestureDetector(
              onTap: !widget.control.disabled ? _toggleValue : null,
              child: labelPosition == LabelPosition.right
                  ? Row(children: [cupertinoCheckbox, label])
                  : Row(children: [label, cupertinoCheckbox])));
    }

    // Apply width and height if provided
    var width = widget.control.getDouble("width");
    var height = widget.control.getDouble("height");
    if (width != null || height != null) {
      result = SizedBox(
          width: width,
          height: height,
          child: FittedBox(fit: BoxFit.fill, child: result));
    }

    return ConstrainedControl(control: widget.control, child: result);
  }
}
