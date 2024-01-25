import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'cupertino_switch.dart';
import 'list_tile.dart';

enum LabelPosition { right, left }

class SwitchControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final dynamic dispatch;

  const SwitchControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.dispatch});

  @override
  State<SwitchControl> createState() => _SwitchControlState();
}

class _SwitchControlState extends State<SwitchControl> {
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
    setState(() {
      _value = value;
    });
    List<Map<String, String>> props = [
      {"i": widget.control.id, "value": svalue}
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
    final server = FletAppServices.of(context).server;
    server.updateControlProps(props: props);
    server.sendPageEvent(
        eventTarget: widget.control.id, eventName: "change", eventData: svalue);
  }

  void _onFocusChange() {
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SwitchControl build: ${widget.control.id}");

    bool adaptive = widget.control.attrBool("adaptive", false)!;
    if (adaptive &&
        (defaultTargetPlatform == TargetPlatform.iOS ||
            defaultTargetPlatform == TargetPlatform.macOS)) {
      return CupertinoSwitchControl(
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
    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    debugPrint("Switch build: ${widget.control.id}");

    bool value = widget.control.attrBool("value", false)!;
    if (_value != value) {
      _value = value;
    }

    var swtch = Switch(
        autofocus: autofocus,
        focusNode: _focusNode,
        activeColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("activeColor", "")!),
        activeTrackColor: HexColor.fromString(Theme.of(context),
            widget.control.attrString("activeTrackColor", "")!),
        inactiveThumbColor: HexColor.fromString(Theme.of(context),
            widget.control.attrString("inactiveThumbColor", "")!),
        inactiveTrackColor: HexColor.fromString(Theme.of(context),
            widget.control.attrString("inactiveTrackColor", "")!),
        thumbColor: parseMaterialStateColor(
            Theme.of(context), widget.control, "thumbColor"),
        thumbIcon: parseMaterialStateIcon(
            Theme.of(context), widget.control, "thumbIcon"),
        trackColor: parseMaterialStateColor(
            Theme.of(context), widget.control, "trackColor"),
        focusColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("focusColor", "")!),
        value: _value,
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
