@TestOn('browser')
library;

import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'package:flet_notifications/src/notifications.dart';
import 'package:flutter/services.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences_platform_interface/in_memory_shared_preferences_async.dart';
import 'package:shared_preferences_platform_interface/shared_preferences_async_platform_interface.dart';

import 'fakes.dart' show invoke, makeService;

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
    // The browser plugin fails to initialize without notification support.
    return fln.WebFlutterLocalNotificationsPlugin.isSupported
        ? initializationResult
        : false;
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
    NotificationsService.resetForTesting();
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
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
        await invoke(makeService(), 'are_notifications_enabled'),
        permission == 'granted',
      );
      expect(requests, 0);
    });
  }

  test('granted permission is not requested again', () async {
    notification['permission'] = 'granted'.toJS;
    expect(await invoke(makeService(), 'request_permissions'), isTrue);
    expect(requests, 0);
  });

  test('missing browser Notification API reports false without throwing',
      () async {
    _global.delete('Notification'.toJS);
    final service = makeService();
    expect(await invoke(service, 'are_notifications_enabled'), isFalse);
    expect(await invoke(service, 'request_permissions'), isFalse);
    expect(await invoke(service, 'show', {'id': 1}),
        startsWith('unsupported_platform: '));
    expect(requests, 0);
  });

  test('a backend that cannot initialize reports false and retries later',
      () async {
    // As when the service worker can't register, as in private windows.
    final plugin = _WebPlugin()..initializationResult = false;
    fln.FlutterLocalNotificationsPlatform.instance = plugin;
    final service = makeService();
    expect(await invoke(service, 'are_notifications_enabled'), isFalse);
    expect(await invoke(service, 'request_permissions'), isFalse);
    expect(await invoke(service, 'show', {'id': 1}),
        'unsupported_platform: this browser can\'t show notifications');
    expect(requests, 0);
    expect(plugin.shown, isEmpty);

    plugin.initializationResult = true;
    expect(await invoke(service, 'show', {'id': 1}), null);
    expect(plugin.shown, hasLength(1));
  });

  test('show forwards all browser presentation options', () async {
    final service = makeService();
    final result = await invoke(service, 'show', {
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
          'silent': true,
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
}
