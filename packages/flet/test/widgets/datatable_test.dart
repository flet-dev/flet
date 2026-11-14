import 'dart:ui' show SemanticsAction, SemanticsFlag;

import 'package:flet/src/controls/control_widget.dart';
import 'package:flet/src/controls/datatable.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/semantics.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

class _Backend extends FletBackend {
  _Backend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [FletCoreExtension()],
            multiView: false);

  final events = <(int, String, dynamic)>[];

  @override
  void triggerControlEventById(int controlId, String eventName,
      [dynamic eventData]) {
    events.add((controlId, eventName, eventData));
  }
}

class _Table {
  _Table(this.backend, this.control);

  final _Backend backend;
  final Control control;

  List<Control> get rows => control.children('rows');
}

Future<_Table> _pumpTable(WidgetTester tester, Map<String, dynamic> props,
    {int rows = 3,
    String Function(int row, int column)? text,
    Object? Function(int row, int column)? content,
    Object? heading,
    bool textControls = false,
    Map<String, dynamic> rowProps = const {},
    Set<int> selected = const {}}) async {
  final backend = _Backend();
  var id = 1;
  Map<String, dynamic> control(String type, Map<String, dynamic> properties) =>
      {'_c': type, '_i': id++, ...properties};

  final table = Control.fromMap(
      control('DataTable', {
        ...props,
        'columns': [
          control('DataColumn', {'label': heading ?? 'A'}),
          control('DataColumn', {'label': 'B'}),
        ],
        'rows': [
          for (var r = 0; r < rows; r++)
            control('DataRow', {
              ...rowProps,
              if (selected.contains(r)) 'selected': true,
              'cells': [
                for (var c = 0; c < 2; c++)
                  control('DataCell', {
                    'content': content?.call(r, c) ??
                        (textControls
                            ? control('Text',
                                {'value': text?.call(r, c) ?? 'r$r c$c'})
                            : text?.call(r, c) ?? 'r$r c$c')
                  })
              ]
            })
        ],
      }),
      backend);

  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(
              body: SingleChildScrollView(
                  child: ControlWidget(control: table))))));
  await tester.pump();
  expect(tester.takeException(), isNull);
  return _Table(backend, table);
}

Future<void> _scrollTo(WidgetTester tester, double offset) async {
  tester
      .state<ScrollableState>(find.byType(Scrollable))
      .position
      .jumpTo(offset);
  await tester.pump();
  await tester.pump();
}

/// The header's select-all checkbox: the header is the last table.
Finder _headerCheckbox() => find
    .descendant(
        of: find.byType(DataTable).last, matching: find.byType(Checkbox))
    .first;

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
            matching: find.byWidgetPredicate(
                (w) => w is RepaintBoundary && w.child is DataTable)),
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

  testWidgets('a long table builds only the rows near the viewport',
      (tester) async {
    await _pumpTable(tester, {}, rows: 1000, text: (r, c) => 'r$r c$c');

    // Heading row (56) plus 1,000 rows of 48, as one DataTable would be.
    expect(tester.getSize(find.byType(DataTableControl)).height, 56 + 48000);
    expect(find.text('A'), findsOneWidget);
    expect(find.text('r0 c0'), findsOneWidget);
    expect(find.text('r29 c0'), findsOneWidget);
    expect(find.text('r60 c0'), findsNothing);
    expect(find.text('r500 c0'), findsNothing);
    expect(find.text('r999 c1'), findsNothing);

    // Rows are where one big table would put them.
    expect(tester.getTopLeft(find.text('r10 c0')).dy,
        moreOrLessEquals(tester.getTopLeft(find.text('r0 c0')).dy + 480));

    await _scrollTo(tester, 56 + 500 * 48);
    expect(find.text('r500 c0'), findsOneWidget);
    expect(tester.getTopLeft(find.text('r500 c0')).dy, lessThan(48));
    expect(find.text('r0 c0'), findsNothing);

    await _scrollTo(tester, 56 + 48000 - 600);
    expect(find.text('r999 c1'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('long table columns line up and fit text not yet shown',
      (tester) async {
    const long = 'a much, much longer value far down the table';
    await _pumpTable(tester, {},
        rows: 1000, text: (r, c) => r == 900 && c == 0 ? long : 'r$r c$c');

    final b = tester.getTopLeft(find.text('B')).dx;
    for (final cell in ['r0 c1', 'r9 c1', 'r10 c1', 'r25 c1']) {
      expect(tester.getTopLeft(find.text(cell)).dx, b, reason: cell);
    }
    // Column A is already wide enough for row 900.
    expect(
        b,
        greaterThan(
            tester.getSize(find.text(long, skipOffstage: false)).width));

    await _scrollTo(tester, 56 + 895 * 48);
    expect(tester.getTopLeft(find.text('B')).dx, b);
    expect(tester.getTopLeft(find.text('r900 c1')).dx, b);
    expect(tester.getTopRight(find.text(long)).dx, lessThan(b));
  });

  testWidgets('long table of Text controls fits text not yet shown',
      (tester) async {
    const long = 'a much, much longer value far down the table';
    await _pumpTable(tester, {},
        rows: 1000,
        textControls: true,
        text: (r, c) => r == 900 && c == 0 ? long : 'r$r c$c');

    final b = tester.getTopLeft(find.text('B')).dx;
    expect(tester.getTopLeft(find.text('r0 c1')).dx, b);
    await _scrollTo(tester, 56 + 895 * 48);
    expect(tester.getTopLeft(find.text('r900 c1')).dx, b);
    expect(tester.getTopRight(find.text(long)).dx, lessThan(b));
    expect(tester.takeException(), isNull);
  });

  testWidgets('long table header checkbox selects rows not yet shown',
      (tester) async {
    final table = await _pumpTable(tester, {'show_checkbox_column': true},
        rows: 300, rowProps: {'on_select_change': true});

    expect(find.byType(Checkbox), findsWidgets);
    final header = _headerCheckbox();
    expect(tester.widget<Checkbox>(header).value, false);

    await tester.tap(header);
    expect(table.backend.events, hasLength(300));
    expect(table.backend.events.first,
        (table.rows.first.id, 'select_change', true));
    expect(
        table.backend.events.last, (table.rows.last.id, 'select_change', true));
  });

  testWidgets('long table header checkbox shows rows selected out of view',
      (tester) async {
    await _pumpTable(tester, {'show_checkbox_column': true},
        rows: 300, rowProps: {'on_select_change': true}, selected: {250});
    expect(tester.widget<Checkbox>(_headerCheckbox()).value, isNull);
  });

  testWidgets('zero-height rows use the eager table', (tester) async {
    await _pumpTable(
        tester,
        {
          'data_row_min_height': 0.0,
          'data_row_max_height': 0.0,
        },
        rows: 100);

    expect(
        tester.widget<DataTable>(find.byType(DataTable)).rows, hasLength(100));
  });

  testWidgets('scaled tables build rows in the visible viewport',
      (tester) async {
    await _pumpTable(
        tester,
        {
          'scale': {
            'scale': 0.5,
            'alignment': {'x': -1.0, 'y': -1.0},
          },
        },
        rows: 1000);

    expect(
        tester.getTopLeft(find.text('r10 c0')).dy -
            tester.getTopLeft(find.text('r0 c0')).dy,
        240);
    await _scrollTo(tester, 5000);
    final row = find.text('r215 c0');
    expect(row, findsOneWidget);
    expect(tester.getTopLeft(row).dy, inInclusiveRange(0, 600));
  });

  testWidgets('long tables remeasure offscreen and visible text edits',
      (tester) async {
    final table = await _pumpTable(tester, {}, rows: 1000, textControls: true);
    final original = tester.getTopLeft(find.text('B')).dx;
    final content = table.rows[700].children('cells').first.child('content')!;
    const long = 'A much longer value in row 700';
    expect(find.text('r700 c0'), findsNothing);

    content.update({'value': long}, shouldNotify: true);
    await tester.pumpAndSettle();
    expect(find.text(long), findsNothing);
    final expanded = tester.getTopLeft(find.text('B')).dx;
    expect(expanded, greaterThan(original));

    await _scrollTo(tester, 56 + 700 * 48);
    expect(find.text(long), findsOneWidget);
    content.update({'value': 'r700 c0'}, shouldNotify: true);
    await tester.pumpAndSettle();
    expect(find.text('r700 c0'), findsOneWidget);
    expect(tester.getTopLeft(find.text('B')).dx, original);
    expect(tester.getTopLeft(find.text('r700 c1')).dx, original);
  });

  testWidgets('long tables remeasure when heading text shrinks',
      (tester) async {
    final table = await _pumpTable(tester, {},
        rows: 100,
        heading: {
          '_c': 'Text',
          '_i': 100000,
          'value': 'A long column heading'
        });
    final before = tester.getTopLeft(find.text('B')).dx;
    table.control
        .children('columns')
        .first
        .child('label')!
        .update({'value': 'A'}, shouldNotify: true);
    await tester.pumpAndSettle();
    final after = tester.getTopLeft(find.text('B')).dx;
    expect(after, lessThan(before));
    expect(tester.getTopLeft(find.text('r0 c1')).dx, after);
  });

  testWidgets('chunks realign when only a minimum column width grows',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(500, 600));
    addTearDown(() => tester.binding.setSurfaceSize(null));
    await _pumpTable(tester, {},
        rows: 1000,
        text: (r, c) => '${List.filled(9, 'word').join(' ')} r$r c$c',
        content: (r, c) => r == 700 && c == 0
            ? {'_c': 'Container', '_i': 100000, 'width': 340.0, 'height': 10.0}
            : null);
    final before = tester.getTopLeft(find.text('B')).dx;
    await _scrollTo(tester, 56 + 690 * 48);
    await tester.pumpAndSettle();

    final header = tester.getTopLeft(find.text('B')).dx;
    expect(header, greaterThan(before));
    for (final row in [690, 700]) {
      expect(tester.getTopLeft(find.textContaining('r$row c1')).dx, header);
    }
  });

  testWidgets('clipped table checkboxes are absent from accessibility',
      (tester) async {
    final semantics = tester.ensureSemantics();
    try {
      final table = await _pumpTable(
          tester,
          {
            'show_checkbox_column': true,
            'horizontal_lines': {'width': 2.0, 'color': 'red'},
          },
          rows: 100,
          rowProps: {'on_select_change': true});
      final header = find.descendant(
          of: find.byType(DataTable).last, matching: find.byType(Checkbox));
      final chunk = find.descendant(
          of: find.byType(DataTable).first, matching: find.byType(Checkbox));

      final owner = tester.binding.pipelineOwner.semanticsOwner!;
      final actionableNodes = <int>{};
      bool collectActions(SemanticsNode node) {
        final data = node.getSemanticsData();
        if (data.hasFlag(SemanticsFlag.isHidden)) return true;
        if (data.hasAction(SemanticsAction.tap)) actionableNodes.add(node.id);
        node.visitChildren(collectActions);
        return true;
      }

      collectActions(owner.rootSemanticsNode!);
      bool hasTap(Finder finder) =>
          actionableNodes.contains(tester.getSemantics(finder).id);

      expect(hasTap(header.first), isTrue);
      expect(hasTap(chunk.at(1)), isTrue);
      expect(hasTap(header.at(1)), isFalse);
      expect(hasTap(header.at(2)), isFalse);
      expect(hasTap(chunk.first), isFalse);
      owner.performAction(
          tester.getSemantics(header.first).id, SemanticsAction.tap);
      expect(table.backend.events, hasLength(100));
    } finally {
      semantics.dispose();
    }
  });
}
