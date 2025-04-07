import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import 'base_controls.dart';

class RangeSliderControl extends StatefulWidget {
  final Control control;

  const RangeSliderControl({
    super.key,
    required this.control,
  });

  @override
  State<RangeSliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<RangeSliderControl> {
  final _debouncer = Debouncer(milliseconds: isDesktopPlatform() ? 10 : 100);

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  void onChange(double startValue, double endValue) {
    var props = {"start_value": startValue, "end_value": endValue};
    FletBackend.of(context)
        .updateControl(widget.control.id, props, python: false, notify: true);
    _debouncer.run(() {
      FletBackend.of(context)
          .updateControl(widget.control.id, props, notify: true);
      widget.control.triggerEvent("change", context);
    });
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
                FletBackend.of(context)
                    .triggerControlEvent(widget.control, "change_start");
              }
            : null,
        onChangeEnd: !widget.control.disabled
            ? (RangeValues newValues) {
                FletBackend.of(context)
                    .triggerControlEvent(widget.control, "change_end");
              }
            : null);

    return ConstrainedControl(control: widget.control, child: rangeSlider);
  }
}
