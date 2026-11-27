import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:material_ui/material_ui.dart';

import 'utils/gauge_chart.dart';

class GaugeChartControl extends StatefulWidget {
  final Control control;

  GaugeChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<GaugeChartControl> createState() => _GaugeChartControlState();
}

class _GaugeChartControlState extends State<GaugeChartControl> {
  GaugeChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("GaugeChart build: ${widget.control.id}");

    final theme = Theme.of(context);
    final animation = widget.control.getAnimation(
        "animation",
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 150),
            curve: Curves.linear))!;
    final interactive = widget.control.getBool("interactive", true)! &&
        !widget.control.disabled;
    final border = widget.control.getBorder("border", theme);
    final minValue = widget.control.getDouble("min_value", 0)!;
    final maxValue = widget.control.getDouble("max_value", 1)!;

    final chart = GaugeChart(
      GaugeChartData(
        rings: (widget.control.get<List>("rings") ?? [])
            .map((ring) => parseGaugeRing(ring, theme))
            .nonNulls
            .toList(),
        minValue: minValue,
        maxValue: maxValue,
        startDegreeOffset:
            widget.control.getDouble("start_degree_offset", -225)!,
        sweepAngle: widget.control.getDouble("sweep_angle", 270)!,
        direction: parseGaugeDirection(
            widget.control.getString("direction"), GaugeDirection.clockwise)!,
        defaultRingWidth: widget.control.getDouble("default_ring_width", 10)!,
        ringsSpace: widget.control.getDouble("rings_space", 0)!,
        ticks: parseGaugeTicks(
            widget.control.get("ticks"), minValue, maxValue, theme),
        markers: (widget.control.get<List>("markers") ?? [])
            .map((marker) => parseGaugeMarker(marker, theme))
            .nonNulls
            .toList(),
        pointers: (widget.control.get<List>("pointers") ?? [])
            .map((pointer) => parseGaugePointer(pointer, theme))
            .nonNulls
            .toList(),
        borderData: FlBorderData(show: border != null, border: border),
        touchData: GaugeTouchData(
          enabled: interactive,
          longPressDuration: widget.control.getDuration("long_press_duration"),
          touchCallback: (event, response) {
            final eventData = GaugeChartEventData.fromDetails(event, response);
            if (eventData != _eventData) {
              _eventData = eventData;
              widget.control.triggerEvent("event", eventData.toMap());
            }
          },
        ),
      ),
      duration: animation.duration,
      curve: animation.curve,
    );

    return LayoutControl(
        control: widget.control,
        child: LayoutBuilder(
            builder: (BuildContext context, BoxConstraints constraints) {
          return (constraints.maxHeight == double.infinity)
              ? ConstrainedBox(
                  constraints: const BoxConstraints(maxHeight: 300),
                  child: chart)
              : chart;
        }));
  }
}
