import 'package:flet/src/controls/datatable.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

class _Backend extends FletBackend {
  _Backend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [],
            multiView: false);
}

Future<void> _pumpTable(WidgetTester tester, Map<String, dynamic> props) async {
  final backend = _Backend();
  var id = 1;
  Control control(String type, Map<String, dynamic> properties) =>
      Control(id: id++, type: type, properties: properties, backend: backend);

  final table = control('DataTable', {
    ...props,
    'columns': [
      for (final label in ['A', 'B']) control('DataColumn', {'label': label})
    ],
    'rows': [
      for (var r = 0; r < 3; r++)
        control('DataRow', {
          'cells': [
            for (var c = 0; c < 2; c++)
              control('DataCell', {'content': 'r$r c$c'})
          ]
        })
    ],
  });

  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(
              body: SingleChildScrollView(
                  child: DataTableControl(control: table))))));
  expect(tester.takeException(), isNull);
}

void main() {
  testWidgets('DataTable paints behind its own repaint boundary',
      (tester) async {
    await _pumpTable(tester, {});
    expect(
        find.ancestor(
            of: find.byType(DataTable), matching: find.byType(RepaintBoundary)),
        findsWidgets);
    expect(
        find.descendant(
            of: find.byType(DataTableControl),
            matching: find.byWidgetPredicate((w) =>
                w is RepaintBoundary && w.child is DataTable)),
        findsOneWidget);
    expect(find.text('r2 c1'), findsOneWidget);
  });

  testWidgets('horizontal_lines and vertical_lines draw the table border',
      (tester) async {
    await _pumpTable(tester, {
      'horizontal_lines': {'width': 2.0, 'color': 'red'},
      'vertical_lines': {'width': 3.0, 'color': 'blue'},
    });
    final border = tester.widget<DataTable>(find.byType(DataTable)).border!;
    expect(border.horizontalInside.width, 2.0);
    expect(border.horizontalInside.color, Colors.red);
    expect(border.verticalInside.width, 3.0);
    expect(border.verticalInside.color, Colors.blue);
  });
}
