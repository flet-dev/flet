import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;

import '../protocol/message.dart';
import '../utils/networking.dart';
import 'flet_backend_channel.dart';
import 'flet_msgpack_decoder.dart';
import 'flet_msgpack_encoder.dart';
import 'streaming_msgpack_deserializer.dart';

const int defaultLocalReconnectInterval = 200;
const int defaultPublicReconnectInterval = 500;

class FletSocketBackendChannel implements FletBackendChannel {
  String address;
  FletBackendChannelOnMessageCallback onMessage;
  FletBackendChannelOnDisconnectCallback onDisconnect;
  Socket? _socket;
  late final bool _isLocalConnection;
  late final int _defaultReconnectIntervalMs;

  // Create an instance of the StreamingDeserializer.
  // This object buffers incoming chunks and decodes complete MessagePack objects.
  final StreamingMsgpackDeserializer _streamingDeserializer;

  FletSocketBackendChannel({
    required this.address,
    required this.onDisconnect,
    required this.onMessage,
  }) : _streamingDeserializer =
            StreamingMsgpackDeserializer(extDecoder: FletMsgpackDecoder());

  @override
  connect() async {
    debugPrint("Connecting to Socket $address...");

    if (address.startsWith("tcp://")) {
      var u = Uri.parse(address);
      _isLocalConnection = await isPrivateHost(u.host);
      _defaultReconnectIntervalMs = _isLocalConnection
          ? defaultLocalReconnectInterval
          : defaultPublicReconnectInterval;
      _socket = await Socket.connect(u.host, u.port);
      debugPrint(
          'Connected to: ${_socket!.remoteAddress.address}:${_socket!.remotePort}');
    } else {
      final udsPath = InternetAddress(address, type: InternetAddressType.unix);
      _isLocalConnection = true;
      _defaultReconnectIntervalMs = defaultLocalReconnectInterval;
      _socket = await Socket.connect(udsPath, 0);
      debugPrint('Connected to: $udsPath');
    }

    // Listen for incoming data.
    _socket!.listen(
      (Uint8List data) {
        debugPrint("Received packet: ${data.length}");
        // Feed the incoming chunk into the streaming deserializer.
        _streamingDeserializer.addChunk(data);
        // Try to decode complete MessagePack messages from buffered data.
        var messages = _streamingDeserializer.decodeMessages();
        for (var message in messages) {
          //debugPrint('Decoded message: ${message.toString()}');
          _onMessage(message);
        }
      },
      onError: (error) {
        debugPrint("Error: $error");
        _socket?.destroy();
        onDisconnect();
      },
      onDone: () {
        debugPrint('Server disconnected.');
        _socket?.destroy();
        onDisconnect();
      },
    );
  }

  @override
  bool get isLocalConnection => _isLocalConnection;

  @override
  int get defaultReconnectIntervalMs => _defaultReconnectIntervalMs;

  // Note: At this point, the incoming message is already a decoded MessagePack object.
  _onMessage(dynamic message) {
    onMessage(Message.fromJson(message));
  }

  @override
  void send(Message message) {
    // Serialize the message using MessagePack and send it.
    _socket!.add(
        msgpack.serialize(message.toJson(), extEncoder: FletMsgpackEncoder()));
  }

  @override
  void disconnect() {
    _socket?.destroy();
  }
}
