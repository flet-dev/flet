import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class RangeSliderControl extends StatefulWidget {
  final Control control;

  RangeSliderControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<RangeSliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<RangeSliderControl> {
  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  void onChange(double startValue, double endValue) {
    var props = {"start_value": startValue, "end_value": endValue};
    widget.control.updateProperties(props, notify: true);
    widget.control.triggerEvent("change");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("RangeSliderControl build: ${widget.control.id}");

    double startValue = widget.control.getDouble("start_value", 0)!;
    double endValue = widget.control.getDouble("end_value", 0)!;
    String label = widget.control.getString("label", "")!;

    double min = widget.control.getDouble("min", 0)!;
    double max = widget.control.getDouble("max", 1)!;

    int round = widget.control.getInt("round", 0)!;

    debugPrint("SliderControl build: ${widget.control.id}");

    var rangeSlider = RangeSlider(
        values: RangeValues(startValue, endValue),
        labels: RangeLabels(
            (label).replaceAll("{value}", startValue.toStringAsFixed(round)),
            (label).replaceAll("{value}", endValue.toStringAsFixed(round))),
        min: min,
        max: max,
        divisions: widget.control.getInt("divisions"),
        activeColor: widget.control.getColor("active_color", context),
        inactiveColor: widget.control.getColor("inactive_color", context),
        mouseCursor: widget.control.getWidgetStateMouseCursor("mouse_cursor"),
        overlayColor: widget.control
            .getWidgetStateColor("overlay_color", Theme.of(context)),
        onChanged: !widget.control.disabled
            ? (RangeValues newValues) {
                onChange(newValues.start, newValues.end);
              }
            : null,
        onChangeStart: !widget.control.disabled
            ? (RangeValues newValues) {
                widget.control.triggerEvent("change_start");
              }
            : null,
        onChangeEnd: !widget.control.disabled
            ? (RangeValues newValues) {
                widget.control.triggerEvent("change_end");
              }
            : null);

    return LayoutControl(control: widget.control, child: rangeSlider);
  }
}
