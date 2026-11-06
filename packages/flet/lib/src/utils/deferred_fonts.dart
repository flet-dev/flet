import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

/// Where `flet build web` lists the fonts it moved out of
/// `FontManifest.json`, in the same format.
const deferredFontManifest = "DeferredFontManifest.json";

typedef FontFamilyLoader = Future<void> Function(
    String family, List<Future<ByteData>> fonts);

/// Loads the fonts of a Dart package on first use, in a web app.
///
/// Flutter web downloads every font in `FontManifest.json` before the first
/// frame. `flet build web` moves the fonts that only some controls need
/// (math in `Markdown`, flet-shadcn-ui's icons and text) to
/// [deferredFontManifest]; a control calls [loadDeferredFonts] with the
/// package that brings them before it draws. Text that used a font before it
/// arrived redraws by itself once it's loaded.
class DeferredFonts {
  DeferredFonts({AssetBundle? bundle, FontFamilyLoader? loadFamily, bool? web})
      : _bundle = bundle ?? rootBundle,
        _loadFamily = loadFamily ?? _loadWithFontLoader,
        _web = web ?? kIsWeb;

  static DeferredFonts instance = DeferredFonts();

  final AssetBundle _bundle;
  final FontFamilyLoader _loadFamily;
  final bool _web;
  final _packages = <String, Future<void>>{};
  final _loadedFamilies = <String>{};
  Future<List<Map<String, dynamic>>>? _deferred;

  /// Loads the deferred fonts of Dart package [package], once. Does nothing
  /// outside the web, or when the package's fonts are in `FontManifest.json`
  /// (`flet debug` and web builds made before Flet 1.1.2).
  /// Failed downloads are retried on the next call.
  Future<void> load(String package) {
    if (!_web) return Future.value();
    return _packages[package] ??= _load(package).catchError((Object error) {
      // Controls need not await this call. Keep failures handled, but allow
      // the next control build to retry after connectivity recovers.
      _packages.remove(package);
      debugPrint("Error loading deferred fonts for $package: $error");
    });
  }

  Future<void> _load(String package) async {
    final prefix = "packages/$package/";
    bool ofPackage(Map<String, dynamic> f) =>
        (f["family"] as String? ?? "").startsWith(prefix);

    // Fetched by the engine at startup, so usually from the browser's cache.
    if ((await _readManifest("FontManifest.json")).any(ofPackage)) return;
    final families =
        (await (_deferred ??= _readDeferredManifest())).where(ofPackage);
    await Future.wait(families.map((f) async {
      final family = f["family"] as String;
      if (_loadedFamilies.contains(family)) return;
      await _loadFamily(family, [
        for (final font in (f["fonts"] as List? ?? const []))
          // The manifest has the path URL-encoded (`Geist%5Bwght%5D.ttf`,
          // a file of that name) and the asset bundle encodes its key
          // again: decoded, the request is the engine's for the font.
          _bundle.load(Uri.decodeFull(font["asset"] as String))
      ]);
      // Other families may have failed. Retain successful registrations so
      // retrying the package doesn't register these families a second time.
      _loadedFamilies.add(family);
    }));
  }

  Future<List<Map<String, dynamic>>> _readDeferredManifest() async {
    try {
      return await _readManifest(deferredFontManifest);
    } catch (_) {
      _deferred = null;
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> _readManifest(String name) async {
    try {
      final json = jsonDecode(await _bundle.loadString(name));
      return (json as List).cast<Map<String, dynamic>>();
    } catch (_) {
      // CachingAssetBundle also caches failed loadString futures.
      _bundle.evict(name);
      rethrow;
    }
  }

  static Future<void> _loadWithFontLoader(
      String family, List<Future<ByteData>> fonts) async {
    // FontLoader awaits its futures sequentially. Handle every download now
    // so a later failure cannot escape while an earlier font is pending.
    final bytes = await Future.wait(fonts);
    final loader = FontLoader(family);
    for (final font in bytes) {
      loader.addFont(Future.value(font));
    }
    return loader.load();
  }
}

/// Loads the fonts of Dart package [package] that `flet build web` deferred.
/// See [DeferredFonts].
Future<void> loadDeferredFonts(String package) =>
    DeferredFonts.instance.load(package);
