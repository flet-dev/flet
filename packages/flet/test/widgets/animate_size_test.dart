import 'dart:convert';

import 'package:flet/src/controls/control_widget.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
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

  final events = <String>[];

  @override
  void triggerControlEvent(Control control, String eventName,
      [dynamic eventData]) {
    if (eventName == 'animation_end') events.add(eventData as String);
  }
}

const _half = Duration(milliseconds: 100);
const _boxInternals = {
  'skip_properties': ['width', 'height', 'margin']
};

Future<Control> _pumpControl(WidgetTester tester, Map<String, dynamic> props,
    {String type = 'Container', _Backend? backend}) async {
  backend ??= _Backend();
  final control = Control.fromMap(
      {'_c': type, '_i': 1, '_internals': _boxInternals, ...props}, backend);
  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(
              body: Align(
                  alignment: Alignment.topLeft,
                  child: ControlWidget(control: control))))));
  await tester.pumpAndSettle();
  return control;
}

Future<void> _update(
    WidgetTester tester, Control control, Map<String, dynamic> props) async {
  control.update(props, shouldNotify: true);
  await tester.pump();
}

void main() {
  for (final ink in [false, true]) {
    testWidgets(
        'decorated Container resizes its contents at each frame (ink=$ink)',
        (tester) async {
      final control = await _pumpControl(tester, {
        'animate_size': 200,
        'width': 100,
        'margin': 10,
        'bgcolor': 'green',
        'ink': ink,
        'on_click': ink,
        'content': {
          '_c': 'Container',
          '_i': 2,
          '_internals': _boxInternals,
          'height': 100
        },
      });
      final child = find.byWidgetPredicate(
          (w) => w is ControlWidget && w.control == control.child('content'));
      expect(tester.getSize(child).height, 100);

      await _update(tester, control, {'height': 0});
      await tester.pump(_half);
      expect(tester.getSize(child).height, closeTo(50, 0.01));
      expect(tester.getTopLeft(child).dy, 10);
      await tester.pumpAndSettle();
      expect(tester.getSize(child).height, 0);

      await _update(tester, control, {'height': null});
      await tester.pump(_half);
      expect(tester.getSize(child).height, closeTo(50, 0.01));
      // Reverse before the natural-size transition has finished.
      await _update(tester, control, {'height': 200});
      await tester.pump(_half);
      expect(tester.getSize(child).height, closeTo(125, 0.01));
      await tester.pumpAndSettle();
      expect(tester.getSize(child).height, 200);
    });
  }

  testWidgets(
      'natural size animates new text and follows parent constraints immediately',
      (tester) async {
    final control = await _pumpControl(tester, {
      'animate_size': 200,
      'content': {'_c': 'Text', '_i': 2, 'value': 'one'},
    });
    final text = control.child('content')!;
    final child =
        find.byWidgetPredicate((w) => w is ControlWidget && w.control == text);
    final first = tester.getSize(child);
    await _update(tester, text, {'value': 'one\ntwo\nthree'});
    await tester.pump(_half);
    final middle = tester.getSize(child);
    await tester.pumpAndSettle();
    expect(middle.height, greaterThan(first.height));
    expect(middle.height, lessThan(tester.getSize(child).height));

    await tester.binding.setSurfaceSize(const Size(15, 500));
    addTearDown(() => tester.binding.setSurfaceSize(null));
    await tester.pump();
    final resized = tester.getSize(child);
    expect(resized.width, lessThanOrEqualTo(15));
    expect(resized.height, greaterThan(middle.height));
    await tester.pump(_half);
    expect(tester.getSize(child), resized);
  });

  testWidgets(
      'width-only animation measures wrapping text at each intermediate width',
      (tester) async {
    const value = 'each word wraps as the width of the container changes';
    final control = await _pumpControl(tester, {
      'width': 240,
      'animate_size': 200,
      'content': {'_c': 'Text', '_i': 2, 'value': value},
    });
    final text = find.text(value);
    await _update(tester, control, {'width': 80});
    await tester.pump(_half);
    final animated = tester.getSize(text);
    expect(animated.width, 160);

    await _update(tester, control, {'width': 160, 'animate_size': false});
    expect(tester.getSize(text), animated);
  });

  testWidgets('toggling size animation preserves text field state and focus',
      (tester) async {
    final control = await _pumpControl(tester, {
      'width': 240,
      'content': {'_c': 'TextField', '_i': 2},
    });
    final field = find.byType(EditableText);
    await tester.enterText(field, 'still editing');
    final state = tester.state<EditableTextState>(field);
    for (final setting in [200, false]) {
      await _update(tester, control, {'animate_size': setting});
      expect(tester.state(field), same(state));
      expect(state.widget.focusNode.hasFocus, isTrue);
      expect(state.widget.controller.text, 'still editing');
    }
  });

  testWidgets(
      'container and size animations keep independent timings and completion events',
      (tester) async {
    final backend = _Backend();
    final control = await _pumpControl(
        tester,
        {
          'width': 40,
          'height': 40,
          'animate': 200,
          'margin': 0,
          'on_animation_end': true,
          'content': {'_c': 'Container', '_i': 2, '_internals': _boxInternals},
        },
        backend: backend);
    final child = find.byWidgetPredicate(
        (w) => w is ControlWidget && w.control == control.child('content'));
    await _update(tester, control, {'width': 200, 'margin': 20});
    await tester.pump(_half);
    expect(tester.getSize(child).width, 120);
    expect(tester.getTopLeft(child).dx, 10);
    await tester.pumpAndSettle();
    expect(backend.events, ['container']);

    backend.events.clear();
    await _update(
        tester, control, {'animate_size': 400, 'width': 40, 'margin': 0});
    await tester.pump(const Duration(milliseconds: 200));
    expect(tester.getSize(child).width, 120);
    expect(tester.getTopLeft(child).dx, 0);
    await tester.pump(const Duration(milliseconds: 1));
    expect(backend.events, ['container']);
    await tester.pumpAndSettle();
    expect(backend.events, ['container', 'size']);

    backend.events.clear();
    await _update(tester, control, {'width': 100});
    await tester.pumpAndSettle();
    expect(backend.events, ['size']);

    backend.events.clear();
    await _update(tester, control, {'animate_size': false});
    await _update(tester, control, {'width': 200});
    await tester.pumpAndSettle();
    expect(backend.events, ['container']);
  });

  testWidgets('Image animates the painted raster', (tester) async {
    final control = await _pumpControl(
        tester,
        {
          'src': base64Decode(
              'iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+KAAAADElEQVR4nGNg+A+BAA/5A/3YOXFBAAAAAElFTkSuQmCC'),
          'width': 40,
          'height': 40,
          'animate_size': 200,
        },
        type: 'Image');
    final source = find.byType(Image);
    await tester.runAsync(() => precacheImage(
        tester.widget<Image>(source).image, tester.element(source)));
    await tester.pump();
    final image = find.byType(RawImage);
    expect(tester.widget<RawImage>(image).image?.width, 2);
    await _update(tester, control, {'height': 200});
    await tester.pump(_half);
    expect(tester.getSize(image), const Size(40, 120));
    await tester.pumpAndSettle();
    expect(tester.getSize(image).height, 200);

    await _update(tester, control, {'height': null});
    await tester.pump(_half);
    expect(tester.getSize(image), const Size(40, 110));
    await tester.pumpAndSettle();
    expect(tester.getSize(image), const Size(40, 20));
  });
}
