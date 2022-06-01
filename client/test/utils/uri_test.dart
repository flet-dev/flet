import 'package:flet_view/utils/uri.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("Empty URI can be parsed", () {
    var uri = Uri.parse("");
    expect(uri.hasAuthority, false);
  });
  test("Relative URI can be parsed", () {
    var uri = Uri.parse("images/test.png");
    expect(uri.hasAuthority, false);
  });

  test("getWebPageName returns correct name from Uri", () {
    expect(
        getWebPageName(Uri.parse('http://localhost:8550/p/test/')), "p/test");
    expect(getWebPageName(Uri.parse('http://localhost:8550/p/test')), "p/test");
    expect(getWebPageName(Uri.parse('http://localhost:8550/')), "");
    expect(getWebPageName(Uri.parse('http://localhost:8550/#/')), "");
  });

  test("getWebSocketEndpoint returns correct URL", () {
    expect(getWebSocketEndpoint(Uri.parse('http://localhost:8550/p/test/')),
        "ws://localhost:8550/ws");
    expect(getWebSocketEndpoint(Uri.parse('http://localhost')),
        "ws://localhost/ws");
    expect(getWebSocketEndpoint(Uri.parse('https://app.flet.dev/')),
        "wss://app.flet.dev/ws");
  });
}
