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

/// Shows a `PopupMenuButton` with a `Badge`, opens its menu, applies
/// [changeBadge] while the menu is open, then closes the menu by selecting
/// its item or tapping outside, and returns the events the button sent.
Future<List<String>> _openChangeAndClose(
  WidgetTester tester, {
  required Map<String, dynamic> badge,
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
    'badge': {'_c': 'Badge', '_i': 2, ...badge},
    'items': [
      {'_c': 'PopupMenuItem', '_i': 3, 'content': 'Item'}
    ],
  }, backend);
  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(body: Center(child: ControlWidget(control: popup))))));

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
}
