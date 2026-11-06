import 'dart:typed_data';

import 'package:flet/src/utils/box.dart';
import 'package:flet/src/utils/images.dart';
import 'package:flet/src/utils/images_web.dart' as web;
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group("ResolvedAssetSource byte buffers", () {
    test("full-buffer sources retain their identity", () {
      final bytes = Uint8List.fromList([1, 2, 3]);

      expect(ResolvedAssetSource.from(bytes).bytes, same(bytes));
    });

    final views = <String, Uint8List Function()>{
      "offset view": () =>
          Uint8List.sublistView(Uint8List.fromList([99, 1, 2, 3, 88]), 1, 4),
      "zero-offset truncated view": () =>
          Uint8List.sublistView(Uint8List.fromList([1, 2, 3, 88]), 0, 3),
      "view ending at the buffer boundary": () =>
          Uint8List.sublistView(Uint8List.fromList([99, 1, 2, 3]), 1),
    };

    for (final entry in views.entries) {
      test("${entry.key} gets a stable, independent buffer", () {
        final source = entry.value();
        final bytes = ResolvedAssetSource.from(source).bytes!;

        expect(bytes, [1, 2, 3]);
        expect(bytes.offsetInBytes, 0);
        expect(bytes.buffer.lengthInBytes, bytes.lengthInBytes);
        expect(identical(bytes.buffer, source.buffer), isFalse);
        expect(ResolvedAssetSource.from(source).bytes, same(bytes));
      });
    }

    test("replacing a source resolves the new bytes", () {
      final first = Uint8List.sublistView(Uint8List.fromList([99, 1, 2]), 1);
      final next = Uint8List.sublistView(Uint8List.fromList([99, 3, 4]), 1);

      final firstBytes = ResolvedAssetSource.from(first).bytes!;
      final nextBytes = ResolvedAssetSource.from(next).bytes!;

      expect(nextBytes, [3, 4]);
      expect(nextBytes, isNot(same(firstBytes)));
      expect(ResolvedAssetSource.from(next).bytes, same(nextBytes));
    });

    test("direct conversions still read current data for clipboard writes", () {
      final source = Uint8List.sublistView(Uint8List.fromList([99, 1, 2]), 1);
      final assetBytes = ResolvedAssetSource.from(source).bytes!;
      final firstWrite = convertToUint8List(source)!;
      source[0] = 3;
      final nextWrite = convertToUint8List(source)!;

      expect(assetBytes, [1, 2]);
      expect(firstWrite, [1, 2]);
      expect(nextWrite, [3, 2]);
    });

    testWidgets("image and decoration providers keep their keys on rebuild",
        (tester) async {
      final source = Uint8List.sublistView(Uint8List.fromList([99, 1, 2]), 1);
      final images = <ImageProvider>[];
      final providers = <ImageProvider>[];
      final decorations = <ImageProvider>[];

      Widget build(double width) => Builder(builder: (context) {
            final image = buildImage(
              context: context,
              errorCtrl: null,
              src: source,
              width: width,
            ) as Image;
            images.add(image.image);
            providers.add(parseImageProvider(source, context)!);
            decorations
                .add(parseDecorationImage({"src": source}, context)!.image);
            return const SizedBox();
          });

      await tester.pumpWidget(build(100));
      await tester.pumpWidget(build(200));

      expect(images[1], images[0]);
      expect(providers[1], providers[0]);
      expect(decorations[1], decorations[0]);
      expect(providers[0], images[0]);
      expect(decorations[0], images[0]);
    });
  });

  group("getAssetSrc (web) — URL scheme pass-through", () {
    final pageUri = Uri.parse("http://localhost:8550/");
    const assetsDir = "/assets";

    test("http URLs pass through", () {
      expect(
          web.getAssetSrc("http://example.com/a.png", pageUri, assetsDir).path,
          "http://example.com/a.png");
    });

    test("https URLs pass through", () {
      expect(
          web.getAssetSrc("https://example.com/a.png", pageUri, assetsDir).path,
          "https://example.com/a.png");
    });

    test("data URLs pass through", () {
      expect(
          web
              .getAssetSrc("data:image/png;base64,iVBO", pageUri, assetsDir)
              .path,
          "data:image/png;base64,iVBO");
    });

    test("blob URLs pass through", () {
      expect(web.getAssetSrc("blob:http://x/abc", pageUri, assetsDir).path,
          "blob:http://x/abc");
    });

    test("rtsp URLs pass through (media_kit streaming)", () {
      expect(
          web.getAssetSrc("rtsp://cam.local/stream", pageUri, assetsDir).path,
          "rtsp://cam.local/stream");
    });

    test("rtmp URLs pass through", () {
      expect(
          web.getAssetSrc("rtmp://x/y", pageUri, assetsDir).path, "rtmp://x/y");
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
