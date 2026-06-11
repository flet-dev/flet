import '../protocol/message.dart';
import '../utils/platform_utils_web.dart'
    if (dart.library.io) "../utils/platform_utils_non_web.dart";
import 'flet_backend_channel_javascript_web.dart'
    if (dart.library.io) "flet_backend_channel_javascript_io.dart";
import 'flet_backend_channel_mock.dart';
import 'flet_backend_channel_socket.dart';
import 'flet_backend_channel_web_socket.dart';

typedef FletBackendChannelOnDisconnectCallback = void Function();
typedef FletBackendChannelOnMessageCallback = void Function(Message message);

/// Builds a custom [FletBackendChannel] supplied by the embedder.
///
/// When provided to [FletApp]/[FletBackend], the channel is used directly and
/// the URL-scheme factory below is skipped — letting embedded runtimes (e.g.
/// `serious_python`'s in-process Dart↔Python FFI bridge) plug in a transport
/// that needs more setup than a `String address` URL can express, without
/// forcing the `flet` package to take a Python-related dependency.
typedef FletBackendChannelBuilder = FletBackendChannel Function({
  required FletBackendChannelOnMessageCallback onMessage,
  required FletBackendChannelOnDisconnectCallback onDisconnect,
});

abstract class FletBackendChannel {
  factory FletBackendChannel(
      {required String address,
      required Map<String, dynamic> args,
      required bool forcePyodide,
      required FletBackendChannelOnDisconnectCallback onDisconnect,
      required FletBackendChannelOnMessageCallback onMessage}) {
    if (isPyodideMode() || forcePyodide) {
      // Pyodide/JavaScript
      return FletJavaScriptBackendChannel(
          address: address,
          args: args,
          onDisconnect: onDisconnect,
          onMessage: onMessage);
    } else if (address.startsWith("http://") ||
        address.startsWith("https://")) {
      // WebSocket
      return FletWebSocketBackendChannel(
          address: address, onDisconnect: onDisconnect, onMessage: onMessage);
    } else if (address == "mock") {
      // Mock
      return FletMockBackendChannel(
          address: address, onDisconnect: onDisconnect, onMessage: onMessage);
    } else {
      // TCP or UDS
      return FletSocketBackendChannel(
          address: address, onDisconnect: onDisconnect, onMessage: onMessage);
    }
  }

  Future connect();
  bool get isLocalConnection;
  int get defaultReconnectIntervalMs;
  void send(Message message);
  void disconnect();
}
