import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:table_calendar/table_calendar.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_children_view_model.dart';
import '../protocol/update_control_props_payload.dart';

class TableCalendarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const TableCalendarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<TableCalendarControl> createState() => _TableCalendarControlState();
}

class _TableCalendarControlState extends State<TableCalendarControl> {
  final ValueNotifier<List<Event>> _selectedEvents = ValueNotifier([]);

  DateTime? _focusedDay;
  DateTime? _selectedDay;
  DateTime? _rangeStart;
  DateTime? _rangeEnd;

  @override
  void initState() {
    super.initState();
    _focusedDay = widget.control.attrDateTime("focusedDay") ?? kToday;
    _selectedDay = widget.control.attrDateTime("focusedDay") ?? _focusedDay;
  }

  @override
  void dispose() {
    _selectedEvents.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TableCalendar build: ${widget.control.id}");

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          return StoreConnector<AppState, ControlChildrenViewModel>(
              distinct: true,
              converter: (store) => ControlChildrenViewModel.fromStore(
                  store, widget.control.id,
                  dispatch: store.dispatch),
              builder: (context, itemsView) {
                debugPrint(
                    "TableCalendar StoreConnector build: ${widget.control.id}");

                DateTime firstDay =
                    widget.control.attrDateTime("firstDay") ?? kFirstDay;
                DateTime lastDay =
                    widget.control.attrDateTime("lastDay") ?? kLastDay;
                DateTime? currentDay =
                    widget.control.attrDateTime("currentDay");

                bool onDaySelected =
                    widget.control.attrBool("onDaySelected", false)!;
                bool onRangeSelected =
                    widget.control.attrBool("onRangeSelected", false)!;
                bool onFormatChanged =
                    widget.control.attrBool("onFormatChange", false)!;
                bool onPageChanged =
                    widget.control.attrBool("onPageChanged", false)!;

                String? localeString = widget.control.attrString("locale");
                CalendarFormat calendarFormat = parseCalendarFormat(
                    widget.control.attrString("calendarFormat", "")!);
                RangeSelectionMode rangeSelectionMode = parseRangeSelectionMode(
                    widget.control
                        .attrString("rangeSelectionMode", "toggledoff")!);

                // locale isn't supported yet in Flet
                Locale locale;
                if (localeString == null) {
                  locale = Localizations.localeOf(context);
                } else {
                  locale = Locale(localeString);
                }

                var events = itemsView.children
                    .where((c) => c.name == null)
                    .map<Event>((Control itemCtrl) {
                      return Event(
                          itemCtrl.attrs["key"],
                          itemCtrl.attrs["label"],
                          itemCtrl.attrDateTime("date"));
                    })
                    .where((e) => e.key != null && e.date != null)
                    .toList();

                LinkedHashMap kEvents = LinkedHashMap<DateTime, List<Event>>(
                  equals: isSameDay,
                  hashCode: getHashCode,
                );
                for (var event in events) {
                  var day = DateTime.utc(
                      event.date!.year, event.date!.month, event.date!.day);
                  kEvents[day].add(event);
                }

                List<Event> _getEventsForDay(DateTime day) {
                  return kEvents[day] ?? [];
                }

                List<Event> _getEventsForRange(DateTime start, DateTime end) {
                  // Implementation example
                  final days = daysInRange(start, end);

                  return [
                    for (final d in days) ..._getEventsForDay(d),
                  ];
                }

                void _onDaySelected(DateTime selectedDay, DateTime focusedDay) {
                  if (!isSameDay(_selectedDay, selectedDay)) {
                    setState(() {
                      _selectedDay = selectedDay;
                      _focusedDay = focusedDay;
                      _rangeStart = null; // Important to clean those
                      _rangeEnd = null;
                    });

                    _selectedEvents.value = _getEventsForDay(selectedDay);
                  }

                  String modeValue = RangeSelectionMode.toggledOff.toString();
                  List<Map<String, String>> props = [
                    {"i": widget.control.id, "rangeSelectionMode": modeValue}
                  ];
                  dispatch(UpdateControlPropsAction(
                      UpdateControlPropsPayload(props: props)));
                  FletAppServices.of(context)
                      .server
                      .updateControlProps(props: props);

                  String stringValue = selectedDay.toIso8601String();
                  if (onDaySelected) {
                    FletAppServices.of(context).server.sendPageEvent(
                        eventTarget: widget.control.id,
                        eventName: "daySelected",
                        eventData: stringValue);
                  }
                }

                void _onRangeSelected(
                    DateTime? start, DateTime? end, DateTime focusedDay) {
                  setState(() {
                    _selectedDay = null;
                    _focusedDay = focusedDay;
                    _rangeStart = start;
                    _rangeEnd = end;
                  });

                  String stringValue = RangeSelectionMode.toggledOn.toString();
                  List<Map<String, String>> props = [
                    {"i": widget.control.id, "rangeSelectionMode": stringValue}
                  ];
                  dispatch(UpdateControlPropsAction(
                      UpdateControlPropsPayload(props: props)));
                  FletAppServices.of(context)
                      .server
                      .updateControlProps(props: props);

                  // `start` or `end` could be null
                  if (start != null && end != null) {
                    _selectedEvents.value = _getEventsForRange(start, end);

                    String stringValue =
                        "${start.toIso8601String()},${end.toIso8601String()}";

                    if (onRangeSelected) {
                      FletAppServices.of(context).server.sendPageEvent(
                          eventTarget: widget.control.id,
                          eventName: "rangeSelected",
                          eventData: stringValue);
                    }
                  } else if (start != null) {
                    _selectedEvents.value = _getEventsForDay(start);
                  } else if (end != null) {
                    _selectedEvents.value = _getEventsForDay(end);
                  }
                }

                void _onFormatChanged(format) {
                  String stringValue = format.toString();
                  List<Map<String, String>> props = [
                    {"i": widget.control.id, "calendarFormat": stringValue}
                  ];
                  dispatch(UpdateControlPropsAction(
                      UpdateControlPropsPayload(props: props)));
                  FletAppServices.of(context)
                      .server
                      .updateControlProps(props: props);
                  if (onFormatChanged) {
                    FletAppServices.of(context).server.sendPageEvent(
                        eventTarget: widget.control.id,
                        eventName: "formatChange",
                        eventData: stringValue);
                  }
                }

                void _onPageChanged(focusedDay) {
                  _focusedDay = focusedDay;
                  String stringValue = focusedDay.toIso8601String() ?? "";
                  if (onPageChanged) {
                    FletAppServices.of(context).server.sendPageEvent(
                        eventTarget: widget.control.id,
                        eventName: "pageChanged",
                        eventData: stringValue);
                  }
                }

                return TableCalendar(
                  firstDay: firstDay,
                  lastDay: lastDay,
                  focusedDay: _focusedDay!,
                  currentDay: currentDay,
                  // locale isn't supported yet in Flet
                  // locale: locale,
                  selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
                  rangeStartDay: _rangeStart,
                  rangeEndDay: _rangeEnd,
                  calendarFormat: calendarFormat,
                  rangeSelectionMode: rangeSelectionMode,
                  eventLoader: _getEventsForDay,
                  startingDayOfWeek: StartingDayOfWeek.monday,
                  calendarStyle: const CalendarStyle(
                    // Use `CalendarStyle` to customize the UI
                    outsideDaysVisible: false,
                  ),
                  onDaySelected: _onDaySelected,
                  onRangeSelected: _onRangeSelected,
                  onFormatChanged: _onFormatChanged,
                  onPageChanged: _onPageChanged,
                  // just turn off select format in widget
                  availableCalendarFormats: {calendarFormat: ""},
                );
              });
        });
  }
}

CalendarFormat parseCalendarFormat(String format) {
  switch (format.toLowerCase()) {
    case "month":
      return CalendarFormat.month;
    case "twoweeks":
      return CalendarFormat.twoWeeks;
    case "week":
      return CalendarFormat.week;
  }
  return CalendarFormat.month;
}

RangeSelectionMode parseRangeSelectionMode(String mode) {
  switch (mode.toLowerCase()) {
    case "disabled":
      return RangeSelectionMode.disabled;
    case "toggledoff":
      return RangeSelectionMode.toggledOff;
    case "toggledon":
      return RangeSelectionMode.toggledOn;
    case "enforced":
      return RangeSelectionMode.enforced;
  }
  return RangeSelectionMode.toggledOff;
}

class Event {
  final String? key;
  final String? label;
  final DateTime? date;

  const Event(this.key, this.label, this.date);

  @override
  String toString() => label ?? key ?? "";
}

int getHashCode(DateTime key) {
  return key.day * 1000000 + key.month * 10000 + key.year;
}

/// Returns a list of [DateTime] objects from [first] to [last], inclusive.
List<DateTime> daysInRange(DateTime first, DateTime last) {
  final dayCount = last.difference(first).inDays + 1;
  return List.generate(
    dayCount,
    (index) => DateTime.utc(first.year, first.month, first.day + index),
  );
}

final kToday = DateTime.now();
final kFirstDay = DateTime(kToday.year, kToday.month - 3, kToday.day);
final kLastDay = DateTime(kToday.year, kToday.month + 3, kToday.day);
