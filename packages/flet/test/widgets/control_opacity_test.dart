import 'package:flet/src/controls/base_controls.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';

class _Backend extends FletBackend {
  _Backend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [],
            multiView: false);
}

class _Counter extends StatefulWidget {
  const _Counter();

  @override
  State<_Counter> createState() => _CounterState();
}

class _CounterState extends State<_Counter> {
  int value = 0;

  @override
  Widget build(BuildContext context) =>
      const SizedBox(width: 10, height: 10, child: ColoredBox(color: Colors.red));
}

void main() {
  final backend = _Backend();

  Future<void> pump(WidgetTester tester, double? opacity) {
    final control = Control(
        id: 1,
        type: 'Container',
        properties: {if (opacity != null) 'opacity': opacity},
        backend: backend);
    return tester.pumpWidget(Directionality(
        textDirection: TextDirection.ltr,
        child: Center(
            child: LayoutControl(control: control, child: const _Counter()))));
  }

  int opacityLayers(WidgetTester tester) =>
      tester.layers.whereType<OpacityLayer>().length;

  testWidgets('a control at full opacity paints without its own layer',
      (tester) async {
    await pump(tester, null);
    expect(opacityLayers(tester), 0);
    expect(find.byType(ColoredBox), findsOneWidget);

    await pump(tester, 1.0);
    expect(opacityLayers(tester), 0);
  });

  testWidgets('partial opacity uses a layer, 0 paints nothing',
      (tester) async {
    await pump(tester, 0.5);
    expect(tester.layers.whereType<OpacityLayer>().single.alpha, 128);

    await pump(tester, 0.0);
    expect(opacityLayers(tester), 0);
    expect(tester.layers.whereType<PictureLayer>(), isEmpty);
  });

  testWidgets('changing opacity keeps the child state', (tester) async {
    await pump(tester, null);
    tester.state<_CounterState>(find.byType(_Counter)).value = 7;

    for (final opacity in [0.5, 0.0, 1.0, 0.3]) {
      await pump(tester, opacity);
      expect(tester.state<_CounterState>(find.byType(_Counter)).value, 7);
    }
  });
}
