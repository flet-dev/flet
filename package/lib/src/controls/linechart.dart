import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
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

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    var chart = LineChart(
      LineChartData(
          backgroundColor: Colors.amber[600],
          // minX: -20,
          // maxX: 20,
          // minY: -20,
          // maxY: 20,
          //showingTooltipIndicators: [ShowingTooltipIndicators([LineBarSpot(bar, barIndex, spot)])],
          titlesData: FlTitlesData(
            show: true,
            leftTitles: AxisTitles(
                axisNameWidget: Text("Left axis"),
                sideTitles: SideTitles(
                  showTitles: true,
                  interval: 1,
                  getTitlesWidget: (value, meta) {
                    return Text("aaa-$value");
                  },
                )),
            bottomTitles: AxisTitles(
                sideTitles: SideTitles(
              showTitles: true,
              interval: 1,
              getTitlesWidget: (value, meta) {
                return Text("$value");
              },
            )),
            topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
            rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
          ),
          borderData: FlBorderData(
              show: true,
              border:
                  Border(bottom: BorderSide(color: Colors.black, width: 2))),
          gridData: FlGridData(
            show: true,
            horizontalInterval: 1,
            verticalInterval: 1,
            getDrawingVerticalLine: (value) {
              return FlLine(strokeWidth: 0.5);
            },
          ),
          lineBarsData: [
            LineChartBarData(
              isCurved: true,
              //color: const Color(0xff4af699),
              barWidth: 4,
              isStrokeCapRound: true,
              dotData: FlDotData(show: true),
              belowBarData: BarAreaData(show: true),
              spots: const [
                FlSpot(1, 1),
                FlSpot(3, 1.5),
                FlSpot(5, 1.4),
                FlSpot(7, 3.4),
                FlSpot(10, 2),
                FlSpot(12, 2.2),
                FlSpot(13, 1.8),
              ],
            ),
            LineChartBarData(
              isCurved: false,
              color: Colors.red,
              barWidth: 8,
              isStrokeCapRound: false,
              dotData: FlDotData(show: false),
              aboveBarData: BarAreaData(
                show: true,
                color: const Color(0x99aa4cfc),
              ),
              spots: const [
                FlSpot(-1, 1),
                FlSpot(3, 2.8),
                FlSpot(7, 1.2),
                FlSpot(10, 2.8),
                FlSpot(12, 2.6),
                FlSpot(15, 3.9),
              ],
            )
          ]),
      swapAnimationDuration: Duration(milliseconds: 150), // Optional
      swapAnimationCurve: Curves.linear,
    );

    return constrainedControl(context, chart, parent, control);
  }
}
