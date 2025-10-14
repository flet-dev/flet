import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'bar_chart.dart';
import 'candlestick_chart.dart';
import 'line_chart.dart';
import 'radar_chart.dart';
import 'pie_chart.dart';
import 'scatter_chart.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "BarChart":
        return BarChartControl(key: key, control: control);
      case "CandlestickChart":
        return CandlestickChartControl(key: key, control: control);
      case "LineChart":
        return LineChartControl(key: key, control: control);
      case "RadarChart":
        return RadarChartControl(key: key, control: control);
      case "PieChart":
        return PieChartControl(key: key, control: control);
      case "ScatterChart":
        return ScatterChartControl(key: key, control: control);
      default:
        return null;
    }
  }
}
