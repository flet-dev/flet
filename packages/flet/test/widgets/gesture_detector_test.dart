import 'package:flet/src/controls/gesture_detector.dart';
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

GestureDetectorControl _buildDetector(
  _EventBackend backend, {
  required Map<String, dynamic> properties,
}) {
  final parent =
      Control(id: 1, type: 'Column', properties: {}, backend: backend);
  final control = Control(
      id: 2,
      type: 'GestureDetector',
      parent: parent,
      properties: properties,
      backend: backend);
  return GestureDetectorControl(control: control);
}

Future<TestGesture> _pressAndMove(
  WidgetTester tester, {
  required List<Offset> moves,
}) async {
  final center = tester.getCenter(find.byType(GestureDetectorControl));
  final gesture = await tester.startGesture(center);
  await tester.pump(const Duration(milliseconds: 50));
  for (final move in moves) {
    await gesture.moveBy(move);
    await tester.pump(const Duration(milliseconds: 50));
  }
  return gesture;
}

void main() {
  testWidgets('on_tap_move fires while on_tap keeps working', (tester) async {
    final backend = _EventBackend();
    await tester.pumpWidget(MaterialApp(
        home: Scaffold(
            body: _buildDetector(backend,
                properties: {'on_tap': true, 'on_tap_move': true}))));

    final gesture = await _pressAndMove(tester, moves: const [
      Offset(5, 3),
      Offset(3, 2),
    ]);
    await gesture.up();
    await tester.pump();

    // Regression test for https://github.com/flet-dev/flet/issues/6961:
    // Flutter's GestureDetector never forwards `onTapMove` to its
    // TapGestureRecognizer, so `tap_move` events were never sent to Python.
    expect(backend.events, contains('tap_move'));
    expect(backend.events.where((e) => e == 'tap_move'), hasLength(2));
    expect(backend.events, contains('tap'));
    expect(backend.events, isNot(contains('tap_cancel')));
    expect(tester.takeException(), isNull);
  });

  testWidgets('on_tap_move fires when it is the only handler', (tester) async {
    final backend = _EventBackend();
    await tester.pumpWidget(MaterialApp(
        home: Scaffold(
            body: _buildDetector(backend, properties: {'on_tap_move': true}))));

    final gesture = await _pressAndMove(tester, moves: const [Offset(7, 4)]);
    await gesture.up();
    await tester.pump();

    expect(backend.events, ['tap_move']);
    expect(tester.takeException(), isNull);
  });

  testWidgets('on_tap_cancel still fires when the pointer moves beyond slop',
      (tester) async {
    final backend = _EventBackend();
    await tester.pumpWidget(MaterialApp(
        home: Scaffold(
            body: _buildDetector(backend, properties: {
      'on_tap': true,
      'on_tap_move': true,
      'on_tap_cancel': true,
    }))));

    final gesture = await _pressAndMove(tester,
        moves: const [Offset(60, 0), Offset(20, 0)]);
    await gesture.up();
    await tester.pump();

    expect(backend.events, isNot(contains('tap_move')));
    expect(backend.events, isNot(contains('tap')));
    expect(backend.events, contains('tap_cancel'));
    expect(tester.takeException(), isNull);
  });

  testWidgets('on_tap still fires without on_tap_move', (tester) async {
    final backend = _EventBackend();
    await tester.pumpWidget(MaterialApp(
        home: Scaffold(
            body: _buildDetector(backend, properties: {'on_tap': true}))));

    final gesture = await _pressAndMove(tester, moves: const [Offset(5, 3)]);
    await gesture.up();
    await tester.pump();

    expect(backend.events, ['tap']);
    expect(tester.takeException(), isNull);
  });
}
