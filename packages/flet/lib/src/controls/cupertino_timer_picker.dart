import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
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

    int value = widget.control.getInt("value", 0)!;

    Widget picker = CupertinoTimerPicker(
      mode: widget.control
          .getCupertinoTimerPickerMode("mode", CupertinoTimerPickerMode.hms)!,
      initialTimerDuration: Duration(seconds: value),
      minuteInterval: widget.control.getInt("minute_interval", 1)!,
      secondInterval: widget.control.getInt("second_interval", 1)!,
      itemExtent: widget.control.getDouble("item_extent", 32.0)!,
      alignment: widget.control.getAlignment("alignment", Alignment.center)!,
      backgroundColor: widget.control.getColor("bgcolor", context),
      onTimerDurationChanged: (Duration d) {
        widget.control.updateProperties({"value": d.inSeconds});
        widget.control.triggerEvent("change", d.inSeconds);
      },
    );

    return ConstrainedControl(control: widget.control, child: picker);
  }
}
