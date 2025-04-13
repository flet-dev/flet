import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import 'base_controls.dart';

class CupertinoTimerPickerControl extends StatefulWidget {
  final Control control;

  const CupertinoTimerPickerControl({super.key, required this.control});

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
      initialTimerDuration: widget.control.getDuration("value", Duration.zero)!,
      minuteInterval: widget.control.getInt("minute_interval", 1)!,
      secondInterval: widget.control.getInt("second_interval", 1)!,
      itemExtent: widget.control.getDouble("item_extent", 32.0)!,
      alignment: widget.control.getAlignment("alignment", Alignment.center)!,
      backgroundColor: widget.control.getColor("bgcolor", context),
      onTimerDurationChanged: (duration) {
        widget.control.updateProperties({
          "value": {
            "days": duration.inDays,
            "hours": duration.inHours % 24,
            "minutes": duration.inMinutes % 60,
            "seconds": duration.inSeconds % 60,
            "milliseconds": duration.inMilliseconds % 1000,
            "microseconds": duration.inMicroseconds % 1000,
          }
        });
        widget.control.triggerEvent("change", duration.inSeconds);
      },
    );

    return ConstrainedControl(control: widget.control, child: picker);
  }
}
