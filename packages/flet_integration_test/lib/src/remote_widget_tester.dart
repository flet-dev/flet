import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'flutter_test_finder.dart';
import 'flutter_tester.dart';

class RemoteWidgetTester extends FlutterWidgetTester {
  final Socket _socket;
  final Map<int, FlutterTestFinder> _finders = {};
  final Completer<void> _connectionClosed = Completer<void>();
  Future<void> _commandQueue = Future<void>.value();
  StreamSubscription<String>? _subscription;
  bool _teardownRequested = false;

  RemoteWidgetTester._(
    WidgetTester tester,
    IntegrationTestWidgetsFlutterBinding binding,
    this._socket,
  ) : super(tester, binding) {
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
    final lines = utf8.decoder.bind(_socket).transform(const LineSplitter());
    _subscription = lines.listen(
      (line) {
        _commandQueue = _commandQueue.then((_) => _processLine(line));
      },
      onError: (error, stackTrace) {
        if (!_connectionClosed.isCompleted) {
          _connectionClosed.completeError(error, stackTrace);
        }
        _closeSilently();
      },
      onDone: () {
        _closeSilently();
        if (!_connectionClosed.isCompleted) {
          _connectionClosed.complete();
        }
      },
      cancelOnError: true,
    );
  }

  Future<void> _processLine(String line) async {
    final dynamic decoded = jsonDecode(line);
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
      _sendResponse(id, result: response.result);
      if (response.closeAfter) {
        await _socket.flush();
        await _socket.close();
        await _subscription?.cancel();
        if (!_connectionClosed.isCompleted) {
          _connectionClosed.complete();
        }
      }
    } catch (error, stackTrace) {
      _sendResponse(id, error: "$error", stack: stackTrace.toString());
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
        await pump(duration: parseDuration(params["duration"]));
        return _ok();
      case "pump_and_settle":
        await pumpAndSettle(duration: parseDuration(params["duration"]));
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
        await _withFinder(params["id"], (finder) => tap(finder));
        return _ok();
      case "long_press":
        await _withFinder(params["id"], (finder) => longPress(finder));
        return _ok();
      case "enter_text":
        await _withFinder(
          params["id"],
          (finder) => enterText(finder, params["text"] as String),
        );
        return _ok();
      case "mouse_hover":
        await _withFinder(params["id"], (finder) => mouseHover(finder));
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
    dynamic id,
    Future<void> Function(FlutterTestFinder finder) action,
  ) async {
    final finder = _finders[id];
    if (finder == null) {
      throw Exception("Finder with id $id is not registered.");
    }
    await action(finder);
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
    if (value is Map) {
      final keyValue = value["value"];
      return ValueKey<dynamic>(keyValue);
    }
    return ValueKey<dynamic>(value);
  }

  void _sendResponse(
    dynamic id, {
    dynamic result,
    String? error,
    String? stack,
  }) {
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
    _socket.add(utf8.encode("$encoded\n"));
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
