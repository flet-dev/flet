import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'list_tile.dart';

enum LabelPosition { right, left }

class CupertinoSwitchControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CupertinoSwitchControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoSwitchControl> createState() => _CupertinoSwitchControlState();
}

class _CupertinoSwitchControlState extends State<CupertinoSwitchControl> {
  bool _value = false;
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onChange(bool value) {
    var svalue = value.toString();
    debugPrint(svalue);
    _value = value;
    widget.backend.updateControlState(widget.control.id, {"value": svalue});
    widget.backend.triggerControlEvent(widget.control.id, "change", svalue);
  }

  void _onFocusChange() {
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoSwitchControl build: ${widget.control.id}");

    String label = widget.control.attrString("label", "")!;
    LabelPosition labelPosition = LabelPosition.values.firstWhere(
        (p) =>
            p.name.toLowerCase() ==
            widget.control.attrString("labelPosition", "")!.toLowerCase(),
        orElse: () => LabelPosition.right);
    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    debugPrint("CupertinoSwitch build: ${widget.control.id}");

    bool value = widget.control.attrBool("value", false)!;
    if (_value != value) {
      _value = value;
    }

    var materialThumbColor = parseMaterialStateColor(
        Theme.of(context), widget.control, "thumbColor");

    var materialTrackColor = parseMaterialStateColor(
        Theme.of(context), widget.control, "trackColor");

    var swtch = CupertinoSwitch(
        autofocus: autofocus,
        focusNode: _focusNode,
        activeColor: widget.control.attrColor("activeColor", context),
        thumbColor: materialThumbColor?.resolve({}),
        trackColor: materialTrackColor?.resolve({}),
        focusColor: widget.control.attrColor("focusColor", context),
        value: _value,
        offLabelColor: widget.control.attrColor("offLabelColor", context),
        onLabelColor: widget.control.attrColor("onLabelColor", context),
        onChanged: !disabled
            ? (bool value) {
                _onChange(value);
              }
            : null);

    ListTileClicks.of(context)?.notifier.addListener(() {
      _onChange(!_value);
    });

    Widget result = swtch;
    if (label != "") {
      var labelWidget = disabled
          ? Text(label,
              style: TextStyle(color: Theme.of(context).disabledColor))
          : MouseRegion(cursor: SystemMouseCursors.click, child: Text(label));
      result = MergeSemantics(
          child: GestureDetector(
              onTap: !disabled
                  ? () {
                      _onChange(!_value);
                    }
                  : null,
              child: labelPosition == LabelPosition.right
                  ? Row(children: [swtch, labelWidget])
                  : Row(children: [labelWidget, swtch])));
    }

    return constrainedControl(context, result, widget.parent, widget.control);
  }
}
