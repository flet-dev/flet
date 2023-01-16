@JS()
library script.js;

import 'dart:js_util';

import 'package:flutter/foundation.dart';
import 'package:js/js.dart';

import 'flet_server_protocol.dart';
import 'utils/uri.dart';

@JS()
external dynamic sleep(int ms);

@JS()
external dynamic jsConnect();

@JS()
external dynamic jsSend(String data);

@JS()
external dynamic jsReceive();

class FletJavaScriptServerProtocol implements FletServerProtocol {
  late final String _wsUrl;
  FletServerProtocolOnMessageCallback onMessage;
  FletServerProtocolOnDisconnectCallback onDisconnect;

  FletJavaScriptServerProtocol(
      {required String address,
      required this.onDisconnect,
      required this.onMessage}) {
    _wsUrl = getWebSocketEndpoint(Uri.parse(address));
  }

  @override
  connect() async {
    debugPrint("Connecting to JavaScript server $_wsUrl...");
    await promiseToFuture(jsConnect());
    receiveLoop();
  }

  Future receiveLoop() async {
    debugPrint("Starting receive loop...");
    while (true) {
      var message = await promiseToFuture(jsReceive());
      onMessage(message);
    }
  }

  @override
  void send(String message) {
    jsSend(message);
  }

  @override
  void disconnect() {}
}
