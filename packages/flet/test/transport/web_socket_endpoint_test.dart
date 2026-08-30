import 'package:flutter/foundation.dart';

import 'package:flet/src/transport/flet_backend_channel.dart';
import 'package:flet/src/transport/flet_backend_channel_web_socket.dart';
import 'package:flutter_test/flutter_test.dart';

/// Endpoint composition for the embedded branch, plus the factory plumbing
/// that selects it. These hold on every platform.
///
/// The embedded-vs-root *difference* is only observable on web — on io both
/// branches derive the path from the URL — so the regression test for the fix
/// itself lives in `web_socket_endpoint_web_test.dart`, which runs under
/// `flutter test --platform chrome`.
void main() {
  String endpoint(String url, {required bool embedded}) =>
      FletWebSocketBackendChannel(
              address: url,
              embedded: embedded,
              onDisconnect: () {},
              onPacket: (_) {})
          .getWebSocketEndpoint(Uri.parse(url));

  group("getWebSocketEndpoint (embedded)", () {
    // An embedded app derives its WebSocket path from its own URL, so a
    // path-prefixed URL (e.g. behind a reverse proxy on a gateway host)
    // keeps its prefix instead of inheriting the host document's endpoint.
    test("path-prefixed URL keeps its prefix", () {
      expect(endpoint("https://gateway/device1/", embedded: true),
          "wss://gateway/device1/ws");
    });

    test("root URL on a dedicated port resolves to /ws", () {
      expect(
          endpoint("http://host:9001/", embedded: true), "ws://host:9001/ws");
    });

    test("http maps to ws, https maps to wss", () {
      expect(endpoint("http://gateway/device1/", embedded: true),
          startsWith("ws://"));
      expect(endpoint("https://gateway/device1/", embedded: true),
          startsWith("wss://"));
    });

    test("URL without trailing slash and nested paths keep their prefix", () {
      expect(endpoint("https://gateway/device1", embedded: true),
          "wss://gateway/device1/ws");
      expect(endpoint("https://gateway/a/b/", embedded: true),
          "wss://gateway/a/b/ws");
    });
  });

  group("getWebSocketEndpoint (root, io)", () {
    // On io the platform implementation derives the path from the URL too, so
    // desktop and mobile are unaffected by the embedded flag either way. This
    // is a VM-only claim: on web the root branch reads the host document's
    // configuration instead (see web_socket_endpoint_web_test.dart).
    test("root branch derives from the URL path", () {
      expect(endpoint("https://gateway/device1/", embedded: false),
          "wss://gateway/device1/ws");
      expect(
          endpoint("http://host:9001/", embedded: false), "ws://host:9001/ws");
    });
  },
      skip: kIsWeb
          ? "io-only: on web the root branch reads the host config"
          : null);

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
