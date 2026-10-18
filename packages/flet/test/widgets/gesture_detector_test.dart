import 'package:flet/src/controls/gesture_detector.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';

class _EventBackend extends FletBackend {
  _EventBackend()
      : super(
          pageUri: Uri.parse('http://localhost'),
          assetsDir: '',
          extensions: [],
          multiView: false,
        );

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
  final parent = Control(
    id: 1,
    type: 'Column',
    properties: {},
    backend: backend,
  );
  final control = Control(
    id: 2,
    type: 'GestureDetector',
    parent: parent,
    properties: properties,
    backend: backend,
  );
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
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: _buildDetector(
            backend,
            properties: {'on_tap': true, 'on_tap_move': true},
          ),
        ),
      ),
    );

    final gesture = await _pressAndMove(
      tester,
      moves: const [Offset(5, 3), Offset(3, 2)],
    );
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
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: _buildDetector(backend, properties: {'on_tap_move': true}),
        ),
      ),
    );

    final gesture = await _pressAndMove(tester, moves: const [Offset(7, 4)]);
    await gesture.up();
    await tester.pump();

    expect(backend.events, ['tap_move']);
    expect(tester.takeException(), isNull);
  });

  testWidgets('on_tap_cancel still fires when the pointer moves beyond slop', (
    tester,
  ) async {
    final backend = _EventBackend();
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: _buildDetector(
            backend,
            properties: {
              'on_tap': true,
              'on_tap_move': true,
              'on_tap_cancel': true,
            },
          ),
        ),
      ),
    );

    final gesture = await _pressAndMove(
      tester,
      moves: const [Offset(60, 0), Offset(20, 0)],
    );
    await gesture.up();
    await tester.pump();

    expect(backend.events, isNot(contains('tap_move')));
    expect(backend.events, isNot(contains('tap')));
    expect(backend.events, contains('tap_cancel'));
    expect(tester.takeException(), isNull);
  });

  testWidgets('on_tap still fires without on_tap_move', (tester) async {
    final backend = _EventBackend();
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: _buildDetector(backend, properties: {'on_tap': true}),
        ),
      ),
    );

    final gesture = await _pressAndMove(tester, moves: const [Offset(5, 3)]);
    await gesture.up();
    await tester.pump();

    expect(backend.events, ['tap']);
    expect(tester.takeException(), isNull);
  });
  testWidgets('allowed_devices changes apply to the reused tap recognizer', (
    tester,
  ) async {
    final backend = _EventBackend();
    Future<void> build(List<String> devices) => tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: _buildDetector(
                backend,
                properties: {
                  'on_tap': true,
                  'on_tap_move': true,
                  'allowed_devices': devices,
                },
              ),
            ),
          ),
        );
    await build(['touch']);
    await tester.tap(find.byType(GestureDetectorControl));
    await tester.pump();
    expect(backend.events, ['tap']);
    backend.events.clear();
    await build(['mouse']);
    await tester.tap(find.byType(GestureDetectorControl));
    await tester.pump();
    expect(backend.events, isEmpty, reason: 'touch should now be excluded');
    final mouse = await tester.startGesture(
      tester.getCenter(find.byType(GestureDetectorControl)),
      kind: PointerDeviceKind.mouse,
    );
    await mouse.up();
    await tester.pump();
    expect(backend.events, ['tap']);
  });

  for (final move in [false, true]) {
    for (final buttonHandler in [
      null,
      'on_secondary_tap',
      'on_tertiary_tap_up',
    ]) {
      testWidgets('semantic tap move=$move buttonHandler=$buttonHandler', (
        tester,
      ) async {
        final semantics = tester.ensureSemantics();
        final backend = _EventBackend();
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: _buildDetector(
                backend,
                properties: {
                  'on_tap': true,
                  'on_tap_move': move,
                  if (buttonHandler != null) buttonHandler: true,
                },
              ),
            ),
          ),
        );
        final tapNodes = tester.semantics
            .simulatedAccessibilityTraversal()
            .where((node) =>
                node.getSemanticsData().hasAction(SemanticsAction.tap))
            .toList();
        try {
          tapNodes.first.owner!
              .performAction(tapNodes.first.id, SemanticsAction.tap);
          await tester.pump();
        } finally {
          semantics.dispose();
        }
        expect(backend.events, ['tap']);
        expect(tapNodes, hasLength(1));
      });
    }
  }

  testWidgets('double taps still win against the tap-move recognizer', (
    tester,
  ) async {
    final backend = _EventBackend();
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: _buildDetector(
            backend,
            properties: {
              'on_tap': true,
              'on_tap_move': true,
              'on_double_tap': true,
            },
          ),
        ),
      ),
    );
    await tester.tap(find.byType(GestureDetectorControl));
    await tester.pump(const Duration(milliseconds: 50));
    await tester.tap(find.byType(GestureDetectorControl));
    await tester.pumpAndSettle();
    expect(backend.events, ['double_tap']);
  });

  testWidgets('long presses still win against the tap-move recognizer', (
    tester,
  ) async {
    final backend = _EventBackend();
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: _buildDetector(
            backend,
            properties: {
              'on_tap': true,
              'on_tap_move': true,
              'on_long_press': true,
            },
          ),
        ),
      ),
    );
    await tester.longPress(find.byType(GestureDetectorControl));
    await tester.pumpAndSettle();
    expect(backend.events, ['long_press']);
  });
  for (final move in [false, true]) {
    for (final secondary in [false, true]) {
      for (final cancel in [false, true]) {
        testWidgets(
          'mouse tap move=$move secondary=$secondary cancel=$cancel',
          (tester) async {
            final backend = _EventBackend();
            final prefix = secondary ? 'secondary_tap' : 'tertiary_tap';
            await tester.pumpWidget(
              MaterialApp(
                home: Scaffold(
                  body: _buildDetector(
                    backend,
                    properties: {
                      'on_tap_move': move,
                      if (secondary) 'on_secondary_tap': true,
                      'on_${prefix}_down': true,
                      'on_${prefix}_up': true,
                      'on_${prefix}_cancel': true,
                    },
                  ),
                ),
              ),
            );
            final gesture = await tester.startGesture(
              tester.getCenter(find.byType(GestureDetectorControl)),
              kind: PointerDeviceKind.mouse,
              buttons: secondary ? kSecondaryButton : kTertiaryButton,
            );
            await tester.pump(const Duration(milliseconds: 150));
            await gesture.moveBy(Offset(cancel ? 60 : 1, 0));
            await gesture.up();
            await tester.pump();
            expect(backend.events, [
              '${prefix}_down',
              if (cancel) '${prefix}_cancel' else '${prefix}_up',
              if (!cancel && secondary) 'secondary_tap',
            ]);
          },
        );
      }
    }
  }
}
