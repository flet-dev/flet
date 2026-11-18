import 'package:flet/flet.dart';
import 'package:flet_charts/src/bar_chart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';

void main() {
  testWidgets('a stack item without a color uses the rod color',
      (tester) async {
    final backend = FletBackend(
      pageUri: Uri.parse('http://localhost'),
      assetsDir: '',
      extensions: [],
      multiView: false,
    );
    final chart = Control.fromMap({
      '_c': 'BarChart',
      '_i': 1,
      'interactive': false,
      'min_y': 0,
      'max_y': 10,
      'groups': [
        {
          '_c': 'BarChartGroup',
          '_i': 2,
          'x': 0,
          'rods': [
            {
              '_c': 'BarChartRod',
              '_i': 3,
              'to_y': 6,
              'color': '#00ff00',
              'stack_items': [
                {'_c': 'BarChartRodStackItem', '_i': 4, 'to_y': 3},
              ],
            },
          ],
        },
      ],
    }, backend);
    await tester.pumpWidget(MaterialApp(
      home: Center(
        child: SizedBox.square(
          dimension: 200,
          child: BarChartControl(control: chart),
        ),
      ),
    ));
    expect(tester.takeException(), isNull);
  });
}
