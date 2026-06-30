// ignore_for_file: depend_on_referenced_packages
// ignore_for_file: non_const_argument_for_const_parameter
import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:flet/flet.dart';
import 'flutter_test_finder.dart';
import 'flutter_tester.dart';
import 'frame_decoder.dart';

/// Drives [FlutterWidgetTester] over an independent length-prefixed JSON
/// protocol on a raw TCP socket — completely separate from Flet's own transport.
///
/// The on-device app under test runs normally (embedded Python over
/// dart_bridge); this socket connects out to the Python `RemoteTester` server
/// and is the only channel that drives the integration-test `WidgetTester`. No
/// `FletApp`/`FletBackend` is added to the widget tree, so the app settles
/// normally and `WidgetTester.pump`/`pumpAndSettle` behave as usual.
class RemoteWidgetTester extends FlutterWidgetTester {
  final Socket _socket;
  final Map<int, FlutterTestFinder> _finders = {};
  final Completer<void> _connectionClosed = Completer<void>();
  Future<void> _commandQueue = Future<void>.value();
  StreamSubscription<Uint8List>? _subscription;
  bool _teardownRequested = false;

  RemoteWidgetTester._(
    super.tester,
    super.binding,
    this._socket,
  ) {
    _startListening();
  }

  static Future<RemoteWidgetTester> connect({
    required WidgetTester tester,
    required IntegrationTestWidgetsFlutterBinding binding,
    required Uri serverUri,
    Duration timeout = const Duration(seconds: 10),
  }) async {
    if (!serverUri.hasPort) {
      throw ArgumentError("Server URL must include a port: $serverUri");
    }
    final host = serverUri.host.isEmpty ? "127.0.0.1" : serverUri.host;
    final port = serverUri.port;
    final socket = await Socket.connect(host, port, timeout: timeout);
    socket.setOption(SocketOption.tcpNoDelay, true);
    return RemoteWidgetTester._(tester, binding, socket);
  }

  void _startListening() {
    final stream = _socket.transform(const FrameDecoder());
    _subscription = stream.listen(null, onError: (error, stackTrace) {
      if (!_connectionClosed.isCompleted) {
        _connectionClosed.completeError(error, stackTrace);
      }
      _closeSilently();
    }, onDone: () {
      _closeSilently();
      if (!_connectionClosed.isCompleted) {
        _connectionClosed.complete();
      }
    }, cancelOnError: true);
    // Serialize commands by chaining them onto a single queue. Do NOT pause the
    // subscription while a command runs: pausing also stops the socket being
    // serviced for writes, so `_sendResponse`'s flush would deadlock (the
    // response only transmits when an unrelated incoming byte wakes the link).
    _subscription!.onData((frame) {
      _commandQueue = _commandQueue.then((_) => _processFrame(frame));
    });
  }

  Future<void> _processFrame(Uint8List frame) async {
    final dynamic decoded = jsonDecode(utf8.decode(frame));
    if (decoded is! Map<String, dynamic>) {
      throw Exception("Invalid command payload: $decoded");
    }
    final id = decoded["id"];
    final method = decoded["method"] as String?;
    final params = (decoded["params"] as Map<dynamic, dynamic>?)
            ?.cast<String, dynamic>() ??
        const <String, dynamic>{};

    if (id == null || method == null) {
      throw Exception("Command must include both 'id' and 'method'.");
    }

    try {
      final response = await _handleCommand(method, params);
      await _sendResponse(id, result: response.result);
      if (response.closeAfter) {
        await _socket.flush();
        await _socket.close();
        await _subscription?.cancel();
        if (!_connectionClosed.isCompleted) {
          _connectionClosed.complete();
        }
      }
    } catch (error, stackTrace) {
      await _sendResponse(id, error: "$error", stack: stackTrace.toString());
    }
  }

  _CommandResponse _ok([dynamic result]) =>
      _CommandResponse(result, closeAfter: false);

  Future<_CommandResponse> _handleCommand(
    String method,
    Map<String, dynamic> params,
  ) async {
    switch (method) {
      case "pump":
        await pump(duration: _parseDuration(params["duration"]));
        return _ok();
      case "pump_and_settle":
        await pumpAndSettle(duration: _parseDuration(params["duration"]));
        return _ok();
      case "find_by_text":
        return _ok(_storeFinder(findByText(params["text"] as String)));
      case "find_by_text_containing":
        return _ok(
          _storeFinder(findByTextContaining(params["pattern"] as String)),
        );
      case "find_by_key":
        return _ok(_storeFinder(findByKey(_parseKey(params["key"]))));
      case "find_by_tooltip":
        return _ok(_storeFinder(findByTooltip(params["value"] as String)));
      case "find_by_icon":
        return _ok(_storeFinder(findByIcon(_parseIcon(params["icon"]))));
      case "take_screenshot":
        final bytes = await takeScreenshot(params["name"] as String);
        return _ok(base64Encode(bytes));
      case "tap":
        await _withFinder(
            params, (finder, index) => tap(finder, index));
        return _ok();
      case "long_press":
        await _withFinder(
            params, (finder, index) => longPress(finder, index));
        return _ok();
      case "enter_text":
        await _withFinder(params,
            (finder, index) => enterText(finder, index, params["text"] as String));
        return _ok();
      case "mouse_hover":
        await _withFinder(
            params, (finder, index) => mouseHover(finder, index));
        return _ok();
      case "teardown":
        _triggerTeardown();
        return const _CommandResponse(null, closeAfter: true);
      default:
        throw Exception("Unknown Tester method: $method");
    }
  }

  Map<String, dynamic> _storeFinder(TestFinder finder) {
    final flutterFinder = finder as FlutterTestFinder;
    _finders[flutterFinder.id] = flutterFinder;
    return flutterFinder.toMap();
  }

  Future<void> _withFinder(
    Map<String, dynamic> params,
    Future<void> Function(FlutterTestFinder finder, int index) action,
  ) async {
    final id = params["finder_id"];
    final index = (params["finder_index"] as int?) ?? 0;
    final finder = _finders[id];
    if (finder == null) {
      throw Exception("Finder with id $id is not registered.");
    }
    await action(finder, index);
  }

  Duration? _parseDuration(dynamic value) {
    if (value == null) return null;
    if (value is int) return Duration(milliseconds: value);
    if (value is double) return Duration(milliseconds: value.round());
    if (value is Map) {
      final ms = value["milliseconds"] ?? value["ms"];
      if (ms is num) return Duration(milliseconds: ms.round());
    }
    return null;
  }

  IconData _parseIcon(dynamic value) {
    if (value is Map) {
      final codePoint = value["code_point"] as int?;
      if (codePoint == null) {
        throw Exception("Icon payload must include 'code_point'.");
      }
      return IconData(
        codePoint,
        fontFamily: value["font_family"] as String?,
        fontPackage: value["font_package"] as String?,
        matchTextDirection: (value["match_text_direction"] as bool?) ?? false,
      );
    } else if (value is int) {
      return IconData(value, fontFamily: "MaterialIcons");
    }
    throw Exception("Invalid icon format: $value");
  }

  Key _parseKey(dynamic value) {
    final v = (value is Map) ? value["value"] : value;
    // Preserve the concrete value type so the constructed ValueKey<T> matches
    // the one the rendered control assigned — ValueKey's `==` is runtimeType
    // strict (ValueKey<Object>('x') != ValueKey<String>('x')).
    return switch (v) {
      String s => ValueKey<String>(s),
      int i => ValueKey<int>(i),
      double d => ValueKey<double>(d),
      bool b => ValueKey<bool>(b),
      _ => ValueKey<dynamic>(v),
    };
  }

  Future<void> _sendResponse(
    dynamic id, {
    dynamic result,
    String? error,
    String? stack,
  }) async {
    final payload = <String, dynamic>{"id": id};
    if (error != null) {
      payload["error"] = error;
      if (stack != null) {
        payload["stack"] = stack;
      }
    } else {
      payload["result"] = result;
    }
    final encoded = jsonEncode(payload);
    _socket.add(FrameDecoder.encode(utf8.encode(encoded)));
    await _socket.flush();
  }

  void _closeSilently() {
    _subscription?.cancel();
    _triggerTeardown();
    if (!_connectionClosed.isCompleted) {
      _connectionClosed.complete();
    }
  }

  void _triggerTeardown() {
    if (_teardownRequested) {
      return;
    }
    _teardownRequested = true;
    super.teardown();
  }

  @override
  void teardown() => _triggerTeardown();

  /// Blocks until Python calls teardown (or the connection drops). Commands are
  /// handled in the socket subscription; the test body just parks here, exactly
  /// like the host-mode FlutterWidgetTester.
  @override
  Future waitForTeardown() async {
    await _commandQueue;
    await Future.wait([super.waitForTeardown(), _connectionClosed.future]);
  }
}

class _CommandResponse {
  final dynamic result;
  final bool closeAfter;

  const _CommandResponse(this.result, {required this.closeAfter});
}
