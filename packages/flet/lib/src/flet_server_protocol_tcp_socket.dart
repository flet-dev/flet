import 'dart:convert' show utf8;
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/foundation.dart';

import 'flet_server_protocol.dart';
import 'utils/networking.dart';

const int defaultLocalReconnectInterval = 200;
const int defaultPublicReconnectInterval = 500;

class FletTcpSocketServerProtocol implements FletServerProtocol {
  String address;
  FletServerProtocolOnMessageCallback onMessage;
  FletServerProtocolOnDisconnectCallback onDisconnect;
  Socket? _socket;
  late final bool _isLocalConnection;
  late final int _defaultReconnectIntervalMs;

  FletTcpSocketServerProtocol(
      {required this.address,
      required this.onDisconnect,
      required this.onMessage});

  @override
  connect() async {
    debugPrint("Connecting to Socket server $address...");

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

    BytesBuilder buffer = BytesBuilder();
    int msgLen = 0;

    // listen for responses from the server
    _socket!.listen(
      // handle data from the server
      (Uint8List data) {
        debugPrint("Received packet: ${data.length}");
        int packetLen = data.length;

        // process packet
        // it can contain multiple messages
        int i = 0;
        while (i < packetLen) {
          // read message size
          if (msgLen == 0) {
            //print("Read message size: $i");
            int end = i + (4 - buffer.length);
            if (end > packetLen) {
              end = packetLen;
            }
            buffer.add(data.sublist(i, end));

            i = end;

            if (buffer.length == 4) {
              msgLen = ByteData.sublistView(buffer.toBytes())
                  .getUint32(0, Endian.big);
              //print("Message size: $msgLen");
              buffer.clear();
            }
          }

          // read message body
          if (msgLen > 0) {
            //print("Read message body: $i");
            int end = i + (msgLen - buffer.length);
            if (end > packetLen) {
              end = packetLen;
            }
            buffer.add(data.sublist(i, end));

            i = end;

            if (buffer.length == msgLen) {
              String message = String.fromCharCodes(buffer.toBytes());
              debugPrint('Received message: ${message.length}');
              _onMessage(message);
              buffer.clear();
              msgLen = 0;
            }
          }
        }
      },

      // handle errors
      onError: (error) {
        debugPrint("Error: $error");
        _socket?.destroy();
        onDisconnect();
      },

      // handle server ending connection
      onDone: () {
        debugPrint('Server left.');
        _socket?.destroy();
        onDisconnect();
      },
    );
  }

  @override
  bool get isLocalConnection => _isLocalConnection;

  @override
  int get defaultReconnectIntervalMs => _defaultReconnectIntervalMs;

  _onMessage(message) {
    onMessage(message);
  }

  Uint8List int32bytes(int value) =>
      Uint8List(4)..buffer.asInt32List()[0] = value;

  Uint8List int32BigEndianBytes(int value) =>
      Uint8List(4)..buffer.asByteData().setInt32(0, value, Endian.big);

  @override
  void send(String message) {
    var buffer = utf8.encode(message);
    _socket!.add(int32BigEndianBytes(buffer.length));
    debugPrint('Sending: ${buffer.length}');
    _socket!.write(message);
  }

  @override
  void disconnect() {
    _socket?.destroy();
  }
}
