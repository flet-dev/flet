import 'package:flet/src/controls/control_widget.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

/// Wide enough for the `lg` breakpoint.
const double _width = 1200;

/// Width of a child spanning [cols] of 12 columns with [spacing] between
/// them, after the 0.1px the row leaves unused.
double _span(int cols, {double spacing = 10}) =>
    (_width - 0.1 - spacing * 11) / 12 * cols + spacing * (cols - 1);

/// Builds a `ResponsiveRow` whose children have the given `col` values, pumps
/// it, and returns the children.
Future<List<Control>> _pumpRow(WidgetTester tester, List<dynamic> cols,
    {Map<String, dynamic> props = const {}}) async {
  await tester.binding.setSurfaceSize(const Size(_width, 600));
  addTearDown(() => tester.binding.setSurfaceSize(null));

  final backend = FletBackend(
      pageUri: Uri.parse('http://localhost'),
      assetsDir: '',
      extensions: [FletCoreExtension()],
      multiView: false)
    ..pageSize = const Size(_width, 600);
  final row = Control.fromMap({
    '_c': 'ResponsiveRow',
    '_i': 1,
    ...props,
    'controls': [
      for (var i = 0; i < cols.length; i++)
        {'_c': 'Container', '_i': i + 2, 'height': 20, 'col': cols[i]},
    ],
  }, backend);

  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(home: Scaffold(body: ControlWidget(control: row)))));
  return row.children('controls');
}

double _widthOf(WidgetTester tester, Control child) =>
    tester.getSize(find.byKey(GlobalObjectKey(child))).width;

/// Applies [ops] to the `col` dict of [child], the way Python patches a
/// changed breakpoint.
Future<void> _patchColMap(
    WidgetTester tester, Control child, List<dynamic> ops) async {
  child.applyPatch([
    [
      0,
      {
        'col': [1]
      }
    ],
    ...ops,
  ], child.backend);
  await tester.pump();
}

void main() {
  group('ResponsiveRow resizes a child when its col changes', () {
    testWidgets('number replaced', (tester) async {
      final children = await _pumpRow(tester, [6, 6]);
      expect(_widthOf(tester, children[0]), _span(6));

      children[0].applyPatch([
        [0],
        [0, 0, 'col', 3]
      ], children[0].backend);
      await tester.pump();

      expect(_widthOf(tester, children[0]), _span(3));
      expect(_widthOf(tester, children[1]), _span(6));
    });

    testWidgets('breakpoint value replaced', (tester) async {
      final children = await _pumpRow(tester, [
        {'md': 6},
        6
      ]);
      expect(_widthOf(tester, children[0]), _span(6));

      await _patchColMap(tester, children[0], [
        [0, 1, 'md', 3]
      ]);

      expect(_widthOf(tester, children[0]), _span(3));
      expect(_widthOf(tester, children[1]), _span(6));
    });

    testWidgets('breakpoint added', (tester) async {
      final children = await _pumpRow(tester, [
        {'md': 6},
        6
      ]);
      expect(_widthOf(tester, children[0]), _span(6));

      await _patchColMap(tester, children[0], [
        [1, 1, 'lg', 3]
      ]);

      expect(_widthOf(tester, children[0]), _span(3));
      expect(_widthOf(tester, children[1]), _span(6));
    });

    testWidgets('breakpoint removed', (tester) async {
      final children = await _pumpRow(tester, [
        {'md': 6, 'lg': 3},
        6
      ]);
      expect(_widthOf(tester, children[0]), _span(3));

      await _patchColMap(tester, children[0], [
        [2, 1, 'lg']
      ]);

      expect(_widthOf(tester, children[0]), _span(6));
      expect(_widthOf(tester, children[1]), _span(6));
    });
  });
  testWidgets('ResponsiveRow fills one line with zero spacing', (tester) async {
    final children =
        await _pumpRow(tester, List.filled(12, 1), props: {'spacing': 0});

    expect(tester.takeException(), isNull);
    final top = tester.getTopLeft(find.byKey(GlobalObjectKey(children[0]))).dy;
    for (final child in children) {
      expect(_widthOf(tester, child), _span(1, spacing: 0));
      expect(tester.getTopLeft(find.byKey(GlobalObjectKey(child))).dy, top);
    }
  });

  testWidgets('ResponsiveRow wraps children whose gaps overflow a narrow row',
      (tester) async {
    await _pumpRow(tester, List.filled(12, 1), props: {'width': 109});
    expect(tester.takeException(), isNull);

    await _pumpRow(tester, [0.09, ...List.filled(10, 1), 1.91]);
    expect(tester.takeException(), isNull);
  });

  testWidgets('ResponsiveRow wraps with zero spacing', (tester) async {
    final children = await _pumpRow(tester, List.filled(13, 1),
        props: {'spacing': 0, 'run_spacing': 0});

    expect(tester.takeException(), isNull);
    double top(Control child) =>
        tester.getTopLeft(find.byKey(GlobalObjectKey(child))).dy;
    for (final child in children.take(12)) {
      expect(top(child), top(children.first));
    }
    expect(top(children.last), top(children.first) + 20);
  });
}
