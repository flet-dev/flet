import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'cupertino_switch.dart';
import 'flet_store_mixin.dart';
import 'list_tile.dart';

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
        widget.control.id,
        _focusNode.hasFocus ? "focus" : "blur",
        _focusNode.hasPrimaryFocus.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SwitchControl build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive =
          widget.control.getBool("adaptive") ?? widget.parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoSwitchControl(
            control: widget.control,
            parentDisabled: widget.parentDisabled,
            backend: widget.backend);
      }

      String label = widget.control.getString("label", "")!;
      LabelPosition labelPosition = parseLabelPosition(
          widget.control.getString("labelPosition"), LabelPosition.right)!;
      double? width = widget.control.getDouble("width");
      double? height = widget.control.getDouble("height");
      bool autofocus = widget.control.getBool("autofocus", false)!;
      bool disabled = widget.control.disabled || widget.parentDisabled;

      TextStyle? labelStyle =
          parseTextStyle(Theme.of(context), widget.control, "labelStyle");
      if (disabled && labelStyle != null) {
        labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
      }

      bool value = widget.control.getBool("value", false)!;
      if (_value != value) {
        _value = value;
      }

      var s = Switch(
          autofocus: autofocus,
          focusNode: _focusNode,
          activeColor: widget.control.getColor("activeColor", context),
          activeTrackColor:
              widget.control.getColor("activeTrackColor", context),
          inactiveThumbColor:
              widget.control.getColor("inactiveThumbColor", context),
          inactiveTrackColor:
              widget.control.getColor("inactiveTrackColor", context),
          thumbColor: parseWidgetStateColor(
              Theme.of(context), widget.control, "thumbColor"),
          thumbIcon: parseWidgetStateIcon(
              Theme.of(context), widget.control, "thumbIcon"),
          trackColor: parseWidgetStateColor(
              Theme.of(context), widget.control, "trackColor"),
          focusColor: widget.control.getColor("focusColor", context),
          value: _value,
          mouseCursor:
              parseMouseCursor(widget.control.getString("mouseCursor")),
          splashRadius: widget.control.getDouble("splashRadius"),
          hoverColor: widget.control.getColor("hoverColor", context),
          overlayColor: parseWidgetStateColor(
              Theme.of(context), widget.control, "overlayColor"),
          trackOutlineColor: parseWidgetStateColor(
              Theme.of(context), widget.control, "trackOutlineColor"),
          trackOutlineWidth:
              parseWidgetStateDouble(widget.control, "trackOutlineWidth"),
          onChanged: !disabled
              ? (bool value) {
                  _onChange(value);
                }
              : null);

      ListTileClicks.of(context)?.notifier.addListener(() {
        _onChange(!_value);
      });

      Widget result = s;
      if (width != null || height != null) {
        result = SizedBox(
          width: width,
          height: height,
          child: FittedBox(
            fit: BoxFit.fill,
            child: result,
          ),
        );
      }
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
                ? Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [result, labelWidget],
                  )
                : Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [labelWidget, result],
                  ),
          ),
        );
      }

      return constrainedControl(context, result, widget.parent, widget.control);
    });
  }
}
