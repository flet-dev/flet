import '../protocol/message.dart';
import 'flet_backend_channel.dart';

class FletJavaScriptBackendChannel implements FletBackendChannel {
  final String address;
  final Map<String, dynamic> args;
  final FletBackendChannelOnMessageCallback onMessage;
  final FletBackendChannelOnDisconnectCallback onDisconnect;

  FletJavaScriptBackendChannel(
      {required this.address,
      required this.args,
      required this.onDisconnect,
      required this.onMessage});

  @override
  connect() async {}

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 10;

  @override
  void send(Message data) {}

  @override
  void disconnect() {}
}
