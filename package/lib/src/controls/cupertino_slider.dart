import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/desktop.dart';
import 'create_control.dart';
import 'flet_control_state.dart';

class CupertinoSliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const CupertinoSliderControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled});

  @override
  State<CupertinoSliderControl> createState() => _CupertinoSliderControlState();
}

class _CupertinoSliderControlState extends State<CupertinoSliderControl>
    with FletControlState {
  double _value = 0;
  final _debouncer = Debouncer(milliseconds: isDesktop() ? 10 : 100);

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  void onChange(double value) {
    var svalue = value.toString();
    debugPrint(svalue);
    _value = value;
    var props = {"value": svalue};
    updateControlProps(widget.control.id, props, clientOnly: true);
    _debouncer.run(() {
      updateControlProps(widget.control.id, props);
      sendControlEvent(widget.control.id, "change", '');
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoSliderControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    double min = widget.control.attrDouble("min", 0)!;
    double max = widget.control.attrDouble("max", 1)!;
    int? divisions = widget.control.attrInt("divisions");

    debugPrint("CupertinoSliderControl build: ${widget.control.id}");

    double value = widget.control.attrDouble("value", 0)!;
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

    var cupertinoSlider = CupertinoSlider(
        value: _value,
        min: min,
        max: max,
        divisions: divisions,
        activeColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("activeColor", "")!),
        thumbColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("thumbColor", "")!) ??
            CupertinoColors.white,
        onChanged: !disabled
            ? (double value) {
                onChange(value);
              }
            : null,
        onChangeStart: !disabled
            ? (double value) {
                sendControlEvent(
                    widget.control.id, "change_start", value.toString());
              }
            : null,
        onChangeEnd: !disabled
            ? (double value) {
                sendControlEvent(
                    widget.control.id, "change_end", value.toString());
              }
            : null);

    return constrainedControl(
        context, cupertinoSlider, widget.parent, widget.control);
  }
}
