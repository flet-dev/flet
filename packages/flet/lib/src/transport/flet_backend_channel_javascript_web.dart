@JS()
library;

import 'dart:js_interop';
import 'dart:js_util';

import 'package:flutter/foundation.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;

import '../protocol/message.dart';
import 'flet_backend_channel.dart';

typedef FletBackendJavascriptChannelOnMessageCallback = void Function(
    Uint8List message);

@JS()
external dynamic jsConnect(
    FletBackendJavascriptChannelOnMessageCallback onMessage);

@JS()
external dynamic jsSend(Uint8List data);

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
    await promiseToFuture(jsConnect(allowInterop(_onMessage)));
  }

  _onMessage(Uint8List data) {
    onMessage(msgpack.deserialize(data));
  }

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10;

  @override
  void send(Message message) {
    jsSend(msgpack.serialize(message));
  }

  @override
  void disconnect() {}
}
