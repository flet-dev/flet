import 'package:flet/src/controls/control_widget.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/services.dart';
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

/// Shows a `shift_enter` text field of type [type], focuses it and returns
/// the backend that records its events.
Future<_EventBackend> _pumpField(WidgetTester tester, String type) async {
  final backend = _EventBackend();
  final field = Control.fromMap({
    '_c': type,
    '_i': 1,
    'shift_enter': true,
    'on_submit': true,
  }, backend);
  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(body: Center(child: ControlWidget(control: field))))));
  await tester.showKeyboard(find.byType(EditableText));
  return backend;
}

void main() {
  for (final type in ['TextField', 'CupertinoTextField']) {
    group('$type with shift_enter', () {
      testWidgets('Enter submits when no IME is composing', (tester) async {
        final backend = await _pumpField(tester, type);
        tester.testTextInput.updateEditingValue(const TextEditingValue(
            text: 'hello', selection: TextSelection.collapsed(offset: 5)));
        await tester.pump();

        await tester.sendKeyEvent(LogicalKeyboardKey.enter);
        expect(backend.events.where((e) => e == 'submit'), hasLength(1));
      });

      testWidgets('Enter does not submit while an IME is composing',
          (tester) async {
        final backend = await _pumpField(tester, type);
        tester.testTextInput.updateEditingValue(const TextEditingValue(
            text: 'nihao',
            selection: TextSelection.collapsed(offset: 5),
            composing: TextRange(start: 0, end: 5)));
        await tester.pump();

        await tester.sendKeyEvent(LogicalKeyboardKey.enter);
        expect(backend.events, isNot(contains('submit')));

        // The IME commits the text; the next Enter submits.
        tester.testTextInput.updateEditingValue(const TextEditingValue(
            text: 'nihao', selection: TextSelection.collapsed(offset: 5)));
        await tester.pump();
        await tester.sendKeyEvent(LogicalKeyboardKey.enter);
        expect(backend.events.where((e) => e == 'submit'), hasLength(1));
      });
    });
  }
}
