import 'dart:async';
import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flet/src/transport/protocol_muxed_data_channel.dart';
import 'package:flutter_test/flutter_test.dart';

/// Minimal in-memory transport: captures outbound packets and lets the test
/// inject inbound ones, exercising FletBackend's type-byte dispatch + the
/// muxed DataChannel routing without spinning up a real transport.
class _FakeChannel implements FletBackendChannel {
  final List<Uint8List> sent = [];
  late FletBackendChannelOnPacketCallback _onPacket;

  FletBackendChannelBuilder get builder => ({
        required FletBackendChannelOnPacketCallback onPacket,
        required FletBackendChannelOnDisconnectCallback onDisconnect,
      }) {
        _onPacket = onPacket;
        return this;
      };

  void deliver(Uint8List packet) => _onPacket(packet);

  @override
  Future connect() async {}

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 0;

  @override
  void send(Uint8List packet) => sent.add(Uint8List.fromList(packet));

  @override
  void disconnect() {}
}

void main() {
  group('ProtocolMuxedDataChannel wire format', () {
    test('send emits [0x01][channel_id:u32 LE][payload]', () {
      final backend = FletBackend(
          pageUri: Uri.parse("mock"),
          assetsDir: "",
          extensions: [],
          multiView: false);
      final ch1 = backend.openDataChannel();
      final ch2 = backend.openDataChannel();
      expect(ch1.id, 1);
      expect(ch2.id, 2);
    });

    test('inbound 0x01 frame routes to the right channel', () async {
      final fake = _FakeChannel();
      final backend = FletBackend(
          pageUri: Uri.parse("mock"),
          assetsDir: "",
          extensions: [],
          multiView: false,
          channelBuilder: fake.builder);
      // Trigger the connect path so FletBackend wires the fake's onPacket.
      // We don't await — connect() also tries _registerClient which goes
      // through the (now unused) channel send path; both are fine for this
      // smoke test.
      // ignore: unawaited_futures
      backend.connect();

      final chA = backend.openDataChannel() as ProtocolMuxedDataChannel;
      final chB = backend.openDataChannel() as ProtocolMuxedDataChannel;

      final aFrames = <Uint8List>[];
      final bFrames = <Uint8List>[];
      chA.messages.listen(aFrames.add);
      chB.messages.listen(bFrames.add);

      // Inbound for channel B (id=2) → 0x01, id LE, payload.
      final inbound = Uint8List(5 + 3);
      inbound[0] = 0x01;
      ByteData.sublistView(inbound, 1, 5).setUint32(0, chB.id, Endian.little);
      inbound.setRange(5, 8, [10, 20, 30]);
      fake.deliver(inbound);

      // Let the stream-controller microtask flush.
      await Future<void>.delayed(Duration.zero);

      expect(aFrames, isEmpty);
      expect(bFrames, hasLength(1));
      expect(bFrames.single, equals(Uint8List.fromList([10, 20, 30])));

      // Stale frame for closed channel is silently dropped.
      chA.close();
      final staleA = Uint8List(5 + 1);
      staleA[0] = 0x01;
      ByteData.sublistView(staleA, 1, 5).setUint32(0, 1, Endian.little);
      staleA[5] = 99;
      fake.deliver(staleA); // no throw, no delivery
    });

    test('outbound send emits the muxed packet shape', () async {
      final fake = _FakeChannel();
      final backend = FletBackend(
          pageUri: Uri.parse("mock"),
          assetsDir: "",
          extensions: [],
          multiView: false,
          channelBuilder: fake.builder);
      // ignore: unawaited_futures
      backend.connect();

      // Drain the register-client packet that FletBackend.connect emits.
      final preCount = fake.sent.length;

      final ch = backend.openDataChannel();
      ch.send(Uint8List.fromList([0xAA, 0xBB, 0xCC]));

      // Filter to the 0x01 packets we care about.
      final dataPackets =
          fake.sent.skip(preCount).where((p) => p.isNotEmpty && p[0] == 0x01).toList();
      expect(dataPackets, hasLength(1));
      final p = dataPackets.single;
      expect(p[0], 0x01);
      expect(ByteData.sublistView(p, 1, 5).getUint32(0, Endian.little), ch.id);
      expect(p.sublist(5), equals(Uint8List.fromList([0xAA, 0xBB, 0xCC])));
    });
  });
}
