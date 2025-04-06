import 'package:flet/src/extensions/control.dart';
import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/mouse.dart';
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
    var props = {
      "startvalue": startValue.toString(),
      "endvalue": endValue.toString()
    };
    FletBackend.of(context)
        .updateControl(widget.control.id, props, python: false, notify: true);
    _debouncer.run(() {
      FletBackend.of(context)
          .updateControl(widget.control.id, props, notify: true);
      FletBackend.of(context).triggerControlEvent(widget.control, "change");
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("RangeSliderControl build: ${widget.control.id}");

    double startValue = widget.control.getDouble("startValue", 0)!;
    double endValue = widget.control.getDouble("endValue", 0)!;
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
        mouseCursor:
            parseWidgetStateMouseCursor(widget.control.get("mouse_cursor")),
        overlayColor: parseWidgetStateColor(
            widget.control.get("overlay_color"), Theme.of(context)),
        onChanged: widget.control.disabled
            ? null
            : (RangeValues newValues) {
                onChange(newValues.start, newValues.end);
              },
        onChangeStart: widget.control.disabled
            ? null
            : (RangeValues newValues) {
                FletBackend.of(context)
                    .triggerControlEvent(widget.control, "change_start");
              },
        onChangeEnd: widget.control.disabled
            ? null
            : (RangeValues newValues) {
                FletBackend.of(context)
                    .triggerControlEvent(widget.control, "change_end");
              });

    return ConstrainedControl(control: widget.control, child: rangeSlider);
  }
}
