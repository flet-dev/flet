import '../protocol/message.dart';
import '../utils/platform_utils_non_web.dart'
    if (dart.library.js) "utils/platform_utils_web.dart";
import 'flet_backend_channel_javascript_io.dart'
    if (dart.library.js) "flet_backend_channel_javascript_web.dart";
import 'flet_backend_channel_mock.dart';
import 'flet_backend_channel_socket.dart';
import 'flet_backend_channel_web_socket.dart';

typedef FletBackendChannelOnDisconnectCallback = void Function();
typedef FletBackendChannelOnMessageCallback = void Function(Message message);

abstract class FletBackendChannel {
  factory FletBackendChannel(
      {required String address,
      required FletBackendChannelOnDisconnectCallback onDisconnect,
      required FletBackendChannelOnMessageCallback onMessage}) {
    if (isFletWebPyodideMode()) {
      // JavaScript
      return FletJavaScriptBackendChannel(
          address: address, onDisconnect: onDisconnect, onMessage: onMessage);
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
