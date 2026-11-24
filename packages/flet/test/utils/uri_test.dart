import 'package:flet/src/utils/uri.dart';
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
    expect(getWebPageName(Uri.parse('http://localhost:8550/aaa')), "aaa");
    expect(getWebPageName(Uri.parse('http://localhost:8550/p/test/store')),
        "p/test");
    expect(
        getWebPageName(
            Uri.parse('http://localhost:8550/p/test/store/products/1')),
        "p/test");
    expect(getWebPageName(Uri.parse('http://localhost:8550/')), "");
    expect(getWebPageName(Uri.parse('http://localhost:8550/#/')), "");
  });
  group("getAssetUri — path separator (regression for #5198 / #5350)", () {
    // Before 0.28.3 this function concatenated `pageUri.path + assetPath`
    // with no separator, so a non-empty page name silently corrupted every
    // relative asset URL: "/src/main.py" + "images/113.png" produced
    // "/src/main.pyimages/113.png", which 404s. Mobile clients hit it because
    // they connect to a dev server with an empty assetsDir and therefore
    // resolve every `src` through this function.
    final pageUri = Uri.parse("http://localhost:8550/src/main.py");

    test("inserts a separator between page name and nested asset", () {
      expect(getAssetUri(pageUri, "images/113.png").toString(),
          "http://localhost:8550/src/main.py/images/113.png");
    });

    test("never concatenates page name and asset without a separator", () {
      expect(getAssetUri(pageUri, "images/113.png").toString(),
          isNot(contains("main.pyimages")));
    });

    test("inserts a separator before a top-level asset", () {
      expect(getAssetUri(pageUri, "icon.png").toString(),
          "http://localhost:8550/src/main.py/icon.png");
    });

    test("preserves deeply nested asset paths", () {
      expect(getAssetUri(pageUri, "a/b/c/d.png").toString(),
          "http://localhost:8550/src/main.py/a/b/c/d.png");
    });

    test("works with a single-segment page name", () {
      expect(
          getAssetUri(Uri.parse("http://localhost:8550/aaa"), "images/113.png")
              .toString(),
          "http://localhost:8550/aaa/images/113.png");
    });

    test("works with an empty page name", () {
      expect(
          getAssetUri(Uri.parse("http://localhost:8550/"), "images/113.png")
              .toString(),
          "http://localhost:8550/images/113.png");
      expect(
          getAssetUri(Uri.parse("http://localhost:8550"), "images/113.png")
              .toString(),
          "http://localhost:8550/images/113.png");
    });
  });

  group("getAssetUri — origin handling", () {
    test("preserves scheme, host and port", () {
      expect(
          getAssetUri(Uri.parse("https://example.com:9000/app"), "a.png")
              .toString(),
          "https://example.com:9000/app/a.png");
    });

    test("omits the port when it is the scheme default", () {
      expect(getAssetUri(Uri.parse("https://example.com/app"), "a.png").toString(),
          "https://example.com/app/a.png");
    });

    test("does not carry the page query onto the asset URL", () {
      expect(
          getAssetUri(Uri.parse("http://localhost:8550/src/main.py?x=1"), "a.png")
              .toString(),
          "http://localhost:8550/src/main.py/a.png");
    });

    test("does not carry the page fragment onto the asset URL", () {
      expect(
          getAssetUri(Uri.parse("http://localhost:8550/src/main.py#frag"), "a.png")
              .toString(),
          "http://localhost:8550/src/main.py/a.png");
    });
  });

  group("getAssetUri — percent-encoding", () {
    final pageUri = Uri.parse("http://localhost:8550/src/main.py");

    test("encodes spaces in asset names", () {
      expect(getAssetUri(pageUri, "images/a b.png").toString(),
          "http://localhost:8550/src/main.py/images/a%20b.png");
    });

    test("encodes non-ASCII asset names", () {
      expect(getAssetUri(pageUri, "images/ü.png").toString(),
          "http://localhost:8550/src/main.py/images/%C3%BC.png");
    });
  });

  // These pin down behaviour that is currently WRONG or surprising but that
  // no released client depends on being fixed. They exist so a future change
  // to `getAssetUri` is a deliberate decision rather than a silent one - if
  // one of these starts failing, the fix is probably correct and the
  // expectation should be updated, not the code reverted.
  group("getAssetUri — known rough edges (characterization)", () {
    final pageUri = Uri.parse("http://localhost:8550/src/main.py");

    test("an absolute asset src yields a double slash", () {
      // The 0.28.3 fix dropped the old leading-slash strip. Starlette
      // normalizes "//" away, so this resolves today, but a stricter proxy
      // or CDN would not.
      expect(getAssetUri(pageUri, "/images/113.png").toString(),
          "http://localhost:8550/src/main.py//images/113.png");
    });

    test("a trailing slash on the page URI yields a double slash", () {
      expect(
          getAssetUri(
                  Uri.parse("http://localhost:8550/src/main.py/"), "images/113.png")
              .toString(),
          "http://localhost:8550/src/main.py//images/113.png");
    });

    test("a query string in the asset src is encoded into the path", () {
      // Cache-busting suffixes like "?v=2" do not survive: the "?" becomes
      // %3F and the request 404s.
      expect(getAssetUri(pageUri, "images/113.png?v=2").toString(),
          "http://localhost:8550/src/main.py/images/113.png%3Fv=2");
    });

    test("a Windows separator in the asset src is encoded, not normalized", () {
      // The file branch of getAssetSrc calls normalizePath; this network
      // branch does not, so a backslash survives as %5C and 404s.
      expect(getAssetUri(pageUri, r"images\113.png").toString(),
          "http://localhost:8550/src/main.py/images%5C113.png");
    });
  });

  test("getWebsocketEndpointPathFromUriPath derives path from URL path", () {
    expect(getWebsocketEndpointPathFromUriPath(""), "ws");
    expect(getWebsocketEndpointPathFromUriPath("/"), "ws");
    expect(getWebsocketEndpointPathFromUriPath("/sub1"), "sub1/ws");
    expect(getWebsocketEndpointPathFromUriPath("/sub1/"), "sub1/ws");
    expect(getWebsocketEndpointPathFromUriPath("sub1"), "sub1/ws");
    expect(getWebsocketEndpointPathFromUriPath("/a/b/"), "a/b/ws");
  });
}
