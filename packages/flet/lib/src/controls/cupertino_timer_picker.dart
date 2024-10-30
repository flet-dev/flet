import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/others.dart';
import 'create_control.dart';

class CupertinoTimerPickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  final FletControlBackend backend;

  const CupertinoTimerPickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoTimerPickerControl> createState() =>
      _CupertinoTimerPickerControlState();
}

class _CupertinoTimerPickerControlState
    extends State<CupertinoTimerPickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoTimerPicker build: ${widget.control.id}");

    int value = widget.control.attrInt("value", 0)!;
    Duration initialTimerDuration = Duration(seconds: value);

    Widget picker = CupertinoTimerPicker(
      mode: parseCupertinoTimerPickerMode(
          widget.control.attrString("mode"), CupertinoTimerPickerMode.hms)!,
      initialTimerDuration: initialTimerDuration,
      minuteInterval: widget.control.attrInt("minuteInterval", 1)!,
      secondInterval: widget.control.attrInt("secondInterval", 1)!,
      itemExtent: widget.control.attrDouble("itemExtent", 32.0)!,
      alignment: parseAlignment(widget.control, "alignment", Alignment.center)!,
      backgroundColor: widget.control.attrColor("bgColor", context),
      onTimerDurationChanged: (Duration d) {
        widget.backend.updateControlState(
            widget.control.id, {"value": d.inSeconds.toString()});
        widget.backend.triggerControlEvent(
            widget.control.id, "change", d.inSeconds.toString());
      },
    );

    return constrainedControl(context, picker, widget.parent, widget.control);
  }
}
