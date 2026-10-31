import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flet/src/controls/bottom_app_bar.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

const int _width = 800;
const int _height = 600;

/// Pixels skipped at each end of the bar when looking for the notch, so
/// rounded corners don't count as part of it.
const int _cornerInset = 24;

final FletBackend _backend = FletBackend(
    pageUri: Uri.parse('http://localhost'),
    assetsDir: '',
    extensions: [FletCoreExtension()],
    multiView: false);

Control _bar(Map<String, dynamic> props) => Control(
    id: 2,
    type: 'BottomAppBar',
    properties: {
      'bgcolor': '#ff0000',
      'elevation': 0,
      'shape': {'_type': 'circular'},
      ...props,
    },
    backend: _backend);

Map<String, int> _margin({int left = 0, int top = 0, int right = 0}) =>
    {'left': left, 'top': top, 'right': right, 'bottom': 0};

final FloatingActionButton _fab = FloatingActionButton(
    onPressed: () {},
    backgroundColor: const Color(0x00000000),
    elevation: 0,
    highlightElevation: 0,
    focusElevation: 0,
    hoverElevation: 0);

/// Places the floating action button's top-left corner at [offset].
class _FixedFabLocation extends FloatingActionButtonLocation {
  const _FixedFabLocation(this.offset);

  final Offset offset;

  @override
  Offset getOffset(ScaffoldPrelayoutGeometry scaffoldGeometry) => offset;
}

final GlobalKey _boundaryKey = GlobalKey();

Widget _app(Widget scaffold, {ThemeData? theme}) => RepaintBoundary(
    key: _boundaryKey,
    child: ChangeNotifierProvider<FletBackend>.value(
        value: _backend, child: MaterialApp(theme: theme, home: scaffold)));

Widget _slotScaffold(Control bar) => Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      floatingActionButton: _fab,
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      bottomNavigationBar: BottomAppBarControl(control: bar),
    );

Future<void> _setSurfaceSize(WidgetTester tester) async {
  await tester.binding
      .setSurfaceSize(Size(_width.toDouble(), _height.toDouble()));
  addTearDown(() => tester.binding.setSurfaceSize(null));
}

bool _isBar(ByteData data, int x, int y) {
  final i = (y * _width + x) * 4;
  return data.getUint8(i) > 200 && data.getUint8(i + 1) < 60;
}

/// Measures the notch: its center's horizontal distance from the floating
/// action button's center, and its depth below the bar's top at that center.
Future<(double, int)> _measureNotch(WidgetTester tester) async {
  final barRect = tester.getRect(find.byType(BottomAppBar));
  final boundary =
      _boundaryKey.currentContext!.findRenderObject() as RenderRepaintBoundary;
  final data = (await tester.runAsync(() async {
    final image = await boundary.toImage();
    return image.toByteData(format: ui.ImageByteFormat.rawRgba);
  }))!;
  final y = barRect.top.round() + 3;
  final notch = <int>[
    for (var x = barRect.left.round() + _cornerInset;
        x < barRect.right.round() - _cornerInset;
        x++)
      if (!_isBar(data, x, y)) x,
  ];
  final fabX = tester.getCenter(find.byType(FloatingActionButton)).dx.round();
  var depth = 0;
  for (var yy = barRect.top.round(); yy < barRect.bottom.round(); yy++) {
    if (_isBar(data, fabX, yy)) break;
    depth++;
  }
  expect(notch, isNotEmpty, reason: 'the bar has no notch');
  return ((notch.first + notch.last + 1) / 2 - fabX, depth);
}

/// Pumps the bar from [from] to [to] with a 2 second margin animation and
/// returns the largest notch offset seen during and after the animation.
Future<double> _worstOffsetWhileAnimating(WidgetTester tester,
    Map<String, dynamic> from, Map<String, dynamic> to) async {
  await tester
      .pumpWidget(_app(_slotScaffold(_bar({'animate_margin': 2000, ...from}))));
  await tester.pumpAndSettle();
  await tester
      .pumpWidget(_app(_slotScaffold(_bar({'animate_margin': 2000, ...to}))));
  var worst = 0.0;
  for (final ms in [0, 500, 500, 1000]) {
    await tester.pump(Duration(milliseconds: ms));
    final (dx, _) = await _measureNotch(tester);
    if (dx.abs() > worst) worst = dx.abs();
  }
  await tester.pumpAndSettle();
  final (dx, _) = await _measureNotch(tester);
  return dx.abs() > worst ? dx.abs() : worst;
}

void main() {
  group('BottomAppBar notch with a margin in the bottom slot', () {
    for (final margin in [
      null,
      _margin(left: 40, right: 40),
      _margin(top: 16),
      _margin(left: 80),
    ]) {
      testWidgets('stays under the button with margin $margin', (tester) async {
        await _setSurfaceSize(tester);
        await tester.pumpWidget(_app(_slotScaffold(_bar({
          if (margin != null) 'margin': margin,
        }))));
        await tester.pumpAndSettle();
        final (dx, depth) = await _measureNotch(tester);
        // The docked button's center is on the slot's top edge, so a top
        // margin makes the notch shallower by the same amount.
        final top = margin?['top'] ?? 0;
        expect(dx.abs(), lessThan(1.5));
        expect(depth, inInclusiveRange(31 - top, 33 - top));
      });
    }
  });

  testWidgets('BottomAppBar notch follows an animated margin', (tester) async {
    await _setSurfaceSize(tester);
    final worst = await _worstOffsetWhileAnimating(
        tester, {'margin': _margin(right: 80)}, {'margin': _margin(left: 80)});
    expect(worst, lessThan(1.5));
  });

  testWidgets(
      'BottomAppBar notch follows an animated margin when border_radius '
      'changes at the same time', (tester) async {
    await _setSurfaceSize(tester);
    final worst = await _worstOffsetWhileAnimating(
        tester,
        {'margin': _margin(right: 80)},
        {'margin': _margin(left: 80), 'border_radius': 16});
    expect(worst, lessThan(1.5));
  });

  testWidgets('BottomAppBar notch keeps its depth in the page body',
      (tester) async {
    await _setSurfaceSize(tester);
    // A 16 px top margin, then an 80 px bar whose top is at y=520, where the
    // button's center sits.
    await tester.pumpWidget(_app(Scaffold(
      backgroundColor: const Color(0xFFFFFFFF),
      floatingActionButton: _fab,
      floatingActionButtonLocation: const _FixedFabLocation(Offset(372, 492)),
      body: Align(
        alignment: Alignment.bottomCenter,
        child: SizedBox(
          width: _width.toDouble(),
          child: BottomAppBarControl(
              control: _bar({'height': 80, 'margin': _margin(top: 16)})),
        ),
      ),
    )));
    await tester.pumpAndSettle();
    final (dx, depth) = await _measureNotch(tester);
    expect(dx.abs(), lessThan(1.5));
    expect(depth, inInclusiveRange(31, 33));
  });

  testWidgets('BottomAppBar notch shape from the theme follows the margin',
      (tester) async {
    await _setSurfaceSize(tester);
    await tester.pumpWidget(_app(
        _slotScaffold(_bar({
          'shape': null,
          'margin': _margin(left: 40, right: 40),
        })),
        theme: ThemeData(
            bottomAppBarTheme: const BottomAppBarThemeData(
                shape: CircularNotchedRectangle()))));
    await tester.pumpAndSettle();
    final (dx, _) = await _measureNotch(tester);
    expect(dx.abs(), lessThan(1.5));
  });

  testWidgets('BottomAppBar notch ignores a margin in skip_properties',
      (tester) async {
    await _setSurfaceSize(tester);
    await tester.pumpWidget(_app(_slotScaffold(_bar({
      'margin': _margin(left: 80),
      '_internals': {
        'skip_properties': ['margin'],
      },
    }))));
    await tester.pumpAndSettle();
    final (dx, _) = await _measureNotch(tester);
    expect(dx.abs(), lessThan(1.5));
  });
}
