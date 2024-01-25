import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/desktop.dart';
import 'create_control.dart';

class RangeSliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final dynamic dispatch;

  const RangeSliderControl({
    super.key,
    this.parent,
    required this.control,
    required this.parentDisabled,
    required this.dispatch,
  });

  @override
  State<RangeSliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<RangeSliderControl> {
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
    var strStartValue = startValue.toString();
    var strEndValue = endValue.toString();

    List<Map<String, String>> props = [
      {
        "i": widget.control.id,
        "startvalue": strStartValue,
        "endvalue": strEndValue
      }
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));

    _debouncer.run(() {
      final server = FletAppServices.of(context).server;
      server.updateControlProps(props: props);
      server.sendPageEvent(
          eventTarget: widget.control.id, eventName: "change", eventData: '');
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

    final server = FletAppServices.of(context).server;

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
                server.sendPageEvent(
                    eventTarget: widget.control.id,
                    eventName: "change_start",
                    eventData: '');
              }
            : null,
        onChangeEnd: !disabled
            ? (RangeValues newValues) {
                server.sendPageEvent(
                    eventTarget: widget.control.id,
                    eventName: "change_end",
                    eventData: '');
              }
            : null);

    return constrainedControl(
        context, rangeSlider, widget.parent, widget.control);
  }
}
