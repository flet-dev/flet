import 'flet_server_protocol_tcp_socket.dart';
import 'flet_server_protocol_web_socket.dart';

typedef FletServerProtocolOnDisconnectCallback = void Function();
typedef FletServerProtocolOnMessageCallback = void Function(String message);

abstract class FletServerProtocol {
  factory FletServerProtocol(
      {required String address,
      required FletServerProtocolOnDisconnectCallback onDisconnect,
      required FletServerProtocolOnMessageCallback onMessage}) {
    if (address.startsWith("http://") || address.startsWith("https://")) {
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
