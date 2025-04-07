import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'base_controls.dart';
import 'control_widget.dart';
import 'list_tile.dart';

class SwitchControl extends StatefulWidget {
  final Control control;

  const SwitchControl({
    super.key,
    required this.control,
  });

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
    _value = value;
    var props = {"value": value};
    FletBackend.of(context)
        .updateControl(widget.control.id, props, notify: true);
    FletBackend.of(context).triggerControlEvent(widget.control, "change");
  }

  void _onFocusChange() {
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SwitchControl build: ${widget.control.id}");

    var label = widget.control.get("label");
    LabelPosition labelPosition =
        widget.control.getLabelPosition("label_position", LabelPosition.right)!;
    double? width = widget.control.getDouble("width");
    double? height = widget.control.getDouble("height");
    bool autofocus = widget.control.getBool("autofocus", false)!;

    TextStyle? labelStyle =
        widget.control.getTextStyle("label_style", Theme.of(context));
    if (widget.control.disabled && labelStyle != null) {
      labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
    }

    bool value = widget.control.getBool("value", false)!;
    if (_value != value) {
      _value = value;
    }
    ThemeData theme = Theme.of(context);

    var s = Switch(
        autofocus: autofocus,
        focusNode: _focusNode,
        activeColor: widget.control.getColor("active_color", context),
        activeTrackColor:
            widget.control.getColor("active_track_color", context),
        inactiveThumbColor:
            widget.control.getColor("inactive_thumb_color", context),
        inactiveTrackColor:
            widget.control.getColor("inactive_track_color", context),
        thumbColor: widget.control.getWidgetStateColor("thumb_color", theme),
        thumbIcon: widget.control.getWidgetStateIcon("thumb_icon", theme),
        trackColor: widget.control.getWidgetStateColor("track_color", theme),
        focusColor: widget.control.getColor("focus_color", context),
        value: _value,
        mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
        splashRadius: widget.control.getDouble("splash_radius"),
        hoverColor: widget.control.getColor("hover_color", context),
        overlayColor:
            widget.control.getWidgetStateColor("overlay_color", theme),
        trackOutlineColor:
            widget.control.getWidgetStateColor("track_outline_color", theme),
        trackOutlineWidth:
            widget.control.getWidgetStateDouble("track_outline_width"),
        onChanged: !widget.control.disabled
            ? (bool value) {
                _onChange(value);
              }
            : null);

    ListTileClicks.of(context)?.notifier.addListener(() {
      _onChange(!_value);
    });

    Widget result = s;

    if (label is Control || (label is String)) {
      Widget? labelWidget;
      if (label is Control) {
        labelWidget = ControlWidget(control: label);
      } else {
        labelWidget = widget.control.disabled
            ? Text(label, style: labelStyle)
            : MouseRegion(
                cursor: SystemMouseCursors.click,
                child: Text(label, style: labelStyle));
      }

      result = MergeSemantics(
        child: GestureDetector(
          onTap: !widget.control.disabled
              ? () {
                  _onChange(!_value);
                }
              : null,
          child: labelPosition == LabelPosition.right
              ? Row(
                  // mainAxisSize: MainAxisSize.min,
                  children: [result, labelWidget],
                )
              : Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [labelWidget, result],
                ),
        ),
      );
    }
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

    return ConstrainedControl(control: widget.control, child: result);
    //  });
  }
}
