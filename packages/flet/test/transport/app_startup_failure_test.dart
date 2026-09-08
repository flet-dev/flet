import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

const _startupError = "Boom: no such module";

/// A transport whose `connect()` always fails, in one of the two ways
/// [FletBackend] must tell apart: the app itself failed to start, or the peer
/// is simply not reachable yet.
class _FailingChannel implements FletBackendChannel {
  final Object failure;
  int connectAttempts = 0;

  _FailingChannel(this.failure);

  FletBackendChannelBuilder get builder => ({
        required FletBackendChannelOnPacketCallback onPacket,
        required FletBackendChannelOnDisconnectCallback onDisconnect,
      }) =>
          this;

  @override
  Future connect() async {
    connectAttempts++;
    throw failure;
  }

  @override
  bool get isLocalConnection => true;

  // Long enough that a scheduled retry never fires during the test.
  @override
  int get defaultReconnectIntervalMs => 300000;

  @override
  void send(Uint8List packet) {}

  @override
  void disconnect() {}
}

FletBackend _backend(_FailingChannel channel,
        {FletAppErrorsHandler? errorsHandler}) =>
    FletBackend(
      pageUri: Uri.parse("mock"),
      assetsDir: "",
      extensions: [],
      multiView: false,
      channelBuilder: channel.builder,
      errorsHandler: errorsHandler,
    );

void main() {
  group('a FletAppStartupException', () {
    test('settles on the error instead of reconnecting', () async {
      final channel = _FailingChannel(
          const FletAppStartupException(_startupError));
      final backend = _backend(channel);

      await backend.connect();

      expect(backend.isLoading, isFalse);
      expect(backend.error, _startupError);
      // Retrying would only re-run the same failure.
      expect(channel.connectAttempts, 1);

      backend.dispose();
    });

    test('reaches the boot screen', () async {
      final backend = _backend(
          _FailingChannel(const FletAppStartupException(_startupError)));

      await backend.connect();

      // The boot screen renders `bootStatus.error`; leaving it null is what
      // used to leave the page blank for the whole life of the app.
      expect(backend.bootStatus.value.error, contains(_startupError));
      expect(backend.bootStatus.value.done, isFalse);

      backend.dispose();
    });

    test('is reported to an embedding FletApp', () async {
      final errorsHandler = FletAppErrorsHandler();
      final backend = _backend(
          _FailingChannel(const FletAppStartupException(_startupError)),
          errorsHandler: errorsHandler);

      await backend.connect();

      expect(errorsHandler.error, _startupError);

      backend.dispose();
    });
  });

  group('a plain connect failure', () {
    test('still reconnects, and keeps the error for the give-up path',
        () async {
      final channel = _FailingChannel(Exception("connection refused"));
      final backend = _backend(channel);

      await backend.connect();

      // Still in the reconnect loop: loading, nothing shown to the user yet.
      expect(backend.isLoading, isTrue);
      expect(backend.bootStatus.value.error, isNull);
      // The real error survives the reconnect, instead of being overwritten
      // with a status string and then reported in place of the actual cause.
      expect(backend.error, contains("connection refused"));

      backend.dispose();
    });
  });
}
