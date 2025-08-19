import 'package:flutter/cupertino.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class CupertinoSliderControl extends StatefulWidget {
  final Control control;

  CupertinoSliderControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoSliderControl> createState() => _CupertinoSliderControlState();
}

class _CupertinoSliderControlState extends State<CupertinoSliderControl> {
  double _value = 0;
  late FletBackend backend;

  @override
  void dispose() {
    super.dispose();
  }

  void onChange(double value) {
    _value = value;
    var props = {"value": value};
    widget.control.updateProperties(props, notify: true);
    widget.control.triggerEvent("change");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoSliderControl build: ${widget.control.id}");

    double min = widget.control.getDouble("min", 0.0)!;
    double max = widget.control.getDouble("max", 1.0)!;

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

    var cupertinoSlider = CupertinoSlider(
        value: _value,
        min: min,
        max: max,
        divisions: widget.control.getInt("divisions"),
        activeColor: widget.control.getColor("active_color", context),
        thumbColor: widget.control
            .getColor("thumb_color", context, CupertinoColors.white)!,
        onChanged:
            !widget.control.disabled ? (double value) => onChange(value) : null,
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

    return ConstrainedControl(control: widget.control, child: cupertinoSlider);
  }
}
