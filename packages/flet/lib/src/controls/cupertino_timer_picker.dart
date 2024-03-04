import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
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
    int minuteInterval =
        widget.control.attrDouble("minuteInterval", 1)!.toInt();
    int secondInterval =
        widget.control.attrDouble("secondInterval", 1)!.toInt();
    CupertinoTimerPickerMode mode = CupertinoTimerPickerMode.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            widget.control.attrString("mode", "")!.toLowerCase(),
        orElse: () => CupertinoTimerPickerMode.hms);

    Color? backgroundColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgColor", "")!);

    Widget picker = CupertinoTimerPicker(
      mode: mode,
      initialTimerDuration: initialTimerDuration,
      minuteInterval: minuteInterval,
      secondInterval: secondInterval,
      alignment:
          parseAlignment(widget.control, "alignment") ?? Alignment.center,
      backgroundColor: backgroundColor,
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
