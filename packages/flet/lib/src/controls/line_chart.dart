import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../widgets/skip_inherited_notifier.dart';

class LineChartControl extends StatefulWidget implements SkipInheritedNotifier {
  final Control control;
  const LineChartControl({super.key, required this.control});

  @override
  State<LineChartControl> createState() => _LineChartControlState();
}

class _LineChartControlState extends State<LineChartControl> {
  final Map<Control, List<FlSpot>> _barSpots = {};

  @override
  void initState() {
    debugPrint("LineChart.initState: ${widget.control.id}");
    super.initState();
    widget.control.addListener(_chartUpdated);
    _chartUpdated();
  }

  @override
  void dispose() {
    debugPrint("LineChart.dispose: ${widget.control.id}");
    widget.control.removeListener(_chartUpdated);
    super.dispose();
  }

  _chartUpdated() {
    debugPrint("LineChart._chartUpdated: ${widget.control.id}");
    setState(() {
      for (var lineBar in widget.control.children("line_bars")) {
        List<FlSpot> spots = [];
        if (_barSpots.containsKey(lineBar)) {
          spots = _barSpots[lineBar]!;
        } else {
          _barSpots[lineBar] = spots;
          lineBar.addListener(_chartUpdated);
        }

        spots.clear();
        spots.addAll(lineBar.get<List>("spots")!.map(
            (spot) => FlSpot(spot["x"]!.toDouble(), spot["y"]!.toDouble())));
      }

      // removed outdated bars
      for (var lineBar in _barSpots.keys.toList()) {
        if (!widget.control
            .children("line_bars")
            .any((bar) => bar.id == lineBar.id)) {
          _barSpots.remove(lineBar);
          lineBar.removeListener(_chartUpdated);
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("LineChart.build: ${widget.control.id}");

    return SizedBox.fromSize(
        size: Size(300, 300),
        child: LineChart(LineChartData(
            minY: 0,
            maxY: 1,
            clipData: const FlClipData.all(),
            lineBarsData: widget.control
                .children("line_bars")
                .map((lineBar) => LineChartBarData(
                    isCurved: true, spots: _barSpots[lineBar]!))
                .toList())));
  }
}
