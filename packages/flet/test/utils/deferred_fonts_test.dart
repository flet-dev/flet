import 'dart:async';
import 'dart:convert';

import 'package:flet/src/utils/deferred_fonts.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

class _Bundle extends CachingAssetBundle {
  _Bundle(this.files);

  final Map<String, String> files;
  final loaded = <String>[];
  final pending = <String, Completer<ByteData>>{};

  @override
  Future<ByteData> load(String key) async {
    loaded.add(key);
    if (pending.containsKey(key)) return pending[key]!.future;
    final text = files[key];
    if (text == null) throw Exception("404 $key");
    return ByteData.sublistView(utf8.encode(text));
  }
}

Map<String, dynamic> _family(String name, List<String> assets) => {
      "family": name,
      "fonts": [
        for (final a in assets) {"asset": a}
      ],
    };

final _katex = _family("packages/flutter_math_fork/KaTeX_Main", [
  "packages/flutter_math_fork/fonts/KaTeX_Main-Regular.ttf",
  "packages/flutter_math_fork/fonts/KaTeX_Main-Bold.ttf",
]);
final _lucide = _family("packages/lucide_icons_flutter/Lucide",
    ["packages/lucide_icons_flutter/assets/lucide.ttf"]);
final _material = _family("MaterialIcons", ["fonts/MaterialIcons-Regular.otf"]);

void main() {
  late Map<String, List<String>> loadedFamilies;

  Future<void> loadFamily(String family, List<Future<ByteData>> fonts) async {
    final bytes = await Future.wait(fonts);
    loadedFamilies[family] = [
      for (final b in bytes) utf8.decode(b.buffer.asUint8List())
    ];
  }

  // A fake clock for the wait before a retry.
  late DateTime time;
  DateTime now() => time;
  void waitForRetry([int failures = 1]) =>
      time = time.add(DeferredFonts.firstRetryDelay * (1 << (failures - 1)));

  setUp(() {
    loadedFamilies = {};
    time = DateTime(2026, 11, 6, 12);
  });

  _Bundle bundle({List? fontManifest, List? deferred}) => _Bundle({
        "FontManifest.json": jsonEncode(fontManifest ?? [_material]),
        if (deferred != null) deferredFontManifest: jsonEncode(deferred),
        for (final f in [_katex, _lucide])
          for (final font in f["fonts"])
            font["asset"]: "bytes of ${font["asset"]}",
      });

  test("loads only the requested package's deferred families, once", () async {
    final b = bundle(deferred: [_katex, _lucide]);
    final fonts = DeferredFonts(bundle: b, loadFamily: loadFamily, web: true);

    await Future.wait([
      fonts.load("flutter_math_fork"),
      fonts.load("flutter_math_fork"),
    ]);
    await fonts.load("flutter_math_fork");

    expect(loadedFamilies.keys, ["packages/flutter_math_fork/KaTeX_Main"]);
    expect(loadedFamilies.values.single, [
      "bytes of packages/flutter_math_fork/fonts/KaTeX_Main-Regular.ttf",
      "bytes of packages/flutter_math_fork/fonts/KaTeX_Main-Bold.ttf",
    ]);
    expect(b.loaded.where((k) => k == deferredFontManifest).length, 1);

    await fonts.load("lucide_icons_flutter");
    expect(
        loadedFamilies.keys, contains("packages/lucide_icons_flutter/Lucide"));
    // The deferred manifest is read once for all packages.
    expect(b.loaded.where((k) => k == deferredFontManifest).length, 1);
  });

  test("does nothing when the fonts are in FontManifest.json", () async {
    // `flet debug` and web builds made before 1.1.2.
    final b = bundle(fontManifest: [_material, _katex]);
    final fonts = DeferredFonts(bundle: b, loadFamily: loadFamily, web: true);

    await fonts.load("flutter_math_fork");

    expect(loadedFamilies, isEmpty);
    expect(b.loaded, isNot(contains(deferredFontManifest)));
  });

  test("a missing deferred manifest or font doesn't throw", () async {
    final noManifest =
        DeferredFonts(bundle: bundle(), loadFamily: loadFamily, web: true);
    await noManifest.load("flutter_math_fork");
    expect(loadedFamilies, isEmpty);

    final missingFont = DeferredFonts(
        bundle: bundle(deferred: [
          _family(
              "packages/shadcn_ui/Geist", ["packages/shadcn_ui/missing.ttf"])
        ]),
        loadFamily: loadFamily,
        web: true);
    await missingFont.load("shadcn_ui");
    expect(loadedFamilies, isEmpty);
  });

  test("retries a failed deferred manifest for all packages", () async {
    final b = bundle();
    final fonts =
        DeferredFonts(bundle: b, loadFamily: loadFamily, web: true, now: now);

    await Future.wait([
      fonts.load("flutter_math_fork"),
      fonts.load("lucide_icons_flutter"),
    ]);
    expect(loadedFamilies, isEmpty);

    b.files[deferredFontManifest] = jsonEncode([_katex, _lucide]);
    waitForRetry();
    await Future.wait([
      fonts.load("flutter_math_fork"),
      fonts.load("lucide_icons_flutter"),
    ]);

    expect(loadedFamilies.keys,
        containsAll([_katex["family"], _lucide["family"]]));
    expect(b.loaded.where((k) => k == deferredFontManifest).length, 2);
  });

  test("retries a failed startup manifest", () async {
    final b = bundle(deferred: [_katex])..files.remove("FontManifest.json");
    final fonts =
        DeferredFonts(bundle: b, loadFamily: loadFamily, web: true, now: now);

    await fonts.load("flutter_math_fork");
    expect(loadedFamilies, isEmpty);
    expect(b.loaded, isNot(contains(deferredFontManifest)));

    b.files["FontManifest.json"] = jsonEncode([_material]);
    waitForRetry();
    await fonts.load("flutter_math_fork");

    expect(loadedFamilies.keys, [_katex["family"]]);
    expect(b.loaded.where((k) => k == "FontManifest.json").length, 2);
  });

  test("retries failed families without loading successful ones again",
      () async {
    const asset = "packages/flutter_math_fork/fonts/KaTeX_Math-Italic.ttf";
    final math = _family("packages/flutter_math_fork/KaTeX_Math", [asset]);
    final b = bundle(deferred: [_katex, math]);
    final fonts =
        DeferredFonts(bundle: b, loadFamily: loadFamily, web: true, now: now);

    await fonts.load("flutter_math_fork");
    expect(loadedFamilies.keys, [_katex["family"]]);

    b.files[asset] = "math";
    waitForRetry();
    await Future.wait([
      fonts.load("flutter_math_fork"),
      fonts.load("flutter_math_fork"),
    ]);
    await fonts.load("flutter_math_fork");

    expect(loadedFamilies[math["family"]], ["math"]);
    expect(b.loaded.where((k) => k == asset).length, 2);
    for (final font in _katex["fonts"]) {
      expect(b.loaded.where((k) => k == font["asset"]).length, 1);
    }
    expect(b.loaded.where((k) => k == deferredFontManifest).length, 1);
  });

  test("waits longer after each failure in a row, and resets on success",
      () async {
    // Callers run on every build: an offline app mustn't request the font
    // on every frame.
    const asset = "packages/lucide_icons_flutter/assets/lucide.ttf";
    final b = bundle(deferred: [_lucide])..files.remove(asset);
    final fonts =
        DeferredFonts(bundle: b, loadFamily: loadFamily, web: true, now: now);
    int requests() => b.loaded.where((k) => k == asset).length;

    await fonts.load("lucide_icons_flutter");
    expect(requests(), 1);
    // Rebuilds within the wait don't request it again.
    for (var i = 0; i < 10; i++) {
      await fonts.load("lucide_icons_flutter");
    }
    expect(requests(), 1);

    // 5 s, then 10 s, then 20 s, ...
    for (var failures = 1; failures <= 3; failures++) {
      time = time.add(DeferredFonts.firstRetryDelay * (1 << (failures - 1)) -
          const Duration(milliseconds: 1));
      await fonts.load("lucide_icons_flutter");
      expect(requests(), failures, reason: "still waiting after $failures");
      time = time.add(const Duration(milliseconds: 1));
      await fonts.load("lucide_icons_flutter");
      expect(requests(), failures + 1, reason: "retried after $failures");
    }

    // ... up to 5 minutes.
    for (var i = 0; i < 20; i++) {
      time = time.add(DeferredFonts.maxRetryDelay);
      await fonts.load("lucide_icons_flutter");
    }
    expect(requests(), 4 + 20);

    // Back online: it loads, and stays loaded.
    b.files[asset] = "lucide";
    time = time.add(DeferredFonts.maxRetryDelay);
    await fonts.load("lucide_icons_flutter");
    expect(loadedFamilies[_lucide["family"]], ["lucide"]);
    await fonts.load("lucide_icons_flutter");
    expect(requests(), 4 + 20 + 1);
  });

  test("catches later font failures while an earlier font is pending",
      () async {
    final b = bundle(deferred: [_katex]);
    final first = Completer<ByteData>();
    final second = Completer<ByteData>();
    b.pending[_katex["fonts"][0]["asset"]] = first;
    b.pending[_katex["fonts"][1]["asset"]] = second;
    // Use the real FontLoader: a Future.wait mock hides its sequential awaits.
    final fonts = DeferredFonts(bundle: b, web: true);
    final loading = fonts.load("flutter_math_fork");
    await Future<void>.delayed(Duration.zero);
    expect(b.loaded, containsAll(b.pending.keys));

    second.completeError(Exception("bold download failed"));
    await Future<void>.delayed(Duration.zero);
    first.completeError(Exception("regular download failed"));
    await loading;
  });

  test("decodes the manifest's URL-encoded paths for the asset bundle",
      () async {
    // The bundle encodes its key itself; an encoded key would be encoded
    // twice and miss the file (`Geist%5Bwght%5D.ttf` on disk).
    final b = _Bundle({
      "FontManifest.json": "[]",
      deferredFontManifest: jsonEncode([
        _family("packages/shadcn_ui/Geist",
            ["packages/shadcn_ui/fonts/Geist%5Bwght%5D.ttf"])
      ]),
      "packages/shadcn_ui/fonts/Geist[wght].ttf": "geist",
    });

    await DeferredFonts(bundle: b, loadFamily: loadFamily, web: true)
        .load("shadcn_ui");

    expect(loadedFamilies, {
      "packages/shadcn_ui/Geist": ["geist"]
    });
  });

  test("does nothing outside the web", () async {
    final b = bundle(deferred: [_katex]);
    await DeferredFonts(bundle: b, loadFamily: loadFamily, web: false)
        .load("flutter_math_fork");

    expect(loadedFamilies, isEmpty);
    expect(b.loaded, isEmpty);
  });
}
