import 'dart:js_interop';

import 'package:flutter/foundation.dart';

import 'flet_backend_channel.dart';

@JS()
external JSPromise jsConnect(
    String appId, JSAny args, JSExportedDartFunction onMessage);

/// The optional `transferList` argument names ArrayBuffers (in `data`'s
/// underlying buffer) whose ownership should transfer to the receiver —
/// `postMessage` then avoids the structured-clone copy. We pass the
/// packet's `.buffer` here so bulk DataChannel frames are zero-copy across
/// the Worker boundary.
@JS()
external void jsSend(String appId, JSUint8Array data, JSArray<JSObject>? transferList);

@JS()
external void jsDisconnect(String appId);

class FletJavaScriptBackendChannel implements FletBackendChannel {
  final String address;
  final Map<String, dynamic> args;
  final FletBackendChannelOnPacketCallback onPacket;
  final FletBackendChannelOnDisconnectCallback onDisconnect;

  FletJavaScriptBackendChannel(
      {required this.address,
      required this.args,
      required this.onDisconnect,
      required this.onPacket});

  @override
  connect() async {
    debugPrint("Connecting to Flet JavaScript channel $address...");
    await jsConnect(address, args.jsify()!, _onMessage.toJS).toDart;
  }

  void _onMessage(JSUint8Array data) {
    // Each postMessage event is one packet — message boundaries are
    // preserved by the underlying MessageChannel.
    onPacket(data.toDart);
  }

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10000;

  @override
  void send(Uint8List packet) {
    final jsBytes = packet.toJS;
    // Transfer the underlying ArrayBuffer to the receiver — zero copy
    // across the Worker boundary. Safe because the sender does not access
    // `packet` after this call (FletBackend always builds a fresh buffer
    // per send).
    final jsBuffer = packet.buffer.toJS;
    final transferList = <JSObject>[jsBuffer as JSObject].toJS;
    jsSend(address, jsBytes, transferList);
  }

  @override
  void disconnect() {
    jsDisconnect(address);
  }
}
