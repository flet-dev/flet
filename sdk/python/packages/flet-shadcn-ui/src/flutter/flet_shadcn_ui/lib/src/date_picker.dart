import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/dates.dart';
import 'utils/theme.dart';

class ShadDatePickerControl extends StatelessWidget {
  final Control control;

  const ShadDatePickerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadDatePicker build: ${control.id}");

    final value = getDay(control, "value");
    final bounds = DayBounds(control);
    final picker = ShadDatePicker(
      selected: value,
      initialMonth: value != null ? DateTime(value.year, value.month) : null,
      placeholder: control.buildTextOrWidget("placeholder"),
      closeOnSelection: control.getBool("close_on_select", true)!,
      fromMonth: bounds.fromMonth,
      toMonth: bounds.toMonth,
      selectableDayPredicate: bounds.isSelectable,
      enabled: !control.disabled,
      onChanged: (day) {
        control.updateProperties({"value": dayToPython(day)});
        control.triggerEvent("change");
      },
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, picker),
    );
  }
}

class ShadDateRangePickerControl extends StatelessWidget {
  final Control control;

  const ShadDateRangePickerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadDateRangePicker build: ${control.id}");

    final start = getDay(control, "start_value");
    final end = getDay(control, "end_value");
    final bounds = DayBounds(control);
    final picker = ShadDatePicker.range(
      selected: start == null && end == null
          ? null
          : ShadDateTimeRange(start: start, end: end),
      initialMonth: start != null ? DateTime(start.year, start.month) : null,
      numberOfMonths: 2,
      placeholder: control.buildTextOrWidget("placeholder"),
      fromMonth: bounds.fromMonth,
      toMonth: bounds.toMonth,
      selectableDayPredicate: bounds.isSelectable,
      enabled: !control.disabled,
      onRangeChanged: (range) {
        var newStart = range?.start;
        var newEnd = range?.end;
        // Once a range has a start, shadcn_ui moves the end for any later day
        // and the start for any earlier one, so a complete range can never be
        // replaced by clicking. Instead, a click on a complete range starts a
        // new one on the clicked day; the next click sets its end.
        if (start != null && end != null) {
          if (_sameDay(newStart, start) && !_sameDay(newEnd, end)) {
            newStart = newEnd;
            newEnd = null;
          } else if (_sameDay(newEnd, end) && !_sameDay(newStart, start)) {
            newEnd = null;
          }
        }
        control.updateProperties({
          "start_value": dayToPython(newStart),
          "end_value": dayToPython(newEnd),
        }, notify: true);
        control.triggerEvent("change");
      },
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, picker),
    );
  }
}

bool _sameDay(DateTime? a, DateTime? b) => a == null || b == null
    ? a == b
    : a.year == b.year && a.month == b.month && a.day == b.day;
