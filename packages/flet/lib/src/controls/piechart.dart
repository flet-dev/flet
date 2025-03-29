import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';

import '../flet_control_backend.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/text.dart';
import 'create_control.dart';

const eventMap = {
  "FlPointerEnterEvent": "pointerEnter",
  "FlPointerExitEvent": "pointerExit",
  "FlPointerHoverEvent": "pointerHover",
  "FlPanCancelEvent": "panCancel",
  "FlPanDownEvent": "panDown",
  "FlPanEndEvent": "panEnd",
  "FlPanStartEvent": "panStart",
  "FlPanUpdateEvent": "panUpdate",
  "FlLongPressEnd": "longPressEnd",
  "FlLongPressMoveUpdate": "longPressMoveUpdate",
  "FlLongPressStart": "longPressStart",
  "FlTapCancelEvent": "tapCancel",
  "FlTapDownEvent": "tapDown",
  "FlTapUpEvent": "tapUp",
};

class PieChartEventData extends Equatable {
  final String eventType;
  final int? sectionIndex;
  final Offset? localPosition;

  const PieChartEventData(
      {required this.eventType,
      required this.sectionIndex,
      this.localPosition});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'type': eventType,
        'section_index': sectionIndex,
        "lx": localPosition?.dx,
        "ly": localPosition?.dy
      };

  @override
  List<Object?> get props => [eventType, sectionIndex];
}

class PieChartSectionViewModel extends Equatable {
  final Control control;
  final Control? badge;

  const PieChartSectionViewModel({required this.control, required this.badge});

  static PieChartSectionViewModel fromStore(
      Store<AppState> store, Control control) {
    var children = store.state.controls[control.id]!.childIds
        .map((childId) => store.state.controls[childId])
        .nonNulls
        .where((c) => c.visible);

    return PieChartSectionViewModel(
        control: control,
        badge: children.firstWhereOrNull((c) => c.name == "badge"));
  }

  @override
  List<Object?> get props => [control, badge];
}

class PieChartViewModel extends Equatable {
  final Control control;
  final List<PieChartSectionViewModel> sections;

  const PieChartViewModel({required this.control, required this.sections});

  static PieChartViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    return PieChartViewModel(
        control: control,
        sections: children
            .where((c) => c.type == "section" && c.visible)
            .map((c) => PieChartSectionViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, sections];
}

class PieChartControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const PieChartControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<PieChartControl> createState() => _PieChartControlState();
}

class _PieChartControlState extends State<PieChartControl> {
  PieChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("PieChart build: ${widget.control.id}");

    var animate = parseAnimation(widget.control, "animate");

    var result = StoreConnector<AppState, PieChartViewModel>(
        distinct: true,
        converter: (store) =>
            PieChartViewModel.fromStore(store, widget.control, widget.children),
        builder: (context, viewModel) {
          List<PieChartSectionData> sections = viewModel.sections
              .map((g) => getSectionData(Theme.of(context), widget.control, g))
              .toList();

          Widget chart = PieChart(
            PieChartData(
              centerSpaceColor:
                  widget.control.getColor("centerSpaceColor", context),
              centerSpaceRadius: widget.control.getDouble("centerSpaceRadius"),
              sectionsSpace: widget.control.getDouble("sectionsSpace"),
              startDegreeOffset: widget.control.getDouble("startDegreeOffset"),
              pieTouchData: PieTouchData(
                enabled: true,
                touchCallback: widget.control.getBool("onChartEvent", false)!
                    ? (FlTouchEvent evt, PieTouchResponse? resp) {
                        var type = evt.toString();
                        var eventData = PieChartEventData(
                          // grab the event type found in between '' quotes
                          eventType: eventMap[type.substring(
                                  type.indexOf("'") + 1,
                                  type.lastIndexOf("'"))] ??
                              "undefined",
                          sectionIndex:
                              resp?.touchedSection?.touchedSectionIndex,
                          localPosition: evt.localPosition,
                        );
                        if (eventData != _eventData) {
                          _eventData = eventData;
                          debugPrint(
                              "PieChart ${widget.control.id} ${eventData.eventType}");
                          widget.backend.triggerControlEvent(widget.control.id,
                              "chart_event", json.encode(eventData));
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

          return LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
            return (constraints.maxHeight == double.infinity)
                ? ConstrainedBox(
                    constraints: const BoxConstraints(maxHeight: 300),
                    child: chart,
                  )
                : chart;
          });
        });

    return constrainedControl(context, result, widget.parent, widget.control);
  }

  PieChartSectionData getSectionData(ThemeData theme, Control parent,
      PieChartSectionViewModel sectionViewModel) {
    return PieChartSectionData(
      value: sectionViewModel.control.getDouble("value"),
      color: sectionViewModel.control.getColor("color", context),
      radius: sectionViewModel.control.getDouble("radius"),
      showTitle: sectionViewModel.control.getString("title", "")! != "",
      title: sectionViewModel.control.getString("title"),
      titleStyle: parseTextStyle(
          Theme.of(context), sectionViewModel.control, "titleStyle"),
      borderSide:
          parseBorderSide(theme, sectionViewModel.control, "borderSide") ??
              BorderSide.none,
      titlePositionPercentageOffset:
          sectionViewModel.control.getDouble("titlePosition"),
      badgeWidget: sectionViewModel.badge != null
          ? createControl(sectionViewModel.control, sectionViewModel.badge!.id,
              sectionViewModel.control.disabled)
          : null,
      badgePositionPercentageOffset:
          sectionViewModel.control.getDouble("badgePosition"),
    );
  }
}
