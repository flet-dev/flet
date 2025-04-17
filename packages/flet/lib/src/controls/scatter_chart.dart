import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/animations.dart';
import 'package:flet/src/utils/borders.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/edge_insets.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flet/src/utils/time.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/charts.dart';
import '../utils/text.dart';
import 'base_controls.dart';

/// Data sent back when the user interacts with the chart.
class ScatterChartEventData extends Equatable {
  final String eventType;
  final int? spotIndex;

  const ScatterChartEventData({required this.eventType, this.spotIndex});

  Map<String, dynamic> toJson() => {'type': eventType, 'spot_index': spotIndex};

  @override
  List<Object?> get props => [eventType, spotIndex];
}

/// Renders a ScatterChart control backed by Flet's runtime data model.
class ScatterChartControl extends StatefulWidget {
  final Control control;

  const ScatterChartControl({super.key, required this.control});

  @override
  State<ScatterChartControl> createState() => _ScatterChartControlState();
}

class _ScatterChartControlState extends State<ScatterChartControl> {
  @override
  Widget build(BuildContext context) {
    var animate = widget.control.getAnimation("animate");
    var border = widget.control.getBorder("border", Theme.of(context));

    var leftTitles = getAxisTitles(widget.control.child("left_axis"));
    var topTitles = getAxisTitles(widget.control.child("top_axis"));
    var rightTitles = getAxisTitles(widget.control.child("right_axis"));
    var bottomTitles = getAxisTitles(widget.control.child("bottom_axis"));

    var interactive = widget.control.getBool("interactive", true)!;

    // Build list of ScatterSpotData
    final spots = widget.control.children('scatter_spots').map((spot) {
      return ScatterSpot(spot.getDouble('x')!, spot.getDouble('y')!,
          show: spot.getBool('show', true)!,
          renderPriority: spot.getInt('render_priority', 0)!,
          xError: spot.get('x_error'),
          yError: spot.get('y_error'),
          dotPainter: parseChartDotPainter(
              spot.get("point"), Theme.of(context), null, null, 0));
    }).toList();

    final chart = ScatterChart(
      ScatterChartData(
        scatterSpots: spots,
        backgroundColor: widget.control.getColor("bgcolor", context),
        minX: widget.control.getDouble("min_x"),
        maxX: widget.control.getDouble("max_x"),
        minY: widget.control.getDouble("min_y"),
        maxY: widget.control.getDouble("max_y"),
        baselineX: widget.control.getDouble("baseline_x"),
        baselineY: widget.control.getDouble("baseline_y"),
        titlesData: (leftTitles.sideTitles.showTitles ||
                topTitles.sideTitles.showTitles ||
                rightTitles.sideTitles.showTitles ||
                bottomTitles.sideTitles.showTitles)
            ? FlTitlesData(
                show: true,
                leftTitles: leftTitles,
                topTitles: topTitles,
                rightTitles: rightTitles,
                bottomTitles: bottomTitles,
              )
            : const FlTitlesData(show: false),
        borderData: border != null
            ? FlBorderData(show: true, border: border)
            : FlBorderData(show: false),
        gridData: parseChartGridData(Theme.of(context), widget.control,
            "horizontal_grid_lines", "vertical_grid_lines"),
        scatterTouchData: ScatterTouchData(
            enabled: interactive,
            touchCallback: widget.control.getBool("on_chart_event", false)!
                ? (evt, resp) {
                    var eventData = ScatterChartEventData(
                        eventType: evt.runtimeType
                            .toString()
                            .substring(2), // remove "Fl"
                        spotIndex: resp?.touchedSpot?.spotIndex);

                    debugPrint(
                        "ScatterChart ${widget.control.id} ${eventData.eventType}");
                    widget.control
                        .triggerEvent("chart_event", eventData.toJson());
                  }
                : null,
            // mouseCursorResolver: (evt, resp) {
            //   return MouseCursor.defer;
            // },
            longPressDuration:
                widget.control.getDuration("long_press_duration"),
            handleBuiltInTouches:
                widget.control.getBool("handle_built_in_touches", true)!,
            touchTooltipData: ScatterTouchTooltipData(
              tooltipBorder: widget.control.getBorderSide(
                      "tooltip_border_side", Theme.of(context)) ??
                  BorderSide.none,
              tooltipPadding: widget.control.getPadding("tooltip_padding",
                  const EdgeInsets.symmetric(horizontal: 16, vertical: 8))!,
              tooltipHorizontalAlignment: FLHorizontalAlignment.values
                  .firstWhereOrNull((v) =>
                      v.name ==
                      widget.control.getString("tooltip_horizontal_alignment")),
              tooltipHorizontalOffset:
                  widget.control.getDouble("tooltip_horizontal_offset", 0)!,
              tooltipRoundedRadius:
                  widget.control.getDouble("tooltip_rounded_radius", 4)!,
              fitInsideHorizontally: widget.control
                  .getBool("tooltip_fit_inside_horizontally", false)!,
              fitInsideVertically: widget.control
                  .getBool("tooltip_fit_inside_vertically", false)!,
              getTooltipColor: (ScatterSpot spot) {
                var spotIndex = spots
                    .indexWhere((spot) => spot.x == spot.x && spot.y == spot.y);
                var dp = widget.control.children("scatter_spots")[spotIndex];
                return dp.getColor("tooltip_bgcolor", context) ??
                    widget.control.getColor("tooltip_bgcolor", context,
                        const Color.fromRGBO(96, 125, 139, 1))!;
              },
              getTooltipItems: (touchedSpot) {
                var spotIndex = spots.indexWhere((spot) =>
                    spot.x == touchedSpot.x && spot.y == touchedSpot.y);
                var dp = widget.control.children("scatter_spots")[spotIndex];
                var tooltip = dp.getString("tooltip_text") ??
                    dp.getDouble("y").toString();
                var tooltipStyle =
                    dp.getTextStyle("tooltip_style", Theme.of(context));
                tooltipStyle ??= const TextStyle();
                if (tooltipStyle.color == null) {
                  tooltipStyle = tooltipStyle.copyWith(
                      color: touchedSpot.dotPainter.mainColor);
                }
                TextAlign? tooltipAlign =
                    dp.getTextAlign("tooltip_align", TextAlign.center)!;
                List<TextSpan>? spans = dp.get("tooltip_spans") != null
                    ? parseTextSpans(
                        Theme.of(context),
                        dp.children("tooltip_spans"),
                        dp.disabled,
                        (Control control, String eventName, String eventData) {
                          control.triggerEvent(eventName, eventData);
                        },
                      )
                    : null;
                return dp.getBool("show_tooltip", true)!
                    ? ScatterTooltipItem(tooltip,
                        textStyle: tooltipStyle,
                        textAlign: tooltipAlign,
                        children: spans)
                    : null;
              },
            )),
        scatterLabelSettings: ScatterLabelSettings(
          showLabel: true,
          getLabelFunction: (spotIndex, spot) => "aaa",
          getLabelTextStyleFunction: (spotIndex, spot) => const TextStyle(),
        ),
        showingTooltipIndicators: widget.control
            .children('scatter_spots')
            .asMap()
            .entries
            .where((e) => e.value.getBool("selected", false)!)
            .map((e) => e.key)
            .toList(),
        rotationQuarterTurns:
            widget.control.getInt('rotation_quarter_turns', 0)!,
        //errorIndicatorData: widget.control.get('error_indicator_data'),
      ),
      duration: animate != null
          ? animate.duration
          : const Duration(milliseconds: 150),
      curve: animate != null ? animate.curve : Curves.linear,
    );

    return ConstrainedControl(control: widget.control, child: chart);
  }

  AxisTitles getAxisTitles(Control? axis) {
    if (axis == null) {
      return const AxisTitles(sideTitles: SideTitles(showTitles: false));
    }

    return AxisTitles(
        axisNameWidget: axis.buildWidget("title"),
        axisNameSize: axis.getDouble("title_size") ?? 16,
        sideTitles: SideTitles(
          showTitles: axis.getBool("show_labels", true)!,
          reservedSize: axis.getDouble("labels_size") ?? 22,
          interval: axis.getDouble("labels_interval"),
          getTitlesWidget: axis.children("labels").isEmpty
              ? defaultGetTitle
              : (value, meta) {
                  var label = axis
                      .children("labels")
                      .firstWhereOrNull((l) => l.getDouble("value") == value);
                  return label?.buildWidget("label") ?? const SizedBox.shrink();
                },
        ));
  }
}
