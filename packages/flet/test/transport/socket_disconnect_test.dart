@TestOn('vm')
library;

import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flet/src/transport/flet_backend_channel_socket.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';

/// Aborts [socket] with a TCP reset (RST) instead of an orderly FIN.
///
/// This is how Windows closes the connection of a terminated process that
/// still holds unread data, e.g. a Python app killed by a `flet run` hot
/// reload. `SO_LINGER` with a zero timeout makes the close abortive.
void _reset(Socket socket) {
  final soLinger = Platform.isLinux ? 13 : 0x0080;
  final linger = Platform.isWindows
      ? (ByteData(4)
        ..setUint16(0, 1, Endian.host)
        ..setUint16(2, 0, Endian.host))
      : (ByteData(8)
        ..setInt32(0, 1, Endian.host)
        ..setInt32(4, 0, Endian.host));
  socket.setRawOption(RawSocketOption(
      RawSocketOption.levelSocket, soLinger, linger.buffer.asUint8List()));
  socket.destroy();
}

/// Collects `debugPrint` output while [body] runs.
Future<List<String>> _capturePrints(Future<void> Function() body) async {
  final lines = <String>[];
  final original = debugPrint;
  debugPrint = (String? message, {int? wrapWidth}) {
    if (message != null) lines.add(message);
  };
  try {
    await body();
  } finally {
    debugPrint = original;
  }
  return lines;
}

void main() {
  group('FletSocketBackendChannel', () {
    late ServerSocket server;

    setUp(() async {
      server = await ServerSocket.bind(InternetAddress.loopbackIPv4, 0);
    });

    tearDown(() async {
      await server.close();
    });

    /// Connects a channel, lets [close] end the accepted server-side socket
    /// once the client is connected, and returns how many times the channel
    /// reported a disconnect.
    Future<int> disconnectsAfter(void Function(Socket socket) close,
        {List<String>? prints}) async {
      final accepted = Completer<Socket>();
      server.listen(accepted.complete);
      var disconnects = 0;
      final channel = FletSocketBackendChannel(
          address: "tcp://127.0.0.1:${server.port}",
          onDisconnect: () => disconnects++,
          onPacket: (_) {});
      final lines = await _capturePrints(() async {
        await channel.connect();
        close(await accepted.future);
        await Future.delayed(const Duration(milliseconds: 300));
      });
      prints?.addAll(lines);
      channel.disconnect();
      return disconnects;
    }

    test('reports a connection reset as a single disconnect', () async {
      final prints = <String>[];
      final disconnects = await disconnectsAfter(_reset, prints: prints);

      // The reset reaches the channel as a socket error, not a plain close.
      expect(prints, contains(startsWith("Error: ")));
      expect(disconnects, 1);
    });

    test('reports an orderly close as a single disconnect', () async {
      final disconnects = await disconnectsAfter((socket) => socket.destroy());

      expect(disconnects, 1);
    });
  });

  group('FletBackend over a TCP socket', () {
    test('reconnects once after a connection reset', () async {
      final server = await ServerSocket.bind(InternetAddress.loopbackIPv4, 0);
      var connections = 0;
      Socket? active;
      server.listen((socket) {
        connections++;
        final isFirst = connections == 1;
        // Like FletSocketServer, a new client replaces the active one.
        active?.destroy();
        active = socket;
        socket.listen((_) {
          // Reset the first connection once its client has registered.
          if (isFirst && identical(active, socket)) {
            active = null;
            _reset(socket);
          }
        }, onError: (_) {});
      });

      // A reset also fails the client socket's `done` future, which nothing
      // listens to; keep those errors out of the test zone.
      final otherErrors = <Object>[];
      late FletBackend backend;
      await _capturePrints(() async {
        final connected = Completer<void>();
        runZonedGuarded(() {
          backend = FletBackend(
              pageUri: Uri.parse("tcp://127.0.0.1:${server.port}"),
              assetsDir: "",
              extensions: [],
              multiView: false,
              reconnectIntervalMs: 50);
          backend.connect().whenComplete(connected.complete);
        }, (error, stack) {
          if (error is! SocketException) otherErrors.add(error);
        });
        await connected.future;
        await Future.delayed(const Duration(seconds: 1));
      });

      // The reset connection plus exactly one reconnect. Two overlapping
      // reconnects keep replacing each other on the server, so the count
      // would keep growing for as long as the client runs.
      expect(connections, 2);
      expect(otherErrors, isEmpty);

      await server.close();
      backend.dispose();
      active?.destroy();
    });
  });
}
