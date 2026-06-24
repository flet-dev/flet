import 'dart:typed_data';

import '../utils/platform_utils_web.dart'
    if (dart.library.io) "../utils/platform_utils_non_web.dart";
import 'flet_backend_channel_javascript_web.dart'
    if (dart.library.io) "flet_backend_channel_javascript_io.dart";
import 'flet_backend_channel_mock.dart';
import 'flet_backend_channel_socket.dart';
import 'flet_backend_channel_web_socket.dart';

typedef FletBackendChannelOnDisconnectCallback = void Function();

/// Called when the transport receives one complete packet from the peer.
/// The packet is the **full** byte sequence including the 1-byte type
/// discriminator at offset 0:
///
///   `[type:u8][payload]`
///
/// where `type == 0x00` is a MsgPack-encoded Flet protocol frame and
/// `type == 0x01` is a raw DataChannel frame (`[channel_id:u32 LE][bytes]`).
/// Transports are responsible only for delivering packet boundaries; the
/// type byte is interpreted by [FletBackend].
typedef FletBackendChannelOnPacketCallback = void Function(Uint8List packet);

/// Builds a custom [FletBackendChannel] supplied by the embedder.
///
/// When provided to [FletApp]/[FletBackend], the channel is used directly and
/// the URL-scheme factory below is skipped — letting embedded runtimes (e.g.
/// `serious_python`'s in-process Dart↔Python FFI bridge) plug in a transport
/// that needs more setup than a `String address` URL can express, without
/// forcing the `flet` package to take a Python-related dependency.
typedef FletBackendChannelBuilder = FletBackendChannel Function({
  required FletBackendChannelOnPacketCallback onPacket,
  required FletBackendChannelOnDisconnectCallback onDisconnect,
});

abstract class FletBackendChannel {
  factory FletBackendChannel(
      {required String address,
      required Map<String, dynamic> args,
      required bool forcePyodide,
      required FletBackendChannelOnDisconnectCallback onDisconnect,
      required FletBackendChannelOnPacketCallback onPacket}) {
    if (isPyodideMode() || forcePyodide) {
      // Pyodide/JavaScript
      return FletJavaScriptBackendChannel(
          address: address,
          args: args,
          onDisconnect: onDisconnect,
          onPacket: onPacket);
    } else if (address.startsWith("http://") ||
        address.startsWith("https://")) {
      // WebSocket
      return FletWebSocketBackendChannel(
          address: address, onDisconnect: onDisconnect, onPacket: onPacket);
    } else if (address == "mock") {
      // Mock
      return FletMockBackendChannel(
          address: address, onDisconnect: onDisconnect, onPacket: onPacket);
    } else {
      // TCP or UDS
      return FletSocketBackendChannel(
          address: address, onDisconnect: onDisconnect, onPacket: onPacket);
    }
  }

  Future connect();
  bool get isLocalConnection;
  int get defaultReconnectIntervalMs;

  /// Sends one full packet — `[type:u8][payload]` — to the peer. The transport
  /// is responsible for delimiting packet boundaries (length prefix on
  /// stream-oriented transports; native message boundary on others).
  void send(Uint8List packet);

  void disconnect();
}
