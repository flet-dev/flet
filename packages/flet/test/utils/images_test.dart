import 'package:flet/src/utils/images_web.dart' as web;
import 'package:flutter_test/flutter_test.dart';

void main() {
  group("getAssetSrc (web) — URL scheme pass-through", () {
    final pageUri = Uri.parse("http://localhost:8550/");
    const assetsDir = "/assets";

    test("http URLs pass through", () {
      expect(web.getAssetSrc("http://example.com/a.png", pageUri, assetsDir).path,
          "http://example.com/a.png");
    });

    test("https URLs pass through", () {
      expect(
          web.getAssetSrc("https://example.com/a.png", pageUri, assetsDir).path,
          "https://example.com/a.png");
    });

    test("data URLs pass through", () {
      expect(web.getAssetSrc("data:image/png;base64,iVBO", pageUri, assetsDir).path,
          "data:image/png;base64,iVBO");
    });

    test("blob URLs pass through", () {
      expect(web.getAssetSrc("blob:http://x/abc", pageUri, assetsDir).path,
          "blob:http://x/abc");
    });

    test("rtsp URLs pass through (media_kit streaming)", () {
      expect(web.getAssetSrc("rtsp://cam.local/stream", pageUri, assetsDir).path,
          "rtsp://cam.local/stream");
    });

    test("rtmp URLs pass through", () {
      expect(web.getAssetSrc("rtmp://x/y", pageUri, assetsDir).path, "rtmp://x/y");
    });

    test("srt URLs pass through", () {
      expect(web.getAssetSrc("srt://x:1234", pageUri, assetsDir).path,
          "srt://x:1234");
    });

    test("udp URLs pass through", () {
      expect(web.getAssetSrc("udp://239.0.0.1:5000", pageUri, assetsDir).path,
          "udp://239.0.0.1:5000");
    });

    test("file URLs pass through", () {
      expect(web.getAssetSrc("file:///tmp/x.mp4", pageUri, assetsDir).path,
          "file:///tmp/x.mp4");
    });

    test("relative paths are resolved against assetsDir", () {
      expect(web.getAssetSrc("images/a.png", pageUri, assetsDir).path,
          "/assets/images/a.png");
    });

    test("leading-slash relative paths are resolved against assetsDir", () {
      expect(web.getAssetSrc("/images/a.png", pageUri, assetsDir).path,
          "/assets/images/a.png");
    });
  });
}
