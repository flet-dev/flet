import 'package:flet/flet.dart';
import 'package:flet_charts/src/line_chart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';

const _size = 200.0;
const _spotLineColor = Color(0xFFFF0000);

void main() {
  for (final line in ['above_line', 'below_line']) {
    testWidgets('$line follows its visible point through animation', (
      tester,
    ) async {
      final backend = FletBackend(
        pageUri: Uri.parse('http://localhost'),
        assetsDir: '',
        extensions: [],
        multiView: false,
      );
      final chart = Control.fromMap({
        '_c': 'LineChart',
        '_i': 1,
        'animation': 1000,
        'interactive': false,
        'min_x': 0,
        'max_x': 10,
        'min_y': 0,
        'max_y': 10,
        'data_series': [
          {
            '_c': 'LineChartData',
            '_i': 2,
            line: {'color': '#ff0000', 'width': 1},
            'points': [
              {'_c': 'LineChartDataPoint', '_i': 3, 'x': 2, 'y': 2},
              {
                '_c': 'LineChartDataPoint',
                '_i': 4,
                'x': 6,
                'y': 4,
                'show_$line': false,
              },
            ],
          },
        ],
      }, backend);
      await tester.pumpWidget(
        MaterialApp(
          home: Center(
            child: SizedBox.square(
              dimension: _size,
              child: LineChartControl(control: chart),
            ),
          ),
        ),
      );

      void expectSpotLine(double x, double y) {
        expect(tester.takeException(), isNull);
        final paths = <Rect>[];
        expect(
          find.byType(LineChartControl),
          paints
            ..everything((method, arguments) {
              if (method == #drawPath &&
                  (arguments[1] as Paint).color == _spotLineColor) {
                paths.add((arguments[0] as Path).getBounds());
              }
              return true;
            }),
        );
        expect(paths, [
          if (line == 'above_line')
            Rect.fromLTRB(x, 0, x, y)
          else
            Rect.fromLTRB(x, y, x, _size),
        ]);
      }

      expectSpotLine(40, 160);
      final points = chart.children('data_series').single.children('points');
      points.first.update({'x': 4, 'y': 6}, shouldNotify: true);
      points.last.update({'x': 8, 'y': 8}, shouldNotify: true);
      await tester.pump();
      expectSpotLine(40, 160);
      await tester.pump(const Duration(milliseconds: 500));
      expectSpotLine(60, 120);
      await tester.pump(const Duration(milliseconds: 500));
      expectSpotLine(80, 80);
    });
  }
}
