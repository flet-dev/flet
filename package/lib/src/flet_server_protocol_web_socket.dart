import 'package:flet/src/flet_server_protocol.dart';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class FletWebSocketServerProtocol implements FletServerProtocol {
  String address;
  FletServerProtocolOnMessageCallback onMessage;
  FletServerProtocolOnDisconnectCallback onDisconnect;
  WebSocketChannel? _channel;

  FletWebSocketServerProtocol(
      {required this.address,
      required this.onDisconnect,
      required this.onMessage});

  @override
  connect() async {
    debugPrint("Connecting to WebSocket server $address...");
    _channel = WebSocketChannel.connect(Uri.parse(address));
    _channel!.stream.listen(_onMessage, onDone: () async {
      debugPrint("WebSocket stream closed");
      onDisconnect();
    }, onError: (error) async {
      debugPrint("WebSocket stream error $error");
    });
  }

  _onMessage(message) {
    onMessage(message);
  }

  @override
  void send(String message) {
    _channel?.sink.add(message);
  }

  @override
  void disconnect() {
    _channel?.sink.close();
  }
}
