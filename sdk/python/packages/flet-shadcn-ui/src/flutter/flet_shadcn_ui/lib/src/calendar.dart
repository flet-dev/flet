import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/dates.dart';
import 'utils/intrinsics.dart';
import 'utils/theme.dart';

class ShadCalendarControl extends StatefulWidget {
  final Control control;

  const ShadCalendarControl({super.key, required this.control});

  @override
  State<ShadCalendarControl> createState() => _ShadCalendarControlState();
}

class _ShadCalendarControlState extends State<ShadCalendarControl> {
  DateTime? _value;
  // ShadCalendar ignores `selected` becoming null, so clearing the value
  // from Python rebuilds it under a new key.
  int _generation = 0;

  void _onChanged(DateTime? day) {
    _value = day;
    widget.control.updateProperties({"value": dayToPython(day)});
    widget.control.triggerEvent("change");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadCalendar build: ${widget.control.id}");

    final control = widget.control;
    final value = getDay(control, "value");
    if (value != _value) {
      if (value == null) _generation++;
      _value = value;
    }

    final bounds = DayBounds(control);
    final calendar = ShadCalendar(
      key: ValueKey(_generation),
      selected: value,
      initialMonth: value != null ? DateTime(value.year, value.month) : null,
      fromMonth: bounds.fromMonth,
      toMonth: bounds.toMonth,
      selectableDayPredicate: bounds.isSelectable,
      numberOfMonths: control.getInt("number_of_months", 1)!,
      showOutsideDays: control.getBool("show_outside_days", true)!,
      showWeekNumbers: control.getBool("show_week_numbers", false)!,
      onChanged: control.disabled ? null : _onChanged,
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        MeasuredIntrinsics(
          // One month is about 280x330 with the default theme.
          estimate: Size(280.0 * control.getInt("number_of_months", 1)!, 330),
          child: calendar,
        ),
      ),
    );
  }
}
