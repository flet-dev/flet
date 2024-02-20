import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'flet_server_protocol.dart';
import 'utils/networking.dart';
import 'utils/platform_utils_non_web.dart'
    if (dart.library.js) "utils/platform_utils_web.dart";
import 'utils/uri.dart';

class FletWebSocketServerProtocol implements FletServerProtocol {
  late final String _wsUrl;
  late final bool _isLocalConnection;
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
  bool get isLocalConnection => _isLocalConnection;

  @override
  int get defaultReconnectIntervalMs => 500;

  @override
  Future connect() async {
    debugPrint("Connecting to WebSocket server $_wsUrl...");
    try {
      // todo
      var uri = Uri.parse(_wsUrl);
      if (kIsWeb) {
        _isLocalConnection = isLocalhost(uri);
      } else {
        _isLocalConnection = await isPrivateHost(uri.host);
      }

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

  String getWebSocketEndpoint(Uri uri) {
    final wsScheme = uri.scheme == "https" ? "wss" : "ws";
    final wsPath = getWebsocketEndpointPath(uri.path);
    if (wsPath == "") {
      throw Exception("WebSocket endpoint path cannot be empty.");
    }
    return "$wsScheme://${uri.authority}/$wsPath";
  }
}
