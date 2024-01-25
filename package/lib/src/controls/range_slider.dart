import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/desktop.dart';
import 'create_control.dart';
import 'flet_control_stateful_mixin.dart';

class RangeSliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const RangeSliderControl({
    super.key,
    this.parent,
    required this.control,
    required this.parentDisabled,
  });

  @override
  State<RangeSliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<RangeSliderControl>
    with FletControlStatefulMixin {
  final _debouncer = Debouncer(milliseconds: isDesktop() ? 10 : 100);

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
    updateControlProps(widget.control.id, props, clientOnly: true);
    _debouncer.run(() {
      updateControlProps(widget.control.id, props);
      sendControlEvent(widget.control.id, "change", "");
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("RangeSliderControl build: ${widget.control.id}");

    double startValue = widget.control.attrDouble("startvalue", 0)!;
    double endValue = widget.control.attrDouble("endvalue", 0)!;
    String? label = widget.control.attrString("label");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    double min = widget.control.attrDouble("min", 0)!;
    double max = widget.control.attrDouble("max", 1)!;

    int? divisions = widget.control.attrInt("divisions");
    int round = widget.control.attrInt("round", 0)!;

    debugPrint("SliderControl build: ${widget.control.id}");

    var rangeSlider = RangeSlider(
        values: RangeValues(startValue, endValue),
        labels: RangeLabels(
            (label ?? "")
                .replaceAll("{value}", startValue.toStringAsFixed(round)),
            (label ?? "")
                .replaceAll("{value}", endValue.toStringAsFixed(round))),
        min: min,
        max: max,
        divisions: divisions,
        activeColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("activeColor", "")!),
        inactiveColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("inactiveColor", "")!),
        overlayColor: parseMaterialStateColor(
            Theme.of(context), widget.control, "overlayColor"),
        onChanged: !disabled
            ? (RangeValues newValues) {
                onChange(newValues.start, newValues.end);
              }
            : null,
        onChangeStart: !disabled
            ? (RangeValues newValues) {
                sendControlEvent(widget.control.id, "change_start", '');
              }
            : null,
        onChangeEnd: !disabled
            ? (RangeValues newValues) {
                sendControlEvent(widget.control.id, "change_end", '');
              }
            : null);

    return constrainedControl(
        context, rangeSlider, widget.parent, widget.control);
  }
}
