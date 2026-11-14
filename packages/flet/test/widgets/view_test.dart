import 'package:flet/src/controls/view.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

/// Records the events controls send to Python as `[controlId, name, data]`.
class _EventBackend extends FletBackend {
  _EventBackend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [FletCoreExtension()],
            multiView: false) {
    isLoading = false;
  }

  final events = <List<dynamic>>[];

  @override
  void triggerControlEventById(int controlId, String eventName,
      [dynamic eventData]) {
    events.add([controlId, eventName, eventData]);
  }
}

/// Keeps the hand-built pages alive: a control holds its parent weakly.
final _pages = <Control>[];

/// Builds a page holding one `View` per entry of [viewProps], with ids 10, 11…
List<Control> _buildViews(
    FletBackend backend, List<Map<String, dynamic>> viewProps) {
  final page =
      Control(id: 1, type: 'Page', properties: {'views': []}, backend: backend);
  final views = [
    for (var i = 0; i < viewProps.length; i++)
      Control(
          id: 10 + i,
          type: 'View',
          parent: page,
          properties: {'route': '/$i', ...viewProps[i]},
          backend: backend),
  ];
  page.properties['views'] = views;
  _pages.add(page);
  return views;
}

Widget _app(FletBackend backend, Widget home) =>
    ChangeNotifierProvider<FletBackend>.value(
        value: backend, child: MaterialApp(home: home));

Future<void> _setSurfaceSize(WidgetTester tester, Size size) async {
  addTearDown(() => tester.binding.setSurfaceSize(null));
  await tester.binding.setSurfaceSize(size);
}

void main() {
  group('View', () {
    testWidgets('reports its size through on_size_change', (tester) async {
      await _setSurfaceSize(tester, const Size(800, 600));
      final backend = _EventBackend();
      final view = _buildViews(backend, [
        {'on_size_change': true, 'size_change_interval': 0}
      ]).first;

      await tester.pumpWidget(_app(backend, ViewControl(control: view)));
      await tester.pump();
      expect(tester.takeException(), isNull);
      expect(backend.events, [
        [
          10,
          'size_change',
          {'w': 800.0, 'h': 600.0}
        ]
      ]);

      backend.events.clear();
      await tester.binding.setSurfaceSize(const Size(1024, 700));
      await tester.pump();
      await tester.pump();
      expect(backend.events, [
        [
          10,
          'size_change',
          {'w': 1024.0, 'h': 700.0}
        ]
      ]);
    });

    testWidgets('sends no size events without on_size_change', (tester) async {
      await _setSurfaceSize(tester, const Size(800, 600));
      final backend = _EventBackend();
      final view = _buildViews(backend, [{}]).first;

      await tester.pumpWidget(_app(backend, ViewControl(control: view)));
      await tester.binding.setSurfaceSize(const Size(1024, 700));
      await tester.pump();
      await tester.pump();
      expect(tester.takeException(), isNull);
      expect(backend.events, isEmpty);
    });

    testWidgets('applies inherited layout properties', (tester) async {
      await _setSurfaceSize(tester, const Size(800, 600));
      final backend = _EventBackend();
      final view = _buildViews(backend, [
        {
          'margin': {'left': 20.0, 'top': 30.0, 'right': 20.0, 'bottom': 30.0},
          'opacity': 0.5,
        }
      ]).first;

      await tester.pumpWidget(_app(backend, ViewControl(control: view)));
      expect(tester.takeException(), isNull);
      expect(tester.getSize(find.byType(Scaffold)), const Size(760, 540));
      expect(tester.widget<Opacity>(find.byType(Opacity)).opacity, 0.5);
    });

    testWidgets('keeps its scaffold state when on_size_change is toggled',
        (tester) async {
      await _setSurfaceSize(tester, const Size(800, 600));
      final backend = _EventBackend();
      final view = _buildViews(backend, [{}]).first;

      await tester.pumpWidget(_app(backend, ViewControl(control: view)));
      final scaffoldState = tester.state<ScaffoldState>(find.byType(Scaffold));

      view.properties['on_size_change'] = true;
      view.properties['size_change_interval'] = 0;
      await tester.pumpWidget(_app(backend, ViewControl(control: view)));
      await tester.pump();
      expect(tester.takeException(), isNull);
      expect(tester.state<ScaffoldState>(find.byType(Scaffold)),
          same(scaffoldState));
      expect(backend.events.map((e) => e[1]), ['size_change']);

      view.properties['on_size_change'] = false;
      backend.events.clear();
      await tester.pumpWidget(_app(backend, ViewControl(control: view)));
      await tester.binding.setSurfaceSize(const Size(500, 500));
      await tester.pump();
      await tester.pump();
      expect(tester.takeException(), isNull);
      expect(backend.events, isEmpty);
      expect(tester.state<ScaffoldState>(find.byType(Scaffold)),
          same(scaffoldState));
    });

    testWidgets('a covered view reports the new size once uncovered',
        (tester) async {
      await _setSurfaceSize(tester, const Size(800, 600));
      final backend = _EventBackend();
      final views = _buildViews(backend, [
        {'on_size_change': true, 'size_change_interval': 0},
        {'on_size_change': true, 'size_change_interval': 0},
      ]);

      Widget navigator(List<Control> shown) => _app(
          backend,
          Navigator(pages: [
            for (final v in shown)
              MaterialPage(
                  key: ValueKey(v.properties['route']),
                  child: ViewControl(control: v))
          ], onDidRemovePage: (_) {}));

      await tester.pumpWidget(navigator([views[0]]));
      await tester.pumpAndSettle();
      await tester.pumpWidget(navigator([views[0], views[1]]));
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(backend.events.map((e) => e[0]), [10, 11]);

      backend.events.clear();
      await tester.binding.setSurfaceSize(const Size(640, 480));
      await tester.pump();
      await tester.pump();
      expect(backend.events.map((e) => [e[0], e[2]]), [
        [
          11,
          {'w': 640.0, 'h': 480.0}
        ],
      ]);

      backend.events.clear();
      await tester.pumpWidget(navigator([views[0]]));
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(backend.events.map((e) => [e[0], e[2]]), [
        [
          10,
          {'w': 640.0, 'h': 480.0}
        ],
      ]);
    });
  });
}
