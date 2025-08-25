import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import 'base_controls.dart';

class CupertinoTimerPickerControl extends StatefulWidget {
  final Control control;

  CupertinoTimerPickerControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoTimerPickerControl> createState() =>
      _CupertinoTimerPickerControlState();
}

class _CupertinoTimerPickerControlState
    extends State<CupertinoTimerPickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoTimerPicker build: ${widget.control.id}");

    Widget picker = CupertinoTimerPicker(
      mode: widget.control
          .getCupertinoTimerPickerMode("mode", CupertinoTimerPickerMode.hms)!,
      initialTimerDuration: widget.control
          .getDuration("value", Duration.zero, DurationUnit.seconds)!,
      minuteInterval: widget.control.getInt("minute_interval", 1)!,
      secondInterval: widget.control.getInt("second_interval", 1)!,
      itemExtent: widget.control.getDouble("item_extent", 32.0)!,
      alignment: widget.control.getAlignment("alignment", Alignment.center)!,
      backgroundColor: widget.control.getColor("bgcolor", context),
      onTimerDurationChanged: (duration) {
        // preserve (original) value's type
        final d =
            widget.control.get("value") is int ? duration.inSeconds : duration;
        widget.control.updateProperties({"value": d});
        widget.control.triggerEvent("change", d);
      },
    );

    return LayoutControl(control: widget.control, child: picker);
  }
}
