import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';

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

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.attrBool("open", false)!;
    bool showDayOfWeek = widget.control.attrBool("showDayOfWeek", false)!;
    Color? bgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgcolor", "")!);
    DateTime? value = widget.control.attrDateTime("value");
    DateTime? firstDate = widget.control.attrDateTime("firstDate");
    DateTime? lastDate = widget.control.attrDateTime("lastDate");
    DateTime? currentDate = widget.control.attrDateTime("currentDate");
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

    void onClosed(DateTime? dateValue) {
      String stringValue;
      String eventName;
      if (dateValue == null) {
        stringValue =
            value?.toIso8601String() ?? currentDate?.toIso8601String() ?? "";
        eventName = "dismiss";
      } else {
        stringValue = dateValue.toIso8601String();
        eventName = "change";
      }
      widget.control.state["open"] = false;
      widget.backend.updateControlState(
          widget.control.id, {"value": stringValue, "open": "false"});
      widget.backend
          .triggerControlEvent(widget.control.id, eventName, stringValue);
    }

    Widget createSelectDateDialog() {
      Widget dialog = CupertinoDatePicker(
        initialDateTime: value ?? currentDate,
        showDayOfWeek: showDayOfWeek,
        minimumDate: firstDate ?? DateTime(1900),
        maximumDate: lastDate ?? DateTime(2050),
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

      return dialog;
    }

    if (open && (open != lastOpen)) {
      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<DateTime>(
            useRootNavigator: false,
            context: context,
            builder: (context) => createSelectDateDialog()).then((result) {
          debugPrint("pickDate() completed");
          onClosed(result);
        });
      });
    }
    return const SizedBox.shrink();
  }
}
