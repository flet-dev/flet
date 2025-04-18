import 'dart:js_interop';

import 'package:flutter/foundation.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;

import '../protocol/message.dart';
import 'flet_backend_channel.dart';

@JS()
external JSPromise jsConnect(String appId, JSExportedDartFunction onMessage);

@JS()
external void jsSend(String appId, JSUint8Array data);

@JS()
external void jsDisconnect(String appId);

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
    await jsConnect(address, _onMessage.toJS).toDart;
  }

  void _onMessage(JSUint8Array data) {
    onMessage(Message.fromJson(msgpack.deserialize(data.toDart)));
  }

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10000;

  @override
  void send(Message message) {
    jsSend(address, msgpack.serialize(message.toJson()).toJS);
  }

  @override
  void disconnect() {
    jsDisconnect(address);
  }
}
