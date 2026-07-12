import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/foundation.dart';

import '../utils/networking.dart';
import 'flet_backend_channel.dart';

const int defaultLocalReconnectInterval = 200;
const int defaultPublicReconnectInterval = 500;

/// TCP / Unix-domain-socket transport.
///
/// Wire format: every packet on the wire is prefixed with its length as
/// a 4-byte little-endian unsigned integer. The packet itself starts with
/// the 1-byte type discriminator interpreted by [FletBackend]; we just
/// deliver the payload bytes 1:1.
class FletSocketBackendChannel implements FletBackendChannel {
  String address;
  FletBackendChannelOnPacketCallback onPacket;
  FletBackendChannelOnDisconnectCallback onDisconnect;
  Socket? _socket;
  late final bool _isLocalConnection;
  late final int _defaultReconnectIntervalMs;

  // Inbound framing state: accumulate bytes, parse length-prefixed packets.
  // The builder is only flattened when a complete packet (or the 4-byte
  // length header) is available — never per incoming chunk, which would be
  // quadratic in packet size (multi-MB raw image frames arrive in dozens
  // of socket chunks).
  final BytesBuilder _inboundBuffer = BytesBuilder(copy: false);
  int? _pendingLen;

  FletSocketBackendChannel({
    required this.address,
    required this.onDisconnect,
    required this.onPacket,
  });

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

    _socket!.listen(
      _onBytes,
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

  void _onBytes(Uint8List chunk) {
    _inboundBuffer.add(chunk);
    // Parse as many complete packets as the buffer currently holds.
    while (true) {
      if (_pendingLen == null) {
        if (_inboundBuffer.length < 4) return;
        // Flatten to read the header. Cheap: at this point the buffer
        // holds at most one packet's worth of unconsumed leading bytes,
        // and with a single stored chunk takeBytes returns it as-is.
        final bytes = _inboundBuffer.takeBytes();
        _pendingLen =
            ByteData.sublistView(bytes, 0, 4).getUint32(0, Endian.little);
        if (bytes.length > 4) {
          _inboundBuffer.add(Uint8List.sublistView(bytes, 4));
        }
      }
      final len = _pendingLen!;
      if (_inboundBuffer.length < len) return;
      // Single flatten once the whole packet has arrived.
      final bytes = _inboundBuffer.takeBytes();
      _pendingLen = null;
      onPacket(Uint8List.sublistView(bytes, 0, len));
      if (bytes.length > len) {
        _inboundBuffer.add(Uint8List.sublistView(bytes, len));
      }
    }
  }

  @override
  bool get isLocalConnection => _isLocalConnection;

  @override
  int get defaultReconnectIntervalMs => _defaultReconnectIntervalMs;

  @override
  void send(Uint8List packet) {
    final header = ByteData(4)..setUint32(0, packet.length, Endian.little);
    _socket!.add(header.buffer.asUint8List());
    _socket!.add(packet);
  }

  @override
  void disconnect() {
    _socket?.destroy();
  }
}
