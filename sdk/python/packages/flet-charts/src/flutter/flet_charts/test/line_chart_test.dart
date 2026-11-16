import 'package:flet/flet.dart';
import 'package:flet_charts/src/line_chart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';

const _size = 200.0;
const _spotLineColor = Color(0xFFFF0000);

List<Path> _paintedPaths(WidgetTester tester, Color color) {
  expect(tester.takeException(), isNull);
  final paths = <Path>[];
  expect(
    find.byType(LineChartControl),
    paints
      ..everything((method, arguments) {
        if (method == #drawPath && (arguments[1] as Paint).color == color) {
          paths.add(arguments[0] as Path);
        }
        return true;
      }),
  );
  return paths;
}

void main() {
  for (final inferBounds in [false, true]) {
    final bounds = inferBounds ? 'inferred' : 'explicit';
    testWidgets('a rolling window scrolls with $bounds X bounds',
        (tester) async {
      final backend = FletBackend(
        pageUri: Uri.parse('http://localhost'),
        assetsDir: '',
        extensions: [],
        multiView: false,
      );
      const color = Color(0xFF0000FF);
      final chart = Control.fromMap({
        '_c': 'LineChart',
        '_i': 1,
        'animation': 1000,
        'interactive': false,
        if (!inferBounds) 'min_x': 0,
        if (!inferBounds) 'max_x': 4,
        'min_y': 0,
        'max_y': 10,
        'data_series': [
          {
            '_c': 'LineChartData',
            '_i': 2,
            'color': '#0000ff',
            'points': [
              {'_c': 'LineChartDataPoint', '_i': 3, 'x': 0, 'y': 3},
              {'_c': 'LineChartDataPoint', '_i': 4, 'x': 1, 'y': 7},
              {'_c': 'LineChartDataPoint', '_i': 5, 'x': 2, 'y': 2},
              {'_c': 'LineChartDataPoint', '_i': 6, 'x': 3, 'y': 4},
              {'_c': 'LineChartDataPoint', '_i': 7, 'x': 4, 'y': 2},
            ],
          },
        ],
      }, backend);
      await tester.pumpWidget(MaterialApp(
        home: Center(
          child: SizedBox.square(
            dimension: _size,
            child: LineChartControl(control: chart),
          ),
        ),
      ));

      Offset firstPoint() => _paintedPaths(tester, color)
          .single
          .computeMetrics()
          .first
          .getTangentForOffset(0)!
          .position;

      expect(firstPoint(), const Offset(0, 140));
      chart.applyPatch([
        [
          0,
          {
            'data_series': [
              1,
              {
                0: [
                  2,
                  {
                    'points': [3]
                  },
                ],
              },
            ],
          },
        ],
        if (!inferBounds) [0, 0, 'min_x', 1],
        if (!inferBounds) [0, 0, 'max_x', 5],
        [2, 3, 0],
        [
          1,
          3,
          4,
          {'_c': 'LineChartDataPoint', '_i': 8, 'x': 5, 'y': 3}
        ],
      ], backend);
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      expect(firstPoint(), const Offset(25, 60));
      await tester.pump(const Duration(milliseconds: 500));
      expect(firstPoint(), const Offset(0, 60));

      final retained =
          chart.children('data_series').single.children('points').first;
      retained.update({'y': 5}, shouldNotify: true);
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      expect(firstPoint(), const Offset(0, 80));
    });
  }

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
        final paths = _paintedPaths(tester, _spotLineColor);
        expect(paths.map((path) => path.getBounds()), [
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
