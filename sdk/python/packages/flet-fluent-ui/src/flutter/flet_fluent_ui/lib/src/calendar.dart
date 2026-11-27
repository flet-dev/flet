import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

/// A `CalendarView`, or a `CalendarDatePicker` when [picker] is true.
class FluentCalendarControl extends StatefulWidget {
  final Control control;
  final bool picker;

  const FluentCalendarControl({
    super.key,
    required this.control,
    this.picker = false,
  });

  @override
  State<FluentCalendarControl> createState() => _FluentCalendarControlState();
}

class _FluentCalendarControlState extends State<FluentCalendarControl> {
  // fluent_ui's calendar keeps the selection itself, starting from
  // `initialStart` and `initialEnd`; changing them later replaces the
  // selection (losing the dates of a multiple selection). So they keep the
  // values the calendar was created with, and the calendar is created again,
  // with a new key, only when Python selects other dates than it shows.
  int _generation = 0;
  // The selection the calendar shows, as `value` and `end_value`.
  (DateTime?, DateTime?)? _shown;
  // The selection the calendar was created with.
  (DateTime?, DateTime?) _initial = (null, null);
  String? _shownMode;

  Control get control => widget.control;

  void _onSelectionChanged(CalendarSelectionData data) {
    _shown = (data.startDate, data.endDate);
    // Not `notify`: fluent_ui also reports changes while it is being rebuilt.
    control.updateProperties({
      "value": data.startDate,
      if (!widget.picker) "end_value": data.endDate,
    });
    control.triggerEvent(
      "change",
      widget.picker ? null : {"selected_dates": data.selectedDates},
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentCalendar build: ${control.id}");

    final start = control.getDateTime("value");
    final end = widget.picker ? null : control.getDateTime("end_value");
    final mode = control.getString("selection_mode");
    if (_shown != (start, end) || _shownMode != mode) {
      if (_shown != null) _generation++;
      _shown = (start, end);
      _initial = (start, end);
      _shownMode = mode;
    }

    final blackoutDates = control
        .get<List>("blackout_dates", const [])!
        .whereType<DateTime>()
        .map((date) => date.toLocal())
        .toList();
    bool isBlackout(DateTime date) => blackoutDates.any(
      (d) => d.year == date.year && d.month == date.month && d.day == date.day,
    );

    final key = ValueKey(_generation);
    final initialStart = _initial.$1;
    // fluent_ui asserts that the start is before the end.
    final initialEnd =
        _initial.$2 != null &&
            initialStart != null &&
            _initial.$2!.isAfter(initialStart)
        ? _initial.$2
        : null;
    final onSelectionChanged = control.disabled ? null : _onSelectionChanged;
    final minDate = control.getDateTime("first_date");
    final maxDate = control.getDateTime("last_date");
    final blackoutRule = blackoutDates.isEmpty ? null : isBlackout;
    final selectionColor = control.getColor("selection_color", context);
    final firstDayOfWeek = control.getInt("first_day_of_week");
    final isTodayHighlighted = control.getBool("highlight_today", true)!;

    final Widget calendar = widget.picker
        ? CalendarDatePicker(
            key: key,
            initialStart: initialStart,
            onSelectionChanged: onSelectionChanged,
            minDate: minDate,
            maxDate: maxDate,
            blackoutRule: blackoutRule,
            selectionColor: selectionColor,
            firstDayOfWeek: firstDayOfWeek,
            isTodayHighlighted: isTodayHighlighted,
            placeholderText: control.getString("placeholder"),
            closeOnSelection: control.getBool("close_on_selection", true)!,
          )
        : CalendarView(
            key: key,
            initialStart: initialStart,
            initialEnd: initialEnd,
            onSelectionChanged: onSelectionChanged,
            minDate: minDate,
            maxDate: maxDate,
            blackoutRule: blackoutRule,
            selectionColor: selectionColor,
            firstDayOfWeek: firstDayOfWeek,
            isTodayHighlighted: isTodayHighlighted,
            selectionMode: parseEnum(
              CalendarViewSelectionMode.values,
              mode,
              CalendarViewSelectionMode.single,
            )!,
            initialDisplayMode: parseEnum(
              CalendarViewDisplayMode.values,
              control.getString("display_mode"),
              CalendarViewDisplayMode.month,
            )!,
          );

    return LayoutControl(
      control: control,
      child: withFluentTheme(context, calendar),
    );
  }
}
