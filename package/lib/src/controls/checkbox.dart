import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'cupertino_checkbox.dart';
import 'flet_control_state.dart';
import 'list_tile.dart';

enum LabelPosition { right, left }

class CheckboxControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const CheckboxControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled});

  @override
  State<CheckboxControl> createState() => _CheckboxControlState();
}

class _CheckboxControlState extends FletControlState<CheckboxControl> {
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
    sendControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
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
    var svalue = value != null ? value.toString() : "";
    _value = value;
    updateControlProps(widget.control.id, {"value": svalue});
    sendControlEvent(widget.control.id, "change", svalue);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Checkbox build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool adaptive = widget.control.attrBool("adaptive", false)!;
      if (adaptive &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoCheckboxControl(
            control: widget.control, parentDisabled: widget.parentDisabled);
      }

      String label = widget.control.attrString("label", "")!;
      LabelPosition labelPosition = LabelPosition.values.firstWhere(
          (p) =>
              p.name.toLowerCase() ==
              widget.control.attrString("labelPosition", "")!.toLowerCase(),
          orElse: () => LabelPosition.right);
      _tristate = widget.control.attrBool("tristate", false)!;
      bool autofocus = widget.control.attrBool("autofocus", false)!;

      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      debugPrint("Checkbox build: ${widget.control.id}");

      bool? value = widget.control.attrBool("value", _tristate ? null : false);
      if (_value != value) {
        _value = value;
      }

      var checkbox = Checkbox(
          autofocus: autofocus,
          focusNode: _focusNode,
          value: _value,
          activeColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("activeColor", "")!),
          focusColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("focusColor", "")!),
          hoverColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("hoverColor", "")!),
          overlayColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "overlayColor"),
          checkColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("checkColor", "")!),
          fillColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "fillColor"),
          tristate: _tristate,
          onChanged: !disabled
              ? (bool? value) {
                  _onChange(value);
                }
              : null);

      ListTileClicks.of(context)?.notifier.addListener(() {
        _toggleValue();
      });

      Widget result = checkbox;
      if (label != "") {
        var labelWidget = disabled
            ? Text(label,
                style: TextStyle(color: Theme.of(context).disabledColor))
            : MouseRegion(cursor: SystemMouseCursors.click, child: Text(label));
        result = MergeSemantics(
            child: GestureDetector(
                onTap: !disabled ? _toggleValue : null,
                child: labelPosition == LabelPosition.right
                    ? Row(children: [checkbox, labelWidget])
                    : Row(children: [labelWidget, checkbox])));
      }

      return constrainedControl(context, result, widget.parent, widget.control);
    });
  }
}
