import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class CupertinoDatePickerControl extends StatefulWidget {
  final Control control;

  const CupertinoDatePickerControl({super.key, required this.control});

  @override
  State<CupertinoDatePickerControl> createState() =>
      _CupertinoDatePickerControlState();
}

class _CupertinoDatePickerControlState
    extends State<CupertinoDatePickerControl> {

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDatePicker build: ${widget.control.id}");

    Widget dialog;
    try {
      dialog = CupertinoDatePicker(
        initialDateTime: widget.control.getDateTime("value"),
        showDayOfWeek: widget.control.getBool("show_day_of_week", false)!,
        minimumDate: widget.control.getDateTime("first_date"),
        maximumDate: widget.control.getDateTime("last_date"),
        backgroundColor: widget.control.getColor("bgcolor", context),
        minimumYear: widget.control.getInt("minimum_year", 1)!,
        maximumYear: widget.control.getInt("maximum_year"),
        itemExtent: widget.control.getDouble("item_extent", 32.0)!,
        minuteInterval: widget.control.getInt("minute_interval", 1)!,
        use24hFormat: widget.control.getBool("use_24h_format", false)!,
        dateOrder: widget.control.getDatePickerDateOrder("date_order"),
        mode: widget.control.getCupertinoDatePickerMode(
            "date_picker_mode", CupertinoDatePickerMode.dateAndTime)!,
        onDateTimeChanged: (DateTime value) {
          widget.control.updateProperties({"value": value});
          widget.control.triggerEvent("change", data: value);
        },
      );
    } catch (e) {
      return ErrorControl("CupertinoDatePicker Error: ${e.toString()}");
    }

    return ConstrainedControl(control: widget.control, child: dialog);
  }
}
