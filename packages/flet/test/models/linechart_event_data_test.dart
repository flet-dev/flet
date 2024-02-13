import 'dart:convert';

import 'package:flet/src/controls/linechart.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("Test LinechartEventData equality", () {
    var e1 = const LineChartEventData(eventType: "Hover", barSpots: [
      LineChartEventDataSpot(barIndex: 0, spotIndex: 1),
      LineChartEventDataSpot(barIndex: 1, spotIndex: 1)
    ]);
    var e2 = const LineChartEventData(eventType: "Hover", barSpots: [
      LineChartEventDataSpot(barIndex: 0, spotIndex: 1),
      LineChartEventDataSpot(barIndex: 1, spotIndex: 1)
    ]);
    expect(e1 == e2, true);
  });

  test("Test LinechartEventData inequality", () {
    var e1 = const LineChartEventData(eventType: "Hover", barSpots: [
      LineChartEventDataSpot(barIndex: 0, spotIndex: 0),
      LineChartEventDataSpot(barIndex: 1, spotIndex: 0)
    ]);
    var e2 = const LineChartEventData(eventType: "Hover", barSpots: [
      LineChartEventDataSpot(barIndex: 0, spotIndex: 1),
      LineChartEventDataSpot(barIndex: 1, spotIndex: 1)
    ]);
    expect(e1 == e2, false);
  });

  test("LinechartEventData serialize to json", () {
    var e = const LineChartEventData(eventType: "Hover", barSpots: [
      LineChartEventDataSpot(barIndex: 0, spotIndex: 1),
      LineChartEventDataSpot(barIndex: 1, spotIndex: 1)
    ]);

    final j = json.encode(e);

    expect(j,
        '{"type":"Hover","spots":[{"bar_index":0,"spot_index":1},{"bar_index":1,"spot_index":1}]}');
  });
}
