import 'package:flet/src/controls/list_tile.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

class _EventBackend extends FletBackend {
  _EventBackend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [],
            multiView: false);

  final events = <String>[];

  @override
  void triggerControlEvent(Control control, String eventName, [dynamic data]) {
    events.add(eventName);
  }
}

void main() {
  for (final layout in [
    'row',
    'intrinsic row',
    'width',
    'expanded',
    'column'
  ]) {
    for (final disabled in [false, true]) {
      testWidgets('ListTile gestures in $layout, disabled=$disabled',
          (tester) async {
        const surfaceSize = Size(800, 600);
        addTearDown(() => tester.binding.setSurfaceSize(null));
        await tester.binding.setSurfaceSize(surfaceSize);

        final backend = _EventBackend();
        final parent = Control(
            id: 1,
            type: layout == 'column' ? 'Column' : 'Row',
            properties: {
              '_internals': {'host_expanded': true}
            },
            backend: backend);
        final control = Control(
            id: 2,
            type: 'ListTile',
            parent: parent,
            properties: {
              'title': 'Two-line',
              'subtitle': 'Here is a second title.',
              'on_click': true,
              'on_long_press': true,
              'disabled': disabled,
              if (layout == 'width') 'width': 300.0,
              if (layout == 'expanded') 'expand': 1,
            },
            backend: backend);
        final tile = ListTileControl(control: control);
        Widget content = layout == 'column'
            ? Column(children: [tile])
            : Row(children: [tile]);
        if (layout == 'intrinsic row') {
          content = IntrinsicHeight(child: content);
        }
        await tester.pumpWidget(
            MaterialApp(home: Scaffold(body: SafeArea(child: content))));

        expect(tester.takeException(), isNull);
        final size = tester.getSize(find.byType(ListTile));
        expect(size.width.isFinite, isTrue);
        expect(size.width, greaterThan(0));
        if (layout == 'width') {
          expect(size.width, 300);
        } else if (layout == 'expanded' || layout == 'column') {
          expect(size.width, surfaceSize.width);
        }

        backend.events.clear();
        await tester.tap(find.text('Two-line'));
        await tester.pumpAndSettle();
        expect(backend.events, disabled ? isEmpty : ['click']);

        backend.events.clear();
        await tester.longPress(find.text('Two-line'));
        await tester.pumpAndSettle();
        expect(backend.events, disabled ? isEmpty : ['long_press']);
        expect(tester.takeException(), isNull);
      });
    }
  }
}
