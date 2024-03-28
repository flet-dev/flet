import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/debouncer.dart';
import '../utils/desktop.dart';
import 'create_control.dart';

class CupertinoSliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CupertinoSliderControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoSliderControl> createState() => _CupertinoSliderControlState();
}

class _CupertinoSliderControlState extends State<CupertinoSliderControl> {
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
    widget.backend.updateControlState(widget.control.id, props, server: false);
    _debouncer.run(() {
      widget.backend.updateControlState(widget.control.id, props);
      widget.backend.triggerControlEvent(widget.control.id, "change");
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
        activeColor: widget.control.attrColor("activeColor", context),
        thumbColor: widget.control.attrColor("thumbColor", context) ??
            CupertinoColors.white,
        onChanged: !disabled
            ? (double value) {
                onChange(value);
              }
            : null,
        onChangeStart: !disabled
            ? (double value) {
                widget.backend.triggerControlEvent(
                    widget.control.id, "change_start", value.toString());
              }
            : null,
        onChangeEnd: !disabled
            ? (double value) {
                widget.backend.triggerControlEvent(
                    widget.control.id, "change_end", value.toString());
              }
            : null);

    return constrainedControl(
        context, cupertinoSlider, widget.parent, widget.control);
  }
}
