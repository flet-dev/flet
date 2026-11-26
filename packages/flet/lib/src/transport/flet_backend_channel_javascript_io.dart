import 'dart:typed_data';

import 'flet_backend_channel.dart';

class FletJavaScriptBackendChannel implements FletBackendChannel {
  final String address;
  final Map<String, dynamic> args;

  /// Run the Python worker isolated from the page; see
  /// [FletBackend.isolated].
  final bool isolated;
  final FletBackendChannelOnPacketCallback onPacket;
  final FletBackendChannelOnDisconnectCallback onDisconnect;

  FletJavaScriptBackendChannel(
      {required this.address,
      required this.args,
      this.isolated = false,
      required this.onDisconnect,
      required this.onPacket});

  @override
  connect() async {}

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10;

  @override
  void send(Uint8List packet) {}

  @override
  void disconnect() {}
}
