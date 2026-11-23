import 'package:flet/src/controls/control_widget.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/flet_core_extension.dart';
import 'package:flet/src/models/control.dart';
import 'package:flet/src/utils/app_driver.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:provider/provider.dart';

/// Records the events controls send to Python.
class _EventBackend extends FletBackend {
  _EventBackend()
      : super(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [FletCoreExtension()],
            multiView: false);

  final events = <(int, String, dynamic)>[];

  @override
  void triggerControlEvent(Control control, String eventName, [dynamic data]) {
    events.add((control.id, eventName, data));
  }
}

final _appKey = GlobalKey();

/// Shows [control] as the whole app, optionally with [overlay] on top.
Future<_EventBackend> _pump(WidgetTester tester, Map<String, dynamic> control,
    {Widget? overlay}) async {
  final backend = _EventBackend();
  final c = Control.fromMap(control, backend);
  await tester.pumpWidget(ChangeNotifierProvider<FletBackend>.value(
      value: backend,
      child: MaterialApp(
          home: Scaffold(
              body: KeyedSubtree(
                  key: _appKey,
                  child: Stack(children: [
                    Positioned.fill(child: ControlWidget(control: c)),
                    if (overlay != null) Positioned.fill(child: overlay),
                  ]))))));
  return backend;
}

AppDriver _driver() => AppDriver(_appKey.currentContext as Element);

/// Runs [future] while pumping frames, as `act` waits for frames and delays.
Future<T> _run<T>(WidgetTester tester, Future<T> future) async {
  T? result;
  var done = false;
  future.then((v) {
    result = v;
    done = true;
  });
  for (var i = 0; i < 100 && !done; i++) {
    await tester.pump(const Duration(milliseconds: 20));
  }
  expect(done, isTrue, reason: "act() didn't finish");
  return result as T;
}

Map<String, dynamic> _form() => {
      '_c': 'Column',
      '_i': 1,
      'controls': [
        {'_c': 'Text', '_i': 2, 'value': 'Count: 0'},
        {
          '_c': 'FilledButton',
          '_i': 3,
          'content': 'Add',
          'on_click': true,
        },
        {
          '_c': 'TextField',
          '_i': 4,
          'key': 'name',
          'label': 'Name',
          'on_change': true,
          'on_submit': true,
        },
        {
          '_c': 'TextField',
          '_i': 5,
          'label': 'Password',
          'password': true,
          'value': 'secret',
        },
        {
          '_c': 'FilledButton',
          '_i': 6,
          'content': 'Off',
          'disabled': true,
          'on_click': true,
        },
      ],
    };

void main() {
  testWidgets('describe lists what is on screen, not layout', (tester) async {
    await _pump(tester, _form());
    final result = _driver().describe();
    final controls = result['controls'] as List;
    final byId = {for (final c in controls) c['id']: c};

    expect(byId.containsKey(1), isFalse, reason: 'a Column is layout');
    expect(byId[2]['text'], 'Count: 0');
    expect(byId[3]['type'], 'FilledButton');
    expect(byId[3]['text'], 'Add');
    expect(byId[3]['events'], ['click']);
    expect(byId[4]['key'], 'name');
    expect(byId[4]['text'], 'Name');
    expect(byId[5].containsKey('value'), isFalse, reason: 'never a password');
    expect(byId[6]['disabled'], isTrue);
    // The button's label isn't listed again as a separate label.
    expect(controls.where((c) => c['text'] == 'Add'), hasLength(1));
    final rect = byId[3]['rect'] as List;
    expect(rect[2], greaterThan(0));
    expect(result['truncated'], isFalse);
  });

  testWidgets('tap by text fires on_click', (tester) async {
    final backend = await _pump(tester, _form());
    final result = await _run(
        tester,
        _driver().act([
          {
            'action': 'tap',
            'target': {'text': 'Add'}
          }
        ]));
    final step = (result['steps'] as List).single;
    expect(step['status'], 'ok');
    expect(step['target']['id'], 3);
    expect(backend.events.map((e) => (e.$1, e.$2)), contains((3, 'click')));
  });

  testWidgets('enter_text fires on_change, submit fires on_submit',
      (tester) async {
    final backend = await _pump(tester, _form());
    final result = await _run(
        tester,
        _driver().act([
          {
            'action': 'enter_text',
            'target': {'key': 'name'},
            'text': 'Ada',
            'submit': true,
          }
        ]));
    expect((result['steps'] as List).single['status'], 'ok');
    expect(backend.events, contains((4, 'change', 'Ada')));
    expect(backend.events.map((e) => (e.$1, e.$2)), contains((4, 'submit')));
  });

  testWidgets('a disabled or missing target fails and stops the steps',
      (tester) async {
    final backend = await _pump(tester, _form());
    final result = await _run(
        tester,
        _driver().act([
          {
            'action': 'tap',
            'target': {'text': 'Off'}
          },
          {
            'action': 'tap',
            'target': {'text': 'Add'}
          },
        ]));
    final steps = result['steps'] as List;
    expect(steps, hasLength(1));
    expect(steps.single['status'], 'disabled');
    expect(backend.events, isEmpty);

    final missing = await _run(
        tester,
        _driver().act([
          {
            'action': 'tap',
            'target': {'text': 'Count: 99'}
          }
        ]));
    final step = (missing['steps'] as List).single;
    expect(step['status'], 'not_found');
    expect((step['candidates'] as List).first['text'], 'Count: 0');
  });

  testWidgets('a control under something else is covered, not tapped',
      (tester) async {
    final backend = await _pump(tester, _form(),
        overlay: const ModalBarrier(color: Color(0x80000000)));
    final described = _driver().describe()['controls'] as List;
    expect(described.firstWhere((c) => c['id'] == 3)['covered'], isTrue);

    final result = await _run(
        tester,
        _driver().act([
          {
            'action': 'tap',
            'target': {'id': 3}
          }
        ]));
    expect((result['steps'] as List).single['status'], 'covered');
    expect(backend.events, isEmpty);
  });

  testWidgets('tap_at taps a point in app pixels', (tester) async {
    final backend = await _pump(tester, _form());
    final button = (_driver().describe()['controls'] as List)
        .firstWhere((c) => c['id'] == 3);
    final r = button['rect'] as List;
    final result = await _run(
        tester,
        _driver().act([
          {'action': 'tap_at', 'x': r[0] + r[2] / 2, 'y': r[1] + r[3] / 2},
          {'action': 'tap_at', 'x': -5, 'y': 10},
        ], pointer: 'mouse'));
    final steps = result['steps'] as List;
    expect(steps.first['status'], 'ok');
    expect(steps.last['status'], 'error');
    expect(backend.events.map((e) => (e.$1, e.$2)), contains((3, 'click')));
  });

  testWidgets('text drawn without its own control is listed as a label',
      (tester) async {
    await _pump(tester, {
      '_c': 'ListTile',
      '_i': 1,
      'title': 'Groceries',
      'subtitle': 'Nov 21',
      'on_click': true,
    });
    final controls = _driver().describe()['controls'] as List;
    expect(controls.first['type'], 'ListTile');
    expect(controls.first['text'], 'Groceries');
    final label = controls.firstWhere((c) => c['text'] == 'Nov 21');
    expect(label['type'], 'label');
    expect(label['in'], 1);
    expect(controls.where((c) => c['text'] == 'Groceries'), hasLength(1));
  });

  testWidgets('icons and labels repeated by an inner Text are left out',
      (tester) async {
    await _pump(tester, {
      '_c': 'Column',
      '_i': 1,
      'controls': [
        {
          '_c': 'IconButton',
          '_i': 2,
          'icon': 65604, // ft.Icons.ADD
          'tooltip': 'Increment',
          'on_click': true,
        },
        {
          '_c': 'ListTile',
          '_i': 3,
          'title': {'_c': 'Text', '_i': 4, 'value': 'Row 0'},
          'on_click': true,
        },
      ],
    });
    final controls = _driver().describe()['controls'] as List;
    expect(controls.map((c) => c['id']), [2, 3]);
    expect(controls.last['text'], 'Row 0');
  });
}
