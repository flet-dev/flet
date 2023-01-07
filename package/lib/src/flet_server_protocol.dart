typedef FletServerProtocolOnDisconnectCallback = void Function();
typedef FletServerProtocolOnMessageCallback = void Function(String message);

abstract class FletServerProtocol {
  Future connect();
  void send(String message);
  void disconnect();
}
