@TestOn('browser')
library;

import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'package:flet/flet.dart';
import 'package:flet_notifications/src/notifications_service.dart';
import 'package:flet_notifications/src/utils/errors.dart';
import 'package:flutter/services.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

@JS('globalThis')
external JSObject get _global;

// Avoid service-worker registration while retaining the upstream permission API.
class _WebPlugin extends fln.WebFlutterLocalNotificationsPlugin {
  final List<fln.WebNotificationDetails> shown = [];
  bool? initializationResult = true;
  int initializations = 0;
  fln.DidReceiveNotificationResponseCallback? onResponse;

  @override
  Future<void> show({
    required int id,
    String? title,
    String? body,
    String? payload,
    fln.WebNotificationDetails? notificationDetails,
  }) async {
    shown.add(notificationDetails!);
  }

  @override
  Future<bool?> initialize({
    fln.DidReceiveNotificationResponseCallback?
        onDidReceiveNotificationResponse,
  }) async {
    initializations++;
    onResponse = onDidReceiveNotificationResponse;
    return initializationResult;
  }
}

class _RecordingControl extends Control {
  final List<Map<String, Object?>> events = [];

  _RecordingControl()
      : super(
          id: 1,
          type: 'LocalNotifications',
          properties: const {},
          backend: FletBackend(
            pageUri: Uri.parse('http://localhost'),
            assetsDir: '',
            extensions: [],
            multiView: false,
          ),
        );

  @override
  void triggerEvent(String eventName, [dynamic data]) {
    events.add({'name': eventName, 'data': data});
  }
}

LocalNotificationsService _service({Control? control}) =>
    LocalNotificationsService(
      control: control ??
          Control(
            id: 1,
            type: 'LocalNotifications',
            properties: const {},
            backend: FletBackend(
              pageUri: Uri.parse('http://localhost'),
              assetsDir: '',
              extensions: [],
              multiView: false,
            ),
          ),
    );

/// Invokes [method] and returns its result, or for a failure the text Flet
/// reports to Python: the [NotificationException]'s `"<code>: <message>"`.
Future<Object?> _call(LocalNotificationsService service, String method,
    [Object? args]) async {
  try {
    return await service.invokeMethod(method, args);
  } on NotificationException catch (e) {
    return e.toString();
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late JSAny? originalNotification;
  late JSObject notification;
  late String status;
  late String requestResult;
  late int requests;

  setUp(() {
    SharedPreferences.setMockInitialValues({});
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('flutter_timezone'),
      (_) async => 'UTC',
    );
    originalNotification = _global['Notification'];
    notification = JSObject();
    status = 'default';
    requestResult = 'granted';
    requests = 0;
    notification['permission'] = status.toJS;
    notification['requestPermission'] = (() {
      requests++;
      status = requestResult;
      notification['permission'] = status.toJS;
      return Future<JSString>.value(status.toJS).toJS;
    }).toJS;
    _global['Notification'] = notification;
    fln.FlutterLocalNotificationsPlatform.instance = _WebPlugin();
  });

  tearDown(() {
    _global['Notification'] = originalNotification;
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
            const MethodChannel('flutter_timezone'), null);
  });

  for (final permission in ['granted', 'denied', 'default']) {
    test('status reports $permission without prompting', () async {
      notification['permission'] = permission.toJS;
      expect(
        await _call(_service(), 'are_notifications_enabled'),
        permission == 'granted',
      );
      expect(requests, 0);
    });
  }

  for (final result in [false, null]) {
    test('web initialization result $result blocks showing and permits retry',
        () async {
      final plugin = _WebPlugin()..initializationResult = result;
      fln.FlutterLocalNotificationsPlatform.instance = plugin;
      final service = _service();
      expect(await _call(service, 'show', {'id': 1}),
          startsWith('initialization_failed: '));
      expect(plugin.shown, isEmpty);
      plugin.initializationResult = true;
      expect(await _call(service, 'show', {'id': 1}), null);
      expect(plugin.initializations, 2);
      expect(
          await _call(service, 'show', {
            'id': 2,
            'actions': [
              {'id': 'open', 'title': 'Open'}
            ],
          }),
          null);
      expect(plugin.initializations, 2);
    });
  }

  for (final result in ['granted', 'denied', 'default']) {
    test('request returns the browser result $result', () async {
      requestResult = result;
      final service = _service();
      expect(await _call(service, 'are_notifications_enabled'), isFalse);
      expect(
        await _call(service, 'request_permissions'),
        result == 'granted',
      );
      expect(requests, 1);
      expect(
        await _call(service, 'are_notifications_enabled'),
        result == 'granted',
      );
    });
  }

  for (final permission in ['granted', 'denied']) {
    test('existing $permission does not request permission again', () async {
      notification['permission'] = permission.toJS;
      expect(
        await _call(_service(), 'request_permissions'),
        permission == 'granted',
      );
      expect(requests, 0);
    });
  }

  test('missing browser Notification API reports false without throwing',
      () async {
    _global.delete('Notification'.toJS);
    final service = _service();
    expect(await _call(service, 'are_notifications_enabled'), isFalse);
    expect(await _call(service, 'request_permissions'), isFalse);
    expect(requests, 0);
  });

  test('show forwards all browser presentation options', () async {
    final service = _service();
    final result = await _call(service, 'show', {
      'id': 7,
      'title': 'A message',
      'actions': [
        {'id': 'open', 'title': 'Open'},
        {'id': 'archive', 'title': 'Archive', 'foreground': false},
      ],
      'options': {
        'web': {
          'direction': 'rightToLeft',
          'badge_url': 'https://example.com/badge.png',
          'icon_url': '/assets/icon.png',
          'image_url': 'https://example.com/photo.png',
          'lang': 'ar',
          'require_interaction': true,
          'is_silent': true,
          'renotify': true,
          'timestamp': DateTime.utc(2023, 11, 14, 22, 13, 20, 123),
        },
      },
    });
    expect(result, null);
    final plugin = fln.FlutterLocalNotificationsPlatform.instance as _WebPlugin;
    final details = plugin.shown.single;
    expect(details.actions.map((a) => a.action), ['open', 'archive']);
    expect(details.actions.map((a) => a.title), ['Open', 'Archive']);
    expect(details.direction, fln.WebNotificationDirection.rightToLeft);
    expect(details.badgeUrl, Uri.parse('https://example.com/badge.png'));
    expect(details.iconUrl, Uri.parse('/assets/icon.png'));
    expect(details.imageUrl, Uri.parse('https://example.com/photo.png'));
    expect(details.lang, 'ar');
    expect(details.requireInteraction, isTrue);
    expect(details.isSilent, isTrue);
    expect(details.renotify, isTrue);
    expect(details.timestamp!.millisecondsSinceEpoch, 1700000000123);
  });

  test(
      'omitted web options use upstream defaults and explicit false is honored',
      () async {
    final service = _service();
    final plugin = fln.FlutterLocalNotificationsPlatform.instance as _WebPlugin;
    expect(await _call(service, 'show', {'id': 7}), null);
    final defaults = plugin.shown.single;
    expect(defaults.actions, isEmpty);
    expect(defaults.direction, fln.WebNotificationDirection.auto);
    expect(defaults.badgeUrl, isNull);
    expect(defaults.iconUrl, isNull);
    expect(defaults.imageUrl, isNull);
    expect(defaults.lang, isNull);
    expect(defaults.timestamp, isNull);
    expect(defaults.requireInteraction, isFalse);
    expect(defaults.isSilent, isFalse);
    expect(defaults.renotify, isFalse);

    for (final enabled in [true, false]) {
      expect(
          await _call(service, 'show', {
            'id': 7,
            'options': {
              'web': {
                'direction': 'leftToRight',
                'require_interaction': enabled,
                'is_silent': enabled,
                'renotify': enabled,
              },
            },
          }),
          null);
      final details = plugin.shown.last;
      expect(details.direction, fln.WebNotificationDirection.leftToRight);
      expect(details.requireInteraction, enabled);
      expect(details.isSilent, enabled);
      expect(details.renotify, enabled);
    }
  });
  for (final action in [true, false]) {
    test('browser callback emits ${action ? "action" : "tap"} with payload',
        () async {
      final control = _RecordingControl();
      final service = _service(control: control);
      expect(await _call(service, 'initialize'), null);
      final plugin =
          fln.FlutterLocalNotificationsPlatform.instance as _WebPlugin;
      plugin.onResponse!(fln.NotificationResponse(
        id: 7,
        actionId: action ? 'archive' : null,
        payload: 'message:42',
        notificationResponseType: action
            ? fln.NotificationResponseType.selectedNotificationAction
            : fln.NotificationResponseType.selectedNotification,
      ));
      final event = control.events.single;
      expect(event['name'], action ? 'action' : 'tap');
      final data = event['data'] as Map;
      expect(data['id'], 7);
      expect(data['action_id'], action ? 'archive' : '');
      expect(data['payload'], 'message:42');
      expect(data['response_type'], action ? 'action' : 'tap');
    });
  }
}
