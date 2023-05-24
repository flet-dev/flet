import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'flet_server_protocol.dart';
import 'utils/uri.dart';

class FletWebSocketServerProtocol implements FletServerProtocol {
  late final String _wsUrl;
  FletServerProtocolOnMessageCallback onMessage;
  FletServerProtocolOnDisconnectCallback onDisconnect;
  WebSocketChannel? _channel;

  FletWebSocketServerProtocol(
      {required String address,
      required this.onDisconnect,
      required this.onMessage}) {
    _wsUrl = getWebSocketEndpoint(Uri.parse(address));
  }

  @override
  Future connect() async {
    debugPrint("Connecting to WebSocket server $_wsUrl...");
    try {
      // todo
      _channel = WebSocketChannel.connect(Uri.parse(_wsUrl));
    } catch (e) {
      throw Exception('WebSocket connect error: $e');
    }
    _channel!.stream.listen(_onMessage, onDone: () async {
      debugPrint("WebSocket stream closed");
      onDisconnect();
    }, onError: (error) async {
      var socketError = error as WebSocketChannelException;
      debugPrint("WebSocket stream error: ${socketError.message}");
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
