@TestOn('browser')
library;

import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'package:flet/flet.dart';
import 'package:flet_notifications/src/notifications_service.dart';
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
  }) async =>
      true;
}

LocalNotificationsService _service() => LocalNotificationsService(
      control: Control(
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
        await _service().invokeMethod('are_notifications_enabled'),
        permission == 'granted' ? 'true' : 'false',
      );
      expect(requests, 0);
    });
  }

  for (final result in ['granted', 'denied', 'default']) {
    test('request returns the browser result $result', () async {
      requestResult = result;
      final service = _service();
      expect(await service.invokeMethod('are_notifications_enabled'), 'false');
      expect(
        await service.invokeMethod('request_permissions'),
        result == 'granted' ? 'true' : 'false',
      );
      expect(requests, 1);
      expect(
        await service.invokeMethod('are_notifications_enabled'),
        result == 'granted' ? 'true' : 'false',
      );
    });
  }

  for (final permission in ['granted', 'denied']) {
    test('existing $permission does not request permission again', () async {
      notification['permission'] = permission.toJS;
      expect(
        await _service().invokeMethod('request_permissions'),
        permission == 'granted' ? 'true' : 'false',
      );
      expect(requests, 0);
    });
  }

  test('missing browser Notification API reports false without throwing',
      () async {
    _global.delete('Notification'.toJS);
    final service = _service();
    expect(await service.invokeMethod('are_notifications_enabled'), 'false');
    expect(await service.invokeMethod('request_permissions'), 'false');
    expect(requests, 0);
  });

  test('show forwards all browser presentation options', () async {
    final service = _service();
    final result = await service.invokeMethod('show', {
      'id': 7,
      'title': 'A message',
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
          'timestamp': 1700000000123,
        },
      },
    });
    expect(result, 'ok');
    final plugin = fln.FlutterLocalNotificationsPlatform.instance as _WebPlugin;
    final details = plugin.shown.single;
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
    expect(await service.invokeMethod('show', {'id': 7}), 'ok');
    final defaults = plugin.shown.single;
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
          await service.invokeMethod('show', {
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
          'ok');
      final details = plugin.shown.last;
      expect(details.direction, fln.WebNotificationDirection.leftToRight);
      expect(details.requireInteraction, enabled);
      expect(details.isSilent, enabled);
      expect(details.renotify, enabled);
    }
  });
}
