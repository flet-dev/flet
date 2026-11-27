import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';
import 'package:material_ui/material_ui.dart' show TimeOfDay;

import 'utils/theme.dart';

class FluentDatePickerControl extends StatelessWidget {
  final Control control;

  const FluentDatePickerControl({super.key, required this.control});

  void _onChanged(DateTime value) {
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentDatePicker build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        DatePicker(
          selected: control.getDateTime("value"),
          header: control.getString("header"),
          startDate: control.getDateTime("first_date"),
          endDate: control.getDateTime("last_date"),
          showDay: control.getBool("show_day", true)!,
          showMonth: control.getBool("show_month", true)!,
          showYear: control.getBool("show_year", true)!,
          autofocus: control.getBool("autofocus", false)!,
          // fluent_ui disables the picker when onChanged is null.
          onChanged: control.disabled ? null : _onChanged,
        ),
      ),
    );
  }
}

class FluentTimePickerControl extends StatelessWidget {
  final Control control;

  const FluentTimePickerControl({super.key, required this.control});

  void _onChanged(DateTime value) {
    final time = TimeOfDay.fromDateTime(value);
    control.updateProperties({"value": time}, notify: true);
    control.triggerEvent("change", time);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentTimePicker build: ${control.id}");

    final time = control.getTimeOfDay("value");
    final now = DateTime.now();

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        TimePicker(
          // fluent_ui stores a new `selected` time after the frame without
          // rebuilding, so the field would keep showing the old time.
          key: ValueKey(time),
          // fluent_ui works with a DateTime; only its time is used.
          selected: time == null
              ? null
              : DateTime(now.year, now.month, now.day, time.hour, time.minute),
          header: control.getString("header"),
          hourFormat: control.getBool("use_24_hour", false)!
              ? HourFormat.HH
              : HourFormat.h,
          minuteIncrement: control.getInt("minute_increment", 1)!,
          autofocus: control.getBool("autofocus", false)!,
          onChanged: control.disabled ? null : _onChanged,
        ),
      ),
    );
  }
}
