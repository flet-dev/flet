import 'dart:js_interop';

import 'package:flutter/foundation.dart';

import 'flet_backend_channel.dart';

@JS()
external JSPromise jsConnect(
    String appId, JSAny args, JSExportedDartFunction onMessage);

/// `transferList` names ArrayBuffers whose ownership moves to the worker, so
/// `postMessage` hands them over instead of structured-cloning them. Callers
/// pass the packet's own `.buffer`, which keeps bulk DataChannel frames
/// zero-copy across the Worker boundary and detaches the caller's view — safe
/// because every packet is freshly allocated per send and never read back.
@JS()
external void jsSend(String appId, JSUint8Array data, JSArray<JSObject>? transferList);

@JS()
external void jsDisconnect(String appId);

/// Marks the worker's "your script never started a UI" report, so a host page
/// embedding the app can render something friendlier than a crash panel.
/// It is addressed to that host, not to the person looking at the page, so it
/// is stripped before the message reaches the boot screen.
const _noUiSentinel = "__flet_no_ui__:";

/// Returns [error] with a leading [_noUiSentinel] marker removed, or unchanged
/// if it carries none.
///
/// Searches rather than matching a prefix: the worker's string reaches us
/// through a rejected JS promise, so the marker is not guaranteed to survive at
/// offset 0.
String _stripNoUiSentinel(String error) {
  final start = error.indexOf(_noUiSentinel);
  return start == -1
      ? error
      : error.substring(start + _noUiSentinel.length).trimLeft();
}

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
    try {
      await jsConnect(address, args.jsify()!, _onMessage.toJS).toDart;
    } catch (e) {
      // `jsConnect` resolves as soon as the worker reports back, and rejects
      // only when that report is an error — meaning Python already ran and
      // failed (a bad import, a missing dependency, an app archive that would
      // not download). There is no server here to come up later, so this is
      // final rather than something to retry.
      throw FletAppStartupException(_stripNoUiSentinel(e.toString()));
    }
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
    final jsBuffer = packet.buffer.toJS;
    final transferList = <JSObject>[jsBuffer as JSObject].toJS;
    jsSend(address, jsBytes, transferList);
  }

  @override
  void disconnect() {
    jsDisconnect(address);
  }
}
