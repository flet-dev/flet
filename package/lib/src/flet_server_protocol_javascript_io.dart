import 'flet_server_protocol.dart';

class FletJavaScriptServerProtocol implements FletServerProtocol {
  final String address;
  final FletServerProtocolOnMessageCallback onMessage;
  final FletServerProtocolOnDisconnectCallback onDisconnect;

  FletJavaScriptServerProtocol(
      {required this.address,
      required this.onDisconnect,
      required this.onMessage});

  @override
  connect() async {}

  @override
  void send(String message) {}

  @override
  void disconnect() {}
}
