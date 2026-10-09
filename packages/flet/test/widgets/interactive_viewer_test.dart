import 'package:flet/src/controls/interactive_viewer.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

class _TransformEvents extends FletBackend {
  _TransformEvents()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [],
            multiView: false);

  final List<Map<String, dynamic>> payloads = [];

  @override
  void triggerControlEvent(Control control, String eventName,
      [dynamic eventData]) {
    if (eventName == 'transform_changed' && eventData is Map) {
      payloads.add(Map<String, dynamic>.from(eventData));
    }
  }
}

const Duration _methodTimeout = Duration(seconds: 2);

Future<Control> _pumpViewer(
  WidgetTester tester,
  _TransformEvents backend, {
  required int interval,
}) async {
  final Control content = Control(
      id: 2,
      type: 'Container',
      properties: {'width': 200.0, 'height': 200.0},
      backend: backend);
  final Control control = Control(
      id: 1,
      type: 'InteractiveViewer',
      properties: {
        'width': 200.0,
        'height': 200.0,
        'min_scale': 0.5,
        'max_scale': 4.0,
        'boundary_margin': 100.0,
        'interaction_end_friction_coefficient': 0.05,
        'content': content,
        'interaction_update_interval': interval,
        'on_transform_changed': true,
      },
      backend: backend);

  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(body: InteractiveViewerControl(control: control)))));
  expect(tester.takeException(), isNull);
  return control;
}

Future<dynamic> _call(Control control, String name, Map<String, dynamic> args) {
  return control.invokeMethod(name, args, _methodTimeout);
}

double _scale(Map<String, dynamic> payload) => (payload['s'] as num).toDouble();

/// Lets inertial animation finish, then the trailing transform event.
Future<void> _finishTransform(WidgetTester tester) async {
  await tester.pumpAndSettle();
  await tester.pump(const Duration(seconds: 1));
}

void _expectLastMatches(Map<String, dynamic> payload, dynamic transform) {
  expect(payload['s'], transform['s']);
  expect(payload['tx'], transform['tx']);
  expect(payload['ty'], transform['ty']);
  expect(payload['tz'], transform['tz']);
  expect(payload['m'], transform['m']);
}

void main() {
  testWidgets('get_scale and get_transform report the identity transform',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 0);

    final scale = await _call(control, 'get_scale', {});
    final transform = await _call(control, 'get_transform', {});

    expect(scale, 1.0);
    expect(transform['s'], 1.0);
    expect(transform['tx'], 0.0);
    expect(transform['ty'], 0.0);
    expect(transform['tz'], 0.0);
    expect(transform['m'], hasLength(16));
    expect(backend.payloads, isEmpty);
  });

  testWidgets('consecutive zoom, reset and pan update the effective transform',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 0);

    await _call(control, 'zoom', {'factor': 2.0});
    await _call(control, 'zoom', {'factor': 1.5});
    expect(await _call(control, 'get_scale', {}), closeTo(3.0, 1e-9));
    expect(backend.payloads, hasLength(2));
    expect(_scale(backend.payloads[0]), closeTo(2.0, 1e-9));
    expect(_scale(backend.payloads[1]), closeTo(3.0, 1e-9));

    await _call(control, 'reset', {});
    expect(await _call(control, 'get_scale', {}), 1.0);
    expect(_scale(backend.payloads.last), 1.0);
    expect(backend.payloads.last['tx'], 0.0);
    expect(backend.payloads.last['ty'], 0.0);

    await _call(control, 'pan', {'dx': 30.0, 'dy': -20.0});
    final transform = await _call(control, 'get_transform', {});
    expect(transform['s'], 1.0);
    expect(transform['tx'], closeTo(30.0, 1e-6));
    expect(transform['ty'], closeTo(-20.0, 1e-6));
    expect(transform['m'], hasLength(16));
    expect(backend.payloads.last['tx'], closeTo(30.0, 1e-6));
    expect(backend.payloads.last['ty'], closeTo(-20.0, 1e-6));
  });

  testWidgets('mouse-wheel zoom changes the effective scale', (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 0);
    final Offset center = tester.getCenter(find.byType(InteractiveViewer));

    await tester.sendEventToBinding(PointerScrollEvent(
      position: center,
      scrollDelta: const Offset(0, -120),
    ));
    await tester.pump();

    final scale = await _call(control, 'get_scale', {});
    expect(scale, greaterThan(1.0));
    expect(backend.payloads, isNotEmpty);
    expect(_scale(backend.payloads.last), scale);
    expect(backend.payloads.last['m'], hasLength(16));
  });

  testWidgets('transform events keep the interval and one trailing final state',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 1000);

    await _call(control, 'zoom', {'factor': 2.0});
    await _call(control, 'zoom', {'factor': 1.5});
    await _call(control, 'zoom', {'factor': 1.25});

    expect(backend.payloads, hasLength(1));
    expect(_scale(backend.payloads.single), closeTo(2.0, 1e-9));

    await tester.pump(const Duration(milliseconds: 50));
    expect(backend.payloads, hasLength(1));

    await tester.pump(const Duration(seconds: 2));
    expect(backend.payloads, hasLength(2));
    expect(_scale(backend.payloads.last), closeTo(3.75, 1e-9));
    expect(await _call(control, 'get_scale', {}), closeTo(3.75, 1e-9));

    await tester.pump(const Duration(seconds: 1));
    expect(backend.payloads, hasLength(2));
  });

  testWidgets(
      'an immediate notification cancels the pending trailing notification',
      (tester) async {
    final InteractiveViewerTransformGate gate =
        InteractiveViewerTransformGate();
    var now = 1000;
    var matrix = <double>[2];
    final List<List<double>> sent = <List<double>>[];
    void handle() {
      gate.onTransform(
        now: () => now,
        intervalMillis: 200,
        enabled: () => true,
        matrix: () => matrix,
        emit: () => sent.add(List<double>.from(matrix)),
      );
    }

    handle();
    now = 1050;
    matrix = <double>[2.2];
    handle();
    expect(sent, <List<double>>[
      <double>[2]
    ]);

    now = 1200;
    matrix = <double>[2.64];
    handle();
    await tester.pump(const Duration(milliseconds: 500));

    expect(sent, <List<double>>[
      <double>[2],
      <double>[2.64]
    ]);
    gate.dispose();
  });

  testWidgets('a trailing notification is skipped when the matrix is unchanged',
      (tester) async {
    final InteractiveViewerTransformGate gate =
        InteractiveViewerTransformGate();
    var now = 1000;
    var matrix = <double>[2];
    final List<List<double>> sent = <List<double>>[];
    void handle() {
      gate.onTransform(
        now: () => now,
        intervalMillis: 200,
        enabled: () => true,
        matrix: () => matrix,
        emit: () => sent.add(List<double>.from(matrix)),
      );
    }

    handle();
    now = 1050;
    matrix = <double>[4];
    handle();
    now = 1060;
    matrix = <double>[2];
    handle();
    await tester.pump(const Duration(milliseconds: 200));

    expect(sent, <List<double>>[
      <double>[2]
    ]);
    gate.dispose();
  });

  testWidgets('disposing drops a pending transform notification',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 200);

    await _call(control, 'zoom', {'factor': 2.0});
    await _call(control, 'zoom', {'factor': 1.5});
    expect(backend.payloads, hasLength(1));

    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pump(const Duration(milliseconds: 400));

    expect(tester.takeException(), isNull);
    expect(backend.payloads, hasLength(1));
  });

  testWidgets(
      'throttled zoom burst reports the scale still applied when it stops',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 1000);

    await _call(control, 'zoom', {'factor': 2.0});
    await _call(control, 'zoom', {'factor': 1.5});
    await _call(control, 'zoom', {'factor': 0.5});
    await _call(control, 'zoom', {'factor': 1.2});
    expect(backend.payloads, hasLength(1));
    expect(_scale(backend.payloads.single), closeTo(2.0, 1e-9));

    await _finishTransform(tester);

    final transform = await _call(control, 'get_transform', {});
    expect(transform['s'], closeTo(1.8, 1e-9));
    expect(backend.payloads, hasLength(2));
    _expectLastMatches(backend.payloads.last, transform);
  });

  testWidgets('a wheel burst reports the scale still applied when it stops',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 1000);
    final Offset center = tester.getCenter(find.byType(InteractiveViewer));

    for (int i = 0; i < 4; i++) {
      await tester.sendEventToBinding(PointerScrollEvent(
        position: center,
        scrollDelta: const Offset(0, -40),
      ));
      await tester.pump();
    }
    expect(_scale(backend.payloads.first), greaterThan(1.0));

    await _finishTransform(tester);

    final transform = await _call(control, 'get_transform', {});
    expect(transform['s'], greaterThan(_scale(backend.payloads.first)));
    _expectLastMatches(backend.payloads.last, transform);
  });

  testWidgets('an inertial pan reports the translation still applied',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 1000);

    await tester.fling(
        find.byType(InteractiveViewer), const Offset(-120, -40), 2000);
    await _finishTransform(tester);

    final transform = await _call(control, 'get_transform', {});
    expect((transform['tx'] as num).abs() + (transform['ty'] as num).abs(),
        greaterThan(1.0));
    expect(backend.payloads, isNotEmpty);
    _expectLastMatches(backend.payloads.last, transform);
  });

  testWidgets('an animated reset reports the identity transform it ends on',
      (tester) async {
    final backend = _TransformEvents();
    final control = await _pumpViewer(tester, backend, interval: 1000);

    await _call(control, 'zoom', {'factor': 2.0});
    await _call(control, 'reset', {'animation_duration': 300});
    await _finishTransform(tester);

    final transform = await _call(control, 'get_transform', {});
    expect(transform['s'], closeTo(1.0, 1e-9));
    expect(transform['tx'], closeTo(0.0, 1e-6));
    expect(transform['ty'], closeTo(0.0, 1e-6));
    _expectLastMatches(backend.payloads.last, transform);
  });
}
