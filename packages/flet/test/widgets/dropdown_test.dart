import 'package:flet/src/controls/dropdown.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/models/control.dart';
import 'package:material_ui/material_ui.dart';
import 'package:flutter_test/flutter_test.dart';

class _TestBackend extends FletBackend {
  _TestBackend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [],
            multiView: false);
}

void main() {
  testWidgets('Dropdown.expanded_insets is applied when expand is set',
      (tester) async {
    final backend = _TestBackend();
    final control = Control(
        id: 1,
        type: 'Dropdown',
        properties: {
          'expand': 1,
          'expanded_insets': {
            'left': 40.0,
            'top': 0.0,
            'right': 40.0,
            'bottom': 0.0
          },
          'options': [],
        },
        backend: backend);

    await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: DropdownControl(control: control))));

    expect(tester.takeException(), isNull);
    final menu =
        tester.widget<DropdownMenu<String>>(find.byType(DropdownMenu<String>));
    expect(menu.expandedInsets, const EdgeInsets.fromLTRB(40, 0, 40, 0));
  });

  testWidgets(
      'Dropdown falls back to zero insets when expand is set without expanded_insets',
      (tester) async {
    final backend = _TestBackend();
    final control = Control(
        id: 1,
        type: 'Dropdown',
        properties: {
          'expand': 1,
          'options': [],
        },
        backend: backend);

    await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: DropdownControl(control: control))));

    expect(tester.takeException(), isNull);
    final menu =
        tester.widget<DropdownMenu<String>>(find.byType(DropdownMenu<String>));
    expect(menu.expandedInsets, EdgeInsets.zero);
  });

  testWidgets('Dropdown has null expandedInsets when not expanded',
      (tester) async {
    final backend = _TestBackend();
    final control = Control(
        id: 1,
        type: 'Dropdown',
        properties: {
          'expanded_insets': {
            'left': 40.0,
            'top': 0.0,
            'right': 40.0,
            'bottom': 0.0
          },
          'options': [],
        },
        backend: backend);

    await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: DropdownControl(control: control))));

    expect(tester.takeException(), isNull);
    final menu =
        tester.widget<DropdownMenu<String>>(find.byType(DropdownMenu<String>));
    expect(menu.expandedInsets, isNull);
  });
}
