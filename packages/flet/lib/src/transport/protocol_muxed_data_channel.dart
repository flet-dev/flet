import 'dart:async';
import 'dart:typed_data';

import '../flet_backend.dart';
import 'data_channel.dart';

/// Default [DataChannelFactory] used when the embedder does not inject a
/// faster transport (i.e. dev mode `flet run` over UDS/TCP, web with
/// Python server, web with Pyodide). Allocates a monotonic 32-bit id per
/// channel and ships frames as `[0x01][channel_id:u32 LE][payload]` over
/// the active [FletBackendChannel] alongside regular Flet protocol traffic.
///
/// Ids start at 1; 0 is reserved as the "unallocated" sentinel for the
/// `channel_id` field on a control before Dart has minted one. Counter is
/// session-scoped (one [FletBackend] = one session); at one allocation
/// per microsecond the space lasts ~1 hour, well past any realistic
/// channel-churn pattern.
class ProtocolMuxedDataChannelFactory implements DataChannelFactory {
  ProtocolMuxedDataChannelFactory(this._backend);
  final FletBackend _backend;
  int _nextId = 1;

  @override
  DataChannel open() {
    final id = _nextId++;
    return ProtocolMuxedDataChannel(_backend, id);
  }
}

/// Concrete [DataChannel] that rides the Flet protocol transport. Frames
/// are wrapped as `[0x01][channel_id:u32 LE][payload]`; inbound frames are
/// dispatched to [deliver] via [FletBackend]'s mux registry.
class ProtocolMuxedDataChannel implements DataChannel {
  ProtocolMuxedDataChannel(this._backend, this._id) {
    _backend.registerDataChannel(_id, this);
  }

  final FletBackend _backend;
  final int _id;
  final StreamController<Uint8List> _controller =
      StreamController<Uint8List>.broadcast();
  bool _closed = false;

  @override
  int get id => _id;

  @override
  Stream<Uint8List> get messages => _controller.stream;

  @override
  bool send(Uint8List bytes) {
    if (_closed) return false;
    // Header: [0x01][channel_id:u32 LE]. Single allocation for the whole
    // packet (no BytesBuilder copies) — keeps the hot path tight.
    final packet = Uint8List(5 + bytes.length);
    packet[0] = 0x01;
    final view = ByteData.sublistView(packet, 1, 5);
    view.setUint32(0, _id, Endian.little);
    packet.setRange(5, packet.length, bytes);
    _backend.sendRawPacket(packet);
    return true;
  }

  /// Called by [FletBackend._onPacket] when a 0x01 frame arrives for this id.
  void deliver(Uint8List bytes) {
    if (_closed) return;
    _controller.add(bytes);
  }

  @override
  void close() {
    if (_closed) return;
    _closed = true;
    _backend.unregisterDataChannel(_id);
    _controller.close();
  }
}
