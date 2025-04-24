import 'package:flutter/cupertino.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import 'base_controls.dart';

class CupertinoSliderControl extends StatefulWidget {
  final Control control;

  const CupertinoSliderControl({
    super.key,
    required this.control,
  });

  @override
  State<CupertinoSliderControl> createState() => _CupertinoSliderControlState();
}

class _CupertinoSliderControlState extends State<CupertinoSliderControl> {
  double _value = 0;
  final _debouncer = Debouncer(milliseconds: isDesktopPlatform() ? 10 : 100);
  late FletBackend backend;

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  void onChange(double value) {
    _value = value;
    _debouncer.run(() {
      widget.control.updateProperties({"value": value}, notify: true);
      widget.control.triggerEvent("change", data: value);
    });
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
        onChangeStart: widget.control.disabled
            ? (double value) {
                backend.triggerControlEvent(widget.control, "change_start",
                    data: value);
              }
            : null,
        onChangeEnd: !widget.control.disabled
            ? (double value) {
                backend.triggerControlEvent(widget.control, "change_end",
                    data: value);
              }
            : null);

    return ConstrainedControl(control: widget.control, child: cupertinoSlider);
  }
}
