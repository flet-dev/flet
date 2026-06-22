import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import '../utils/networking.dart';
import '../utils/platform_utils_web.dart'
    if (dart.library.io) "../utils/platform_utils_non_web.dart";
import '../utils/uri.dart';
import 'flet_backend_channel.dart';

class FletWebSocketBackendChannel implements FletBackendChannel {
  late final String _wsUrl;
  late final bool _isLocalConnection;
  FletBackendChannelOnPacketCallback onPacket;
  FletBackendChannelOnDisconnectCallback onDisconnect;
  WebSocketChannel? _channel;

  FletWebSocketBackendChannel(
      {required String address,
      required this.onDisconnect,
      required this.onPacket}) {
    _wsUrl = getWebSocketEndpoint(Uri.parse(address));
  }

  @override
  bool get isLocalConnection => _isLocalConnection;

  @override
  int get defaultReconnectIntervalMs => 500;

  @override
  Future connect() async {
    debugPrint("Connecting to WebSocket $_wsUrl...");
    try {
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

  void _onMessage(dynamic message) {
    // Each WebSocket binary message is one complete packet — message
    // boundaries are preserved by the transport, no framing needed here.
    if (message is Uint8List) {
      onPacket(message);
    } else if (message is List<int>) {
      onPacket(Uint8List.fromList(message));
    } else {
      debugPrint("Unexpected WebSocket message type: ${message.runtimeType}");
    }
  }

  @override
  void send(Uint8List packet) {
    _channel?.sink.add(packet);
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
