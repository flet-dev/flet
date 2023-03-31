import 'dart:convert';

import 'package:fl_chart/fl_chart.dart';
import 'package:flet/src/models/piechart_section_view_model.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/piechart_event_data.dart';
import '../models/piechart_view_model.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/text.dart';
import 'create_control.dart';

class PieChartControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const PieChartControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<PieChartControl> createState() => _PieChartControlState();
}

class _PieChartControlState extends State<PieChartControl> {
  PieChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("PieChart build: ${widget.control.id}");

    var animate = parseAnimation(widget.control, "animate");
    var border = parseBorder(Theme.of(context), widget.control, "border");

    return StoreConnector<AppState, PieChartViewModel>(
        distinct: true,
        converter: (store) =>
            PieChartViewModel.fromStore(store, widget.control, widget.children),
        builder: (context, viewModel) {
          var interactive = viewModel.control.attrBool("interactive", true)!;

          List<PieChartSectionData> sections = viewModel.sections
              .map((g) => getSectionData(
                  Theme.of(context), widget.control, interactive, g))
              .toList();

          var chart = PieChart(
            PieChartData(
              centerSpaceColor: HexColor.fromString(Theme.of(context),
                  widget.control.attrString("centerSpaceColor", "")!),
              centerSpaceRadius: widget.control.attrDouble("centerSpaceRadius"),
              sectionsSpace: widget.control.attrDouble("sectionsSpace"),
              startDegreeOffset: widget.control.attrDouble("startDegreeOffset"),
              borderData: border != null
                  ? FlBorderData(show: true, border: border)
                  : FlBorderData(show: false),
              pieTouchData: PieTouchData(
                enabled: interactive,
                touchCallback: widget.control.attrBool("onChartEvent", false)!
                    ? (evt, resp) {
                        var eventData = resp != null &&
                                resp.touchedSection != null
                            ? PieChartEventData(
                                eventType: evt.runtimeType
                                    .toString()
                                    .substring(2), // remove "Fl"
                                sectionIndex:
                                    resp.touchedSection!.touchedSectionIndex)
                            : PieChartEventData(
                                eventType: evt.runtimeType
                                    .toString()
                                    .substring(2), // remove "Fl"
                                sectionIndex: null);
                        if (eventData != _eventData) {
                          _eventData = eventData;
                          debugPrint(
                              "PieChart ${widget.control.id} ${eventData.eventType}");
                          FletAppServices.of(context).server.sendPageEvent(
                              eventTarget: widget.control.id,
                              eventName: "chart_event",
                              eventData: json.encode(eventData));
                        }
                      }
                    : null,
              ),
              sections: sections,
            ),
            swapAnimationDuration: animate != null
                ? animate.duration
                : const Duration(milliseconds: 150), // Optional
            swapAnimationCurve: animate != null ? animate.curve : Curves.linear,
          );

          return constrainedControl(
              context, chart, widget.parent, widget.control);
        });
  }

  PieChartSectionData getSectionData(ThemeData theme, Control parent,
      bool interactiveChart, PieChartSectionViewModel sectionViewModel) {
    return PieChartSectionData(
      value: sectionViewModel.control.attrDouble("value"),
      color: HexColor.fromString(
          Theme.of(context), sectionViewModel.control.attrString("color", "")!),
      radius: sectionViewModel.control.attrDouble("radius"),
      showTitle: sectionViewModel.control.attrBool("showTitle"),
      title: sectionViewModel.control.attrString("title"),
      titleStyle: parseTextStyle(
          Theme.of(context), sectionViewModel.control, "titleStyle"),
      borderSide:
          parseBorderSide(theme, sectionViewModel.control, "borderSide"),
      titlePositionPercentageOffset:
          sectionViewModel.control.attrDouble("titlePosition"),
      badgeWidget: sectionViewModel.badge != null
          ? createControl(sectionViewModel.control, sectionViewModel.badge!.id,
              sectionViewModel.control.isDisabled)
          : null,
      badgePositionPercentageOffset:
          sectionViewModel.control.attrDouble("badgePosition"),
    );
  }
}
