import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class SliderControl extends StatefulWidget {
  final Control control;

  SliderControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<SliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<SliderControl> {
  double _value = 0;
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

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  void onChange(double value) {
    _value = value;
    var props = {"value": value};
    widget.control.updateProperties(props, notify: true);
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SliderControl build: ${widget.control.id}");

    var label = widget.control.getString("label");
    var min = widget.control.getDouble("min", 0)!;
    var max = widget.control.getDouble("max", 1)!;
    var round = widget.control.getInt("round", 0)!;

    double value = widget.control.getDouble("value", min)!;
    if (_value != value) {
      // verify limits
      if (value < min) {
        _value = min;
      } else if (value > max) {
        _value = max;
      } else {
        _value = value;
      }
    }

    var slider = Slider(
        autofocus: widget.control.getBool("autofocus", false)!,
        focusNode: _focusNode,
        value: _value,
        min: min,
        max: max,
        // todo: remove deprecated property year2023
        // ignore: deprecated_member_use
        year2023: widget.control.getBool("year_2023"),
        divisions: widget.control.getInt("divisions"),
        label: label?.replaceAll("{value}", _value.toStringAsFixed(round)),
        activeColor: widget.control.getColor("active_color", context),
        inactiveColor: widget.control.getColor("inactive_color", context),
        overlayColor: widget.control
            .getWidgetStateColor("overlay_color", Theme.of(context)),
        allowedInteraction: widget.control.getSliderInteraction("interaction"),
        thumbColor: widget.control.getColor("thumb_color", context),
        padding: widget.control.getPadding("padding"),
        onChanged: !widget.control.disabled
            ? (double value) {
                onChange(value);
              }
            : null,
        mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
        secondaryActiveColor:
            widget.control.getColor("secondary_active_color", context),
        secondaryTrackValue: widget.control.getDouble("secondary_track_value"),
        onChangeStart: !widget.control.disabled
            ? (double value) {
                widget.control.triggerEvent("change_start", value);
              }
            : null,
        onChangeEnd: !widget.control.disabled
            ? (double value) {
                widget.control.triggerEvent("change_end", value);
              }
            : null);

    return LayoutControl(control: widget.control, child: slider);
  }
}
