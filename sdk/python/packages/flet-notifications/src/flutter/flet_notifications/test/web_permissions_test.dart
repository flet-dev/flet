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
}
