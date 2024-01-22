import 'package:flet/src/controls/cupertino_checkbox.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'list_tile.dart';

enum LabelPosition { right, left }

class CheckboxControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final dynamic dispatch;

  const CheckboxControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.dispatch});

  @override
  State<CheckboxControl> createState() => _CheckboxControlState();
}

class _CheckboxControlState extends State<CheckboxControl> {
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
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
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
    setState(() {
      _value = value;
    });
    List<Map<String, String>> props = [
      {"i": widget.control.id, "value": svalue}
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
    var server = FletAppServices.of(context).server;
    server.updateControlProps(props: props);
    server.sendPageEvent(
        eventTarget: widget.control.id, eventName: "change", eventData: svalue);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Checkbox build: ${widget.control.id}");
    bool adaptive = widget.control.attrBool("adaptive", false)!;
    if (adaptive &&
        (defaultTargetPlatform == TargetPlatform.iOS ||
            defaultTargetPlatform == TargetPlatform.macOS)) {
      return CupertinoCheckboxControl(
          control: widget.control,
          parentDisabled: widget.parentDisabled,
          dispatch: widget.dispatch);
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

    debugPrint("Checkbox StoreConnector build: ${widget.control.id}");

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
  }
}
