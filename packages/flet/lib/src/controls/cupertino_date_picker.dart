import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoDatePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CupertinoDatePickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoDatePickerControl> createState() =>
      _CupertinoDatePickerControlState();
}

class _CupertinoDatePickerControlState
    extends State<CupertinoDatePickerControl> {
  static const double _kItemExtent = 32.0;

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDatePicker build: ${widget.control.id}");

    Widget dialog;
    try {
      dialog = CupertinoDatePicker(
        initialDateTime:  widget.control.attrDateTime("value"),
        showDayOfWeek: widget.control.attrBool("showDayOfWeek", false)!,
        minimumDate: widget.control.attrDateTime("firstDate"),
        maximumDate: widget.control.attrDateTime("lastDate"),
        backgroundColor: widget.control.attrColor("bgcolor", context),
        minimumYear: widget.control.attrInt("minimumYear", 1)!,
        maximumYear: widget.control.attrInt("maximumYear"),
        itemExtent: widget.control.attrDouble("itemExtent", _kItemExtent)!,
        minuteInterval: widget.control.attrInt("minuteInterval", 1)!,
        use24hFormat: widget.control.attrBool("use24hFormat", false)!,
        dateOrder:
            parseDatePickerDateOrder(widget.control.attrString("dateOrder")),
        mode: parseCupertinoDatePickerMode(
            widget.control.attrString("datePickerMode"),
            CupertinoDatePickerMode.dateAndTime)!,
        onDateTimeChanged: (DateTime value) {
          String stringValue = value.toIso8601String();
          widget.backend
              .updateControlState(widget.control.id, {"value": stringValue});
          widget.backend
              .triggerControlEvent(widget.control.id, "change", stringValue);
        },
      );
    } catch (e) {
      return ErrorControl("CupertinoDatePicker Error: ${e.toString()}");
    }

    return constrainedControl(context, dialog, widget.parent, widget.control);
  }
}
