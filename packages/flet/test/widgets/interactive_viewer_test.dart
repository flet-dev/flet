import 'package:flet/src/controls/interactive_viewer.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

/// Pumps an InteractiveViewer built from the same message shape the client
/// receives from Python.
Future<void> _pumpViewer(WidgetTester tester, {Object? alignment}) async {
  final backend = FletBackend(
      pageUri: Uri.parse('http://localhost'),
      assetsDir: '',
      extensions: [FletCoreExtension()],
      multiView: false);
  final viewer = Control.fromMap(<dynamic, dynamic>{
    '_c': 'InteractiveViewer',
    '_i': 1,
    if (alignment != null) 'alignment': alignment,
    'content': <dynamic, dynamic>{'_c': 'Text', '_i': 2, 'value': 'content'},
  }, backend);
  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(body: InteractiveViewerControl(control: viewer)))));
}

/// The alignment the control passed to Flutter's [InteractiveViewer].
Alignment? _passedAlignment(WidgetTester tester) =>
    tester.widget<InteractiveViewer>(find.byType(InteractiveViewer)).alignment;

void main() {
  testWidgets('InteractiveViewer renders its content when alignment is set',
      (tester) async {
    await _pumpViewer(tester, alignment: <dynamic, dynamic>{'x': 0, 'y': 0});

    expect(tester.takeException(), isNull);
    expect(find.text('content'), findsOneWidget);
    expect(_passedAlignment(tester), Alignment.center);
  });

  testWidgets('InteractiveViewer passes no alignment when none is set',
      (tester) async {
    await _pumpViewer(tester);

    expect(tester.takeException(), isNull);
    expect(find.text('content'), findsOneWidget);
    expect(_passedAlignment(tester), isNull);
  });
}
