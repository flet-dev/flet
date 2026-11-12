import 'package:flet/flet.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet_datatable2/src/datatable2.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

class _Backend extends FletBackend {
  _Backend()
    : super(
        pageUri: Uri.parse('http://localhost'),
        assetsDir: '',
        extensions: [FletCoreExtension()],
        multiView: false,
      );
}

Future<void> _pumpTable(
  WidgetTester tester,
  Map<String, dynamic> props, {
  int rows = 1000,
  int columns = 3,
}) async {
  final backend = _Backend();
  var id = 1;
  Control control(String type, Map<String, dynamic> properties) =>
      Control(id: id++, type: type, properties: properties, backend: backend);

  final table = control('DataTable2', {
    ...props,
    'columns': [
      for (var c = 0; c < columns; c++)
        control('DataColumn2', {'label': 'H$c'}),
    ],
    'rows': [
      for (var r = 0; r < rows; r++)
        control('DataRow2', {
          'cells': [
            for (var c = 0; c < columns; c++)
              control('DataCell', {
                'content': control('Text', {'value': 'r$r c$c'}),
              }),
          ],
        }),
    ],
  });

  await tester.pumpWidget(
    ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 800,
            height: 600,
            child: DataTable2Control(control: table),
          ),
        ),
      ),
    ),
  );
  await tester.pump();
  expect(tester.takeException(), isNull);
}

/// Scrolls the table body, the nearest scrollable above a body cell, to
/// [offset], or to its end if that is past it.
Future<void> _scrollBody(WidgetTester tester, double offset) async {
  final cell = find.textContaining(RegExp(r'^r\d+ c1$')).first;
  final position = tester
      .state<ScrollableState>(
        find.ancestor(of: cell, matching: find.byType(Scrollable)).first,
      )
      .position;
  position.jumpTo(offset.clamp(0, position.maxScrollExtent));
  await tester.pump();
}

void main() {
  testWidgets('a long DataTable2 builds only the rows near the viewport', (
    tester,
  ) async {
    await _pumpTable(tester, {});

    expect(find.text('H0'), findsOneWidget);
    expect(find.text('r0 c0'), findsOneWidget);
    expect(find.text('r500 c0'), findsNothing);
    expect(find.text('r999 c2'), findsNothing);
    // Rows sit where one table would put them: 56 heading, then 48 a row.
    expect(
      tester.getTopLeft(find.text('r10 c0')).dy,
      moreOrLessEquals(tester.getTopLeft(find.text('r0 c0')).dy + 480),
    );

    await _scrollBody(tester, 500 * 48);
    expect(find.text('r500 c0'), findsOneWidget);
    expect(find.text('r0 c0'), findsNothing);

    await _scrollBody(tester, 1000 * 48);
    expect(find.text('r999 c2'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('a long DataTable2 keeps fixed left columns in line', (
    tester,
  ) async {
    await _pumpTable(tester, {'fixed_left_columns': 1});

    await _scrollBody(tester, 300 * 48);
    await tester.pump();
    for (final r in [300, 305, 311]) {
      expect(
        tester.getTopLeft(find.text('r$r c0')).dy,
        tester.getTopLeft(find.text('r$r c1')).dy,
        reason: 'row $r',
      );
    }
    expect(tester.takeException(), isNull);
  });

  testWidgets('a short DataTable2 is one table of every row', (tester) async {
    await _pumpTable(tester, {}, rows: 20);
    expect(find.text('r19 c2', skipOffstage: false), findsOneWidget);
    expect(find.byType(ListView), findsNothing);
  });
}
