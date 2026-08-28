import 'package:flet/src/transport/flet_backend_channel.dart';
import 'package:flet/src/transport/flet_backend_channel_web_socket.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  FletWebSocketBackendChannel channel({required bool embedded}) =>
      FletWebSocketBackendChannel(
          address: "https://gateway/device1/",
          embedded: embedded,
          onDisconnect: () {},
          onPacket: (_) {});

  group("getWebSocketEndpoint (embedded)", () {
    // An embedded app derives its WebSocket path from its own URL, so a
    // path-prefixed URL (e.g. behind a reverse proxy on a gateway host)
    // keeps its prefix instead of inheriting the host document's endpoint.
    test("path-prefixed URL keeps its prefix", () {
      expect(
          channel(embedded: true)
              .getWebSocketEndpoint(Uri.parse("https://gateway/device1/")),
          "wss://gateway/device1/ws");
    });

    test("root URL on a dedicated port resolves to /ws", () {
      expect(
          channel(embedded: true)
              .getWebSocketEndpoint(Uri.parse("http://host:9001/")),
          "ws://host:9001/ws");
    });

    test("http maps to ws, https maps to wss", () {
      final c = channel(embedded: true);
      expect(c.getWebSocketEndpoint(Uri.parse("http://gateway/device1/")),
          startsWith("ws://"));
      expect(c.getWebSocketEndpoint(Uri.parse("https://gateway/device1/")),
          startsWith("wss://"));
    });

    test("URL without trailing slash and nested paths keep their prefix", () {
      final c = channel(embedded: true);
      expect(c.getWebSocketEndpoint(Uri.parse("https://gateway/device1")),
          "wss://gateway/device1/ws");
      expect(c.getWebSocketEndpoint(Uri.parse("https://gateway/a/b/")),
          "wss://gateway/a/b/ws");
    });
  });

  group("getWebSocketEndpoint (root)", () {
    // On io the platform implementation already derives the path from the
    // URL, so both branches must agree there — this guards the claim that
    // the root branch is unchanged by the embedded fix.
    test("root branch is unchanged (io derives from the URL path)", () {
      final c = channel(embedded: false);
      expect(c.getWebSocketEndpoint(Uri.parse("https://gateway/device1/")),
          "wss://gateway/device1/ws");
      expect(c.getWebSocketEndpoint(Uri.parse("http://host:9001/")),
          "ws://host:9001/ws");
    });
  });

  group("FletBackendChannel factory", () {
    test("forwards the embedded flag to the WebSocket channel", () {
      final ch = FletBackendChannel(
          address: "https://gateway/device1/",
          args: {},
          forcePyodide: false,
          embedded: true,
          onDisconnect: () {},
          onPacket: (_) {});
      expect(ch, isA<FletWebSocketBackendChannel>());
      expect((ch as FletWebSocketBackendChannel).embedded, true);
    });

    test("defaults to non-embedded", () {
      final ch = FletBackendChannel(
          address: "https://gateway/",
          args: {},
          forcePyodide: false,
          onDisconnect: () {},
          onPacket: (_) {});
      expect((ch as FletWebSocketBackendChannel).embedded, false);
    });
  });
}
