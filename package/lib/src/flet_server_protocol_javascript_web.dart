@JS()
library script.js;

import 'dart:js_util';

import 'package:flutter/foundation.dart';
import 'package:js/js.dart';

import 'flet_server_protocol.dart';

@JS()
external dynamic jsConnect(FletServerProtocolOnMessageCallback onMessage);

@JS()
external dynamic jsSend(String data);

class FletJavaScriptServerProtocol implements FletServerProtocol {
  final String address;
  final FletServerProtocolOnMessageCallback onMessage;
  final FletServerProtocolOnDisconnectCallback onDisconnect;

  FletJavaScriptServerProtocol(
      {required this.address,
      required this.onDisconnect,
      required this.onMessage});

  @override
  connect() async {
    debugPrint("Connecting to JavaScript server $address...");
    await promiseToFuture(jsConnect(allowInterop(onMessage)));
  }

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10;

  @override
  void send(String message) {
    jsSend(message);
  }

  @override
  void disconnect() {}
}
