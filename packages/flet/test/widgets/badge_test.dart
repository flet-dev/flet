import 'package:flet/src/controls/control_widget.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

/// Records the names of the events controls send to Python.
class _EventBackend extends FletBackend {
  _EventBackend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [FletCoreExtension()],
            multiView: false);

  final events = <String>[];

  @override
  void triggerControlEvent(Control control, String eventName, [dynamic data]) {
    events.add(eventName);
  }
}

/// Shows [control] in an app backed by [backend].
Future<void> _pump(WidgetTester tester, FletBackend backend, Control control) =>
    tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
        value: backend,
        child: MaterialApp(
            home: Scaffold(
                body: Center(child: ControlWidget(control: control))))));

/// Shows a `PopupMenuButton` with a `Badge`, opens its menu, applies
/// [changeBadge] while the menu is open, then closes the menu by selecting
/// its item or tapping outside, and returns the events the button sent.
Future<List<String>> _openChangeAndClose(
  WidgetTester tester, {
  required Map<String, dynamic>? badge,
  required void Function(Control popup) changeBadge,
  required bool select,
}) async {
  final backend = _EventBackend();
  final popup = Control.fromMap({
    '_c': 'PopupMenuButton',
    '_i': 1,
    'on_open': true,
    'on_cancel': true,
    'on_select': true,
    if (badge != null) 'badge': {'_c': 'Badge', '_i': 2, ...badge},
    'items': [
      {'_c': 'PopupMenuItem', '_i': 3, 'content': 'Item'}
    ],
  }, backend);
  await _pump(tester, backend, popup);

  await tester.tap(find.byType(PopupMenuButton<String>));
  await tester.pumpAndSettle();
  changeBadge(popup);
  await tester.pumpAndSettle();
  if (select) {
    await tester.tap(find.text('Item').last);
  } else {
    await tester.tapAt(const Offset(5, 5));
  }
  await tester.pumpAndSettle();
  expect(tester.takeException(), isNull);
  return backend.events;
}

/// A `Container` with a text badge.
Map<String, dynamic> _badgedContainer(int id) => {
      '_c': 'Container',
      '_i': id,
      'width': 50,
      'height': 50,
      'badge': '1',
      'content': {'_c': 'Text', '_i': id + 1, 'value': 'Badged'},
    };

void main() {
  group('Badge keeps the state of the control it decorates', () {
    for (final (from, to) in [(false, true), (true, false)]) {
      for (final select in [false, true]) {
        final closing = select ? 'select' : 'cancel';
        testWidgets(
            'PopupMenuButton reports $closing after label_visible '
            '$from -> $to while open', (tester) async {
          final events = await _openChangeAndClose(tester,
              badge: {'label_visible': from},
              changeBadge: (popup) => (popup.get('badge') as Control)
                  .update({'label_visible': to}, shouldNotify: true),
              select: select);
          expect(events,
              select ? ['open', 'click', 'select'] : ['open', 'cancel']);
        });
      }
    }

    testWidgets('PopupMenuButton reports cancel after its badge is replaced',
        (tester) async {
      final events = await _openChangeAndClose(tester,
          badge: {'label_visible': false}, changeBadge: (popup) {
        popup.properties['badge'] = Control.fromMap(
            {'_c': 'Badge', '_i': 4, 'label_visible': true}, popup.backend,
            parent: popup);
        popup.notify();
      }, select: false);
      expect(events, ['open', 'cancel']);
    });

    for (final select in [false, true]) {
      final closing = select ? 'select' : 'cancel';
      final expected =
          select ? ['open', 'click', 'select'] : ['open', 'cancel'];

      testWidgets('PopupMenuButton reports $closing after its badge is removed',
          (tester) async {
        final events = await _openChangeAndClose(tester,
            badge: {'label_visible': true},
            changeBadge: (popup) =>
                popup.update({'badge': null}, shouldNotify: true),
            select: select);
        expect(events, expected);
      });

      testWidgets('PopupMenuButton reports $closing after a badge is added',
          (tester) async {
        final events = await _openChangeAndClose(tester, badge: null,
            changeBadge: (popup) {
          popup.properties['badge'] = Control.fromMap(
              {'_c': 'Badge', '_i': 4}, popup.backend,
              parent: popup);
          popup.notify();
        }, select: select);
        expect(events, expected);
      });
    }

    testWidgets('PopupMenuButton reports cancel after its badge color changes',
        (tester) async {
      final events = await _openChangeAndClose(tester,
          badge: {'label_visible': true},
          changeBadge: (popup) => (popup.get('badge') as Control)
              .update({'bgcolor': 'red'}, shouldNotify: true),
          select: false);
      expect(events, ['open', 'cancel']);
    });
  });

  // These widgets mount the same content twice at once.
  group('Badged content shown twice at once', () {
    testWidgets('Draggable with the default feedback', (tester) async {
      final backend = _EventBackend();
      final draggable = Control.fromMap({
        '_c': 'Draggable',
        '_i': 1,
        'content': _badgedContainer(2),
      }, backend);
      await _pump(tester, backend, draggable);

      final gesture =
          await tester.startGesture(tester.getCenter(find.text('Badged')));
      await gesture.moveBy(const Offset(40, 40));
      await tester.pump();
      expect(tester.takeException(), isNull);
      // At the source and in the feedback.
      expect(find.text('Badged'), findsNWidgets(2));
      await gesture.up();
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
    });

    testWidgets('DropdownM2 option', (tester) async {
      final backend = _EventBackend();
      final dropdown = Control.fromMap({
        '_c': 'DropdownM2',
        '_i': 1,
        'value': 'a',
        'options': [
          {'_c': 'Option', '_i': 2, 'key': 'a', 'content': _badgedContainer(3)}
        ],
      }, backend);
      await _pump(tester, backend, dropdown);

      await tester.tap(find.text('Badged'));
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      // In the button and in the open menu.
      expect(find.text('Badged'), findsNWidgets(2));
    });

    testWidgets('Dropdown option', (tester) async {
      final backend = _EventBackend();
      final dropdown = Control.fromMap({
        '_c': 'Dropdown',
        '_i': 1,
        'options': [
          {
            '_c': 'DropdownOption',
            '_i': 2,
            'key': 'a',
            'content': _badgedContainer(3)
          }
        ],
      }, backend);
      await _pump(tester, backend, dropdown);

      await tester.tap(find.byType(TextField));
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
    });

    testWidgets('CupertinoContextMenu', (tester) async {
      final backend = _EventBackend();
      final menu = Control.fromMap({
        '_c': 'CupertinoContextMenu',
        '_i': 1,
        'content': _badgedContainer(2),
        'actions': [
          {'_c': 'CupertinoContextMenuAction', '_i': 4, 'content': 'Action'}
        ],
      }, backend);
      await _pump(tester, backend, menu);

      // Hold until the menu opens.
      final gesture =
          await tester.startGesture(tester.getCenter(find.text('Badged')));
      for (var i = 0; i < 20; i++) {
        await tester.pump(const Duration(milliseconds: 100));
      }
      expect(tester.takeException(), isNull);
      await gesture.up();
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.text('Action'), findsOneWidget);
    });
  });

  group('Badged control positioned in a Stack', () {
    for (final visible in [true, false]) {
      testWidgets('label_visible: $visible', (tester) async {
        final backend = _EventBackend();
        final stack = Control.fromMap({
          '_c': 'Stack',
          '_i': 1,
          '_internals': {'host_positioned': true},
          'width': 200,
          'height': 200,
          'controls': [
            {
              '_c': 'Text',
              '_i': 2,
              'value': 'Positioned',
              'left': 10,
              'top': 20,
              'badge': {
                '_c': 'Badge',
                '_i': 3,
                'label': 'L',
                'label_visible': visible
              },
            }
          ],
        }, backend);
        await _pump(tester, backend, stack);

        expect(tester.takeException(), isNull);
        final origin = tester.getTopLeft(find.byType(Stack).first);
        final text = tester.getRect(find.text('Positioned'));
        expect(text.topLeft, origin + const Offset(10, 20));
        if (visible) {
          // At the top end of the text, not of the whole Stack.
          final label = tester.getCenter(find.text('L'));
          expect((label - text.topRight).distance, lessThan(20));
        } else {
          expect(find.text('L'), findsNothing);
        }
      });
    }
  });
}
