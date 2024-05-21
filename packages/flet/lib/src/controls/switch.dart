import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/mouse.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'cupertino_switch.dart';
import 'flet_store_mixin.dart';
import 'list_tile.dart';

enum LabelPosition { right, left }

class SwitchControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const SwitchControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<SwitchControl> createState() => _SwitchControlState();
}

class _SwitchControlState extends State<SwitchControl> with FletStoreMixin {
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
    debugPrint("SwitchControl build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive =
          widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoSwitchControl(
            control: widget.control,
            parentDisabled: widget.parentDisabled,
            backend: widget.backend);
      }

      String label = widget.control.attrString("label", "")!;
      LabelPosition labelPosition = LabelPosition.values.firstWhere(
          (p) =>
              p.name.toLowerCase() ==
              widget.control.attrString("labelPosition", "")!.toLowerCase(),
          orElse: () => LabelPosition.right);
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      TextStyle? labelStyle =
          parseTextStyle(Theme.of(context), widget.control, "labelStyle");
      if (disabled && labelStyle != null) {
        labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
      }

      debugPrint("Switch build: ${widget.control.id}");

      bool value = widget.control.attrBool("value", false)!;
      if (_value != value) {
        _value = value;
      }

      var swtch = Switch(
          autofocus: autofocus,
          focusNode: _focusNode,
          activeColor: widget.control.attrColor("activeColor", context),
          activeTrackColor:
              widget.control.attrColor("activeTrackColor", context),
          inactiveThumbColor:
              widget.control.attrColor("inactiveThumbColor", context),
          inactiveTrackColor:
              widget.control.attrColor("inactiveTrackColor", context),
          thumbColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "thumbColor"),
          thumbIcon: parseMaterialStateIcon(
              Theme.of(context), widget.control, "thumbIcon"),
          trackColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "trackColor"),
          focusColor: widget.control.attrColor("focusColor", context),
          value: _value,
          mouseCursor:
              parseMouseCursor(widget.control.attrString("mouseCursor")),
          splashRadius: widget.control.attrDouble("splashRadius"),
          hoverColor: widget.control.attrColor("hoverColor", context),
          overlayColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "overlayColor"),
          trackOutlineColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "trackOutlineColor"),
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
            ? Text(label, style: labelStyle)
            : MouseRegion(
                cursor: SystemMouseCursors.click,
                child: Text(label, style: labelStyle));
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
    });
  }
}
