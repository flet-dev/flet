import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
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

    bool showDayOfWeek = widget.control.attrBool("showDayOfWeek", false)!;
    Color? bgcolor = widget.control.attrColor("bgcolor", context);
    DateTime? value = widget.control.attrDateTime("value");
    DateTime? firstDate = widget.control.attrDateTime("firstDate");
    DateTime? lastDate = widget.control.attrDateTime("lastDate");
    int minimumYear = widget.control.attrInt("minimumYear", 1)!;
    int? maximumYear = widget.control.attrInt("maximumYear");
    double itemExtent = widget.control.attrDouble("itemExtent", _kItemExtent)!;
    int minuteInterval = widget.control.attrInt("minuteInterval", 1)!;
    bool use24hFormat = widget.control.attrBool("use24hFormat", false)!;

    DatePickerDateOrder? dateOrder = DatePickerDateOrder.values
        .firstWhereOrNull((a) =>
            a.name.toLowerCase() ==
            widget.control.attrString("dateOrder", "")!.toLowerCase());
    CupertinoDatePickerMode datePickerMode = CupertinoDatePickerMode.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control.attrString("datePickerMode", "")!.toLowerCase(),
            orElse: () => CupertinoDatePickerMode.dateAndTime);

    Widget dialog;
    try {
      dialog = CupertinoDatePicker(
        initialDateTime: value,
        showDayOfWeek: showDayOfWeek,
        minimumDate: firstDate,
        maximumDate: lastDate,
        backgroundColor: bgcolor,
        minimumYear: minimumYear,
        maximumYear: maximumYear,
        itemExtent: itemExtent,
        minuteInterval: minuteInterval,
        use24hFormat: use24hFormat,
        dateOrder: dateOrder,
        mode: datePickerMode,
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
