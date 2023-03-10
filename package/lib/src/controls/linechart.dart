import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/linechart_axis_view_model.dart';
import '../models/linechart_data_view_model.dart';
import '../models/linechart_view_model.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/charts.dart';
import '../utils/colors.dart';
import '../utils/gradient.dart';
import 'create_control.dart';

class LineChartControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const LineChartControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("LineChart build: ${control.id}");

    var animate = parseAnimation(control, "animate");
    var border = parseBorder(Theme.of(context), control, "border");
    bool disabled = control.isDisabled || parentDisabled;

    return StoreConnector<AppState, LineChartViewModel>(
        distinct: true,
        converter: (store) =>
            LineChartViewModel.fromStore(store, control, children),
        builder: (context, viewModel) {
          var leftTitles = getAxisTitles(control, viewModel.leftAxis, disabled);
          var topTitles = getAxisTitles(control, viewModel.topAxis, disabled);
          var rightTitles =
              getAxisTitles(control, viewModel.rightAxis, disabled);
          var bottomTitles =
              getAxisTitles(control, viewModel.bottomAxis, disabled);

          var chart = LineChart(
            LineChartData(
                backgroundColor: HexColor.fromString(
                    Theme.of(context), control.attrString("bgcolor", "")!),
                minX: control.attrDouble("minx"),
                maxX: control.attrDouble("maxx"),
                minY: control.attrDouble("miny"),
                maxY: control.attrDouble("maxy"),
                baselineX: control.attrDouble("baselinex"),
                baselineY: control.attrDouble("baseliney"),
                //showingTooltipIndicators: [ShowingTooltipIndicators([LineBarSpot(bar, barIndex, spot)])],
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
                    : FlTitlesData(show: false),
                borderData: border != null
                    ? FlBorderData(show: true, border: border)
                    : FlBorderData(show: false),
                gridData: parseChartGridData(Theme.of(context), control,
                    "horizontalGridLines", "verticalGridLines"),
                lineBarsData: viewModel.dataSeries
                    .map((d) => getBarData(Theme.of(context), control, d))
                    .toList()),
            swapAnimationDuration: animate != null
                ? animate.duration
                : const Duration(milliseconds: 150), // Optional
            swapAnimationCurve: animate != null ? animate.curve : Curves.linear,
          );

          return constrainedControl(context, chart, parent, control);
        });
  }

  LineChartBarData getBarData(
      ThemeData theme, Control parent, LineChartDataViewModel dataViewModel) {
    bool showMarkers = dataViewModel.control.attrBool("showMarkers", false)!;
    Color? aboveLineColor = HexColor.fromString(
        theme, dataViewModel.control.attrString("aboveLineColor", "")!);
    Gradient? aboveLineGradient =
        parseGradient(theme, dataViewModel.control, "aboveLineGradient");
    Color? belowLineColor = HexColor.fromString(
        theme, dataViewModel.control.attrString("belowLineColor", "")!);
    Gradient? belowLineGradient =
        parseGradient(theme, dataViewModel.control, "belowLineGradient");
    return LineChartBarData(
        spots: dataViewModel.dataPoints.map((p) => FlSpot(p.x, p.y)).toList(),
        isCurved: dataViewModel.control.attrBool("curved"),
        isStrokeCapRound: dataViewModel.control.attrBool("strokeCapRound"),
        barWidth: dataViewModel.control.attrDouble("strokeWidth"),
        dotData: showMarkers ? FlDotData(show: true) : FlDotData(show: false),
        aboveBarData: aboveLineColor != null || aboveLineGradient != null
            ? BarAreaData(
                show: true, color: aboveLineColor, gradient: aboveLineGradient)
            : null,
        belowBarData: belowLineColor != null || belowLineGradient != null
            ? BarAreaData(
                show: true, color: belowLineColor, gradient: belowLineGradient)
            : null,
        color: HexColor.fromString(
            theme, dataViewModel.control.attrString("color", "")!),
        gradient: parseGradient(theme, dataViewModel.control, "gradient"));
  }

  AxisTitles getAxisTitles(
      Control parent, LineChartAxisViewModel? axisViewModel, bool disabled) {
    if (axisViewModel == null) {
      return AxisTitles(sideTitles: SideTitles(showTitles: false));
    }

    return AxisTitles(
        axisNameWidget: axisViewModel.title != null
            ? createControl(parent, axisViewModel.title!.id, disabled)
            : null,
        axisNameSize: axisViewModel.control.attrDouble("titleSize"),
        sideTitles: SideTitles(
          showTitles: axisViewModel.control.attrBool("showLabels", true),
          reservedSize: axisViewModel.control.attrDouble("labelsSize"),
          interval: axisViewModel.control.attrDouble("labelsInterval"),
          getTitlesWidget: axisViewModel.labels.isEmpty
              ? null
              : (value, meta) {
                  return axisViewModel.labels.containsKey(value)
                      ? createControl(
                          parent, axisViewModel.labels[value]!.id, disabled)
                      : const SizedBox.shrink();
                },
        ));
  }
}
