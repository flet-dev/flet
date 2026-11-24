import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;

/// In-memory transport: lets the test inject inbound protocol messages.
class _FakeChannel implements FletBackendChannel {
  late FletBackendChannelOnPacketCallback _onPacket;

  FletBackendChannelBuilder get builder => ({
        required FletBackendChannelOnPacketCallback onPacket,
        required FletBackendChannelOnDisconnectCallback onDisconnect,
      }) {
        _onPacket = onPacket;
        return this;
      };

  void deliver(MessageAction action, dynamic payload) {
    final encoded = msgpack.serialize(
        Message(action: action, payload: payload).toList(),
        extEncoder: FletMsgpackEncoder());
    final packet = Uint8List(1 + encoded.length)
      ..[0] = 0x00
      ..setRange(1, 1 + encoded.length, encoded);
    _onPacket(packet);
  }

  // An update for a control id this client doesn't have: it still counts as
  // UI traffic (the idle timer restarts before the control lookup), without
  // building a real control tree. FletBackend logs it as dropped.
  void patch() => deliver(MessageAction.patchControl, {"id": 999, "patch": []});

  @override
  Future connect() async {}

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 300000;

  @override
  void send(Uint8List packet) {}

  @override
  void disconnect() {}
}

FletBackend _root() => FletBackend(
    pageUri: Uri.parse("mock"),
    assetsDir: "",
    extensions: [],
    multiView: false);

({FletBackend backend, _FakeChannel channel, FletAppErrorsHandler errors})
    _embedded(FletBackend parent) {
  final channel = _FakeChannel();
  final errors = FletAppErrorsHandler();
  final backend = FletBackend(
      pageUri: Uri.parse("mock"),
      assetsDir: "",
      extensions: [],
      multiView: false,
      channelBuilder: channel.builder,
      errorsHandler: errors,
      controlId: 7,
      parentFletBackend: parent);
  // ignore: unawaited_futures
  backend.connect();
  return (backend: backend, channel: channel, errors: errors);
}

void main() {
  testWidgets('resolves idle only after an update and a quiet period',
      (tester) async {
    final parent = _root();
    final app = _embedded(parent);
    await tester.pump();

    Map<String, dynamic>? result;
    app.backend
        .waitIdle(idleMs: 300, timeoutMs: 10000)
        .then((r) => result = r);

    // No UI update yet (main() may still be awaiting something): not idle.
    await tester.pump(const Duration(milliseconds: 1000));
    expect(result, isNull);

    app.channel.patch();
    await tester.pump(const Duration(milliseconds: 200));
    app.channel.patch(); // restarts the quiet period
    await tester.pump(const Duration(milliseconds: 200));
    expect(result, isNull);

    await tester.pump(const Duration(milliseconds: 150)); // quiet > 300 ms
    await tester.pump(); // the frame that shows the last update
    expect(result, {"status": "idle", "error": null});

    app.backend.dispose();
    parent.dispose();
  });

  testWidgets('a crash resolves error and reaches the host', (tester) async {
    final parent = _root();
    final app = _embedded(parent);
    await tester.pump();

    Map<String, dynamic>? result;
    app.backend.waitIdle(timeoutMs: 10000).then((r) => result = r);
    app.channel.deliver(
        MessageAction.sessionCrashed, {"message": "ZeroDivisionError"});
    await tester.pump();

    expect(result, {"status": "error", "error": "ZeroDivisionError"});
    // FletApp.on_error fires on the host through the errors handler.
    expect(app.errors.error, "ZeroDivisionError");

    app.backend.dispose();
    parent.dispose();
  });

  testWidgets('an app that keeps updating times out', (tester) async {
    final parent = _root();
    final app = _embedded(parent);
    await tester.pump();

    Map<String, dynamic>? result;
    app.backend
        .waitIdle(idleMs: 300, timeoutMs: 2000)
        .then((r) => result = r);
    for (var i = 0; i < 20; i++) {
      app.channel.patch();
      await tester.pump(const Duration(milliseconds: 100));
    }
    expect(result, {"status": "timeout", "error": null});

    app.backend.dispose();
    parent.dispose();
  });

  testWidgets('a new wait supersedes a pending one', (tester) async {
    final parent = _root();
    final app = _embedded(parent);
    await tester.pump();

    Map<String, dynamic>? first;
    Map<String, dynamic>? second;
    app.backend.waitIdle(timeoutMs: 10000).then((r) => first = r);
    app.backend.waitIdle(idleMs: 100, timeoutMs: 10000).then((r) => second = r);
    await tester.pump();
    expect(first?["status"], "timeout");

    app.channel.patch();
    await tester.pump(const Duration(milliseconds: 150));
    await tester.pump();
    expect(second?["status"], "idle");

    app.backend.dispose();
    parent.dispose();
  });

  testWidgets('disposing the embedded app resolves a pending wait',
      (tester) async {
    final parent = _root();
    final app = _embedded(parent);
    await tester.pump();

    Map<String, dynamic>? result;
    app.backend.waitIdle(timeoutMs: 10000).then((r) => result = r);
    app.backend.dispose();
    await tester.pump();
    expect(result?["status"], "error");

    parent.dispose();
  });

  test('a root backend refuses: wait_idle is for embedded apps only',
      () async {
    final root = _root();
    final result = await root.waitIdle();
    expect(result["status"], "error");
    root.dispose();
  });
}
