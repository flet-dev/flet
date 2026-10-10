import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

/// A transport that connects at once and lets the test report disconnects.
class _Channel implements FletBackendChannel {
  final FletBackendChannelOnDisconnectCallback onDisconnect;

  _Channel(this.onDisconnect);

  @override
  Future connect() async {}

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10;

  @override
  void send(Uint8List packet) {}

  @override
  void disconnect() {}
}

/// Returns a backend whose every connection attempt adds its channel to
/// [channels].
FletBackend _backend(List<_Channel> channels) => FletBackend(
      pageUri: Uri.parse("mock"),
      assetsDir: "",
      extensions: [],
      multiView: false,
      channelBuilder: ({
        required FletBackendChannelOnPacketCallback onPacket,
        required FletBackendChannelOnDisconnectCallback onDisconnect,
      }) {
        final channel = _Channel(onDisconnect);
        channels.add(channel);
        return channel;
      },
    );

Future<void> _settle() => Future.delayed(const Duration(milliseconds: 100));

void main() {
  test('a disconnect reported twice by a channel reconnects once', () async {
    final channels = <_Channel>[];
    final backend = _backend(channels);
    await backend.connect();

    channels[0].onDisconnect();
    channels[0].onDisconnect();
    await _settle();

    // The first connection plus exactly one reconnect.
    expect(channels, hasLength(2));

    backend.dispose();
  });

  test('a disconnect from a replaced channel does not reconnect', () async {
    final channels = <_Channel>[];
    final backend = _backend(channels);
    await backend.connect();
    channels[0].onDisconnect();
    await _settle();
    expect(channels, hasLength(2));

    channels[0].onDisconnect();
    await _settle();
    expect(channels, hasLength(2));

    // The current channel still reconnects.
    channels[1].onDisconnect();
    await _settle();
    expect(channels, hasLength(3));

    backend.dispose();
  });
}
