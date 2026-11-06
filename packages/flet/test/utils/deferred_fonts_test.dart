import 'dart:convert';

import 'package:flet/src/utils/deferred_fonts.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

class _Bundle extends CachingAssetBundle {
  _Bundle(this.files);

  final Map<String, String> files;
  final loaded = <String>[];

  @override
  Future<ByteData> load(String key) async {
    loaded.add(key);
    final text = files[key];
    if (text == null) throw Exception("404 $key");
    return ByteData.sublistView(utf8.encode(text));
  }

  @override
  Future<String> loadString(String key, {bool cache = true}) async =>
      utf8.decode((await load(key)).buffer.asUint8List());
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
final _material =
    _family("MaterialIcons", ["fonts/MaterialIcons-Regular.otf"]);

void main() {
  late Map<String, List<String>> loadedFamilies;

  Future<void> loadFamily(String family, List<Future<ByteData>> fonts) async {
    final bytes = await Future.wait(fonts);
    loadedFamilies[family] = [
      for (final b in bytes) utf8.decode(b.buffer.asUint8List())
    ];
  }

  setUp(() => loadedFamilies = {});

  _Bundle bundle({List? fontManifest, List? deferred}) => _Bundle({
        "FontManifest.json": jsonEncode(fontManifest ?? [_material]),
        if (deferred != null) deferredFontManifest: jsonEncode(deferred),
        for (final f in [_katex, _lucide])
          for (final font in f["fonts"]) font["asset"]: "bytes of ${font["asset"]}",
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
    expect(loadedFamilies.keys, contains("packages/lucide_icons_flutter/Lucide"));
    // The deferred manifest is read once for all packages.
    expect(b.loaded.where((k) => k == deferredFontManifest).length, 1);
  });

  test("does nothing when the fonts are in FontManifest.json", () async {
    // `flet debug`, `flet run --web` and builds before 1.1.2.
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
          _family("packages/shadcn_ui/Geist", ["packages/shadcn_ui/missing.ttf"])
        ]),
        loadFamily: loadFamily,
        web: true);
    await missingFont.load("shadcn_ui");
    expect(loadedFamilies, isEmpty);
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
