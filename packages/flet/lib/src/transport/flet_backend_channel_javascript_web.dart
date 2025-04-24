import 'dart:js_interop';

import 'package:flutter/foundation.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;

import '../protocol/message.dart';
import 'flet_backend_channel.dart';

@JS()
external JSPromise jsConnect(JSExportedDartFunction onMessage);

@JS()
external void jsSend(JSUint8Array data);

typedef FletBackendJavascriptChannelOnMessageCallback = void Function(
    List<int> message);

class FletJavaScriptBackendChannel implements FletBackendChannel {
  final String address;
  final FletBackendChannelOnMessageCallback onMessage;
  final FletBackendChannelOnDisconnectCallback onDisconnect;

  FletJavaScriptBackendChannel(
      {required this.address,
      required this.onDisconnect,
      required this.onMessage});

  @override
  connect() async {
    debugPrint("Connecting to Flet JavaScript channel $address...");
    await jsConnect(_onMessage.toJS).toDart;
  }

  void _onMessage(JSUint8Array data) {
    onMessage(Message.fromList(msgpack.deserialize(data.toDart)));
  }

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10000;

  @override
  void send(Message message) {
    jsSend(msgpack.serialize(message.toList()).toJS);
  }

  @override
  void disconnect() {}
}
