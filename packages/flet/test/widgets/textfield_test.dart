import 'package:flet/src/controls/control_widget.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

/// Records the property updates and events controls send to Python.
class _RecordingBackend extends FletBackend {
  _RecordingBackend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [FletCoreExtension()],
            multiView: false);

  final updates = <Map<String, dynamic>>[];
  final events = <String>[];

  @override
  void updateControl(int id, Map<String, dynamic> props,
      {bool dart = true, bool python = true, bool notify = false}) {
    if (python) updates.add(Map.of(props));
    super.updateControl(id, props, dart: dart, python: false, notify: notify);
  }

  @override
  void triggerControlEvent(Control control, String eventName, [dynamic data]) {
    events.add(eventName);
  }
}

/// Shows a text field of type [type] and returns it with its backend.
Future<(Control, _RecordingBackend)> _pumpField(
    WidgetTester tester, String type) async {
  final backend = _RecordingBackend();
  final field =
      Control.fromMap({'_c': type, '_i': 1, 'on_change': true}, backend);
  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(body: Center(child: ControlWidget(control: field))))));
  return (field, backend);
}

void main() {
  for (final type in ['TextField', 'CupertinoTextField']) {
    group('$type.clear()', () {
      testWidgets('empties typed text and reports an empty value',
          (tester) async {
        final (field, backend) = await _pumpField(tester, type);
        await tester.enterText(find.byType(EditableText), 'hello');
        await tester.pump();
        backend.updates.clear();
        backend.events.clear();

        await field.invokeMethod('clear', null, const Duration(seconds: 1));
        await tester.pump();

        expect(
            tester
                .widget<EditableText>(find.byType(EditableText))
                .controller
                .text,
            isEmpty);
        expect(backend.updates, [
          {'value': ''}
        ]);
        expect(backend.events, isNot(contains('change')));
      });
    });
  }
}
