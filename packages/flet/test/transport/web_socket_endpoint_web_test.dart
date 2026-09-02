@TestOn("browser")
library;

import 'package:flet/src/transport/flet_backend_channel_web_socket.dart';
import 'package:flutter_test/flutter_test.dart';

/// Regression test for the embedded-app WebSocket endpoint on web.
///
/// This is the only platform where the embedded and root branches differ: the
/// root branch reads `window.flet.webSocketEndpoint`, which describes the host
/// document and is shared by every app embedded on the page, while an embedded
/// app must derive its path from its own URL. On io both branches derive from
/// the URL, so a VM test cannot tell them apart.
///
/// `window.flet` is undefined under the test harness, so the root branch falls
/// back to the bare `"ws"` endpoint — which is exactly the value a
/// path-prefixed embedded app used to get, and never connected on.
///
/// Run with: `flutter test --platform chrome`
void main() {
  String endpoint(String url, {required bool embedded}) =>
      FletWebSocketBackendChannel(
              address: url,
              embedded: embedded,
              onDisconnect: () {},
              onPacket: (_) {})
          .getWebSocketEndpoint(Uri.parse(url));

  test("embedded app derives its endpoint from its own URL", () {
    expect(endpoint("https://gateway/device1/", embedded: true),
        "wss://gateway/device1/ws");
    expect(endpoint("https://gateway/a/b/", embedded: true),
        "wss://gateway/a/b/ws");
  });

  test("root app reads the host document's endpoint, ignoring the URL path",
      () {
    expect(endpoint("https://gateway/device1/", embedded: false),
        "wss://gateway/ws");
  });
}
