import 'flet_server_protocol_javascript_io.dart'
    if (dart.library.js) "flet_server_protocol_javascript_web.dart";
import 'flet_server_protocol_tcp_socket.dart';
import 'flet_server_protocol_web_socket.dart';
import 'utils/platform_utils_non_web.dart'
    if (dart.library.js) "utils/platform_utils_web.dart";

typedef FletServerProtocolOnDisconnectCallback = void Function();
typedef FletServerProtocolOnMessageCallback = void Function(String message);

abstract class FletServerProtocol {
  factory FletServerProtocol(
      {required String address,
      required FletServerProtocolOnDisconnectCallback onDisconnect,
      required FletServerProtocolOnMessageCallback onMessage}) {
    if (isFletWebPyodideMode()) {
      // JavaScript
      return FletJavaScriptServerProtocol(
          address: address, onDisconnect: onDisconnect, onMessage: onMessage);
    } else if (address.startsWith("http://") ||
        address.startsWith("https://")) {
      // WebSocket
      return FletWebSocketServerProtocol(
          address: address, onDisconnect: onDisconnect, onMessage: onMessage);
    } else {
      // TCP or UDS
      return FletTcpSocketServerProtocol(
          address: address, onDisconnect: onDisconnect, onMessage: onMessage);
    }
  }

  Future connect();
  void send(String message);
  void disconnect();
}
