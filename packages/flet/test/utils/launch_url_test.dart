import 'package:flet/src/utils/launch_url.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group("webUrlScheme", () {
    test("reads the scheme in lower case", () {
      expect(webUrlScheme("https://flet.dev"), "https");
      expect(webUrlScheme("JavaScript:void(0)"), "javascript");
      expect(webUrlScheme("mailto:hi@example.com"), "mailto");
      expect(webUrlScheme("my-app+v2.x:open"), "my-app+v2.x");
    });

    test("ignores what a browser ignores before reading it", () {
      expect(webUrlScheme("  javascript:void(0)"), "javascript");
      expect(webUrlScheme("\u0000\u001fjavascript:void(0)"), "javascript");
      expect(webUrlScheme("java\tscr\nipt\r:void(0)"), "javascript");
    });

    test("is null for a relative URL", () {
      expect(webUrlScheme("/docs"), isNull);
      expect(webUrlScheme("docs/page.html"), isNull);
      expect(webUrlScheme("?q=1"), isNull);
      expect(webUrlScheme(""), isNull);
    });
  });

  group("isOpenableWebUrl", () {
    test("refuses javascript:, blob: and filesystem: URLs on web only", () {
      for (final url in [
        "javascript:alert(1)",
        " JAVA\tSCRIPT:alert(1)",
        "blob:https://example.com/0b1c",
        "filesystem:https://example.com/temporary/a.html",
      ]) {
        expect(isOpenableWebUrl(url), !kIsWeb, reason: url);
      }
    });

    test("opens everything else", () {
      for (final url in [
        "https://flet.dev",
        "http://localhost:8550/",
        "mailto:hi@example.com",
        "tel:+15551234567",
        "data:text/html,<b>hi</b>",
        "my-app://open",
        "/relative/path",
      ]) {
        expect(isOpenableWebUrl(url), isTrue, reason: url);
      }
    });
  });

  group("launchTarget", () {
    test("an embedded app can't target the page it's in, on web", () {
      for (final target in ["_self", "_parent", "_top"]) {
        expect(launchTarget(target, true), kIsWeb ? "_blank" : target);
      }
    });

    test("other targets, and top-level apps, are unchanged", () {
      expect(launchTarget("_blank", true), "_blank");
      expect(launchTarget("docs", true), "docs");
      expect(launchTarget(null, true), isNull);
      expect(launchTarget("_self", false), "_self");
    });
  });

  group("popupWindowName", () {
    test("defaults to Flet and keeps a plain name", () {
      expect(popupWindowName(null), "Flet");
      expect(popupWindowName("Sign in"), "Sign in");
    });

    test("never names a target keyword", () {
      expect(popupWindowName("_self"), "flet_self");
      expect(popupWindowName("_top"), "flet_top");
      expect(popupWindowName("_blank"), "flet_blank");
    });
  });
}
