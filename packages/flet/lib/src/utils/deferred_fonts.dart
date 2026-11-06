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
  DeferredFonts(
      {AssetBundle? bundle,
      FontFamilyLoader? loadFamily,
      bool? web,
      DateTime Function()? now})
      : _bundle = bundle ?? rootBundle,
        _loadFamily = loadFamily ?? _loadWithFontLoader,
        _web = web ?? kIsWeb,
        _now = now ?? DateTime.now;

  static DeferredFonts instance = DeferredFonts();

  /// The wait before retrying a package whose fonts failed to load,
  /// doubling with each failure in a row up to [maxRetryDelay].
  static const firstRetryDelay = Duration(seconds: 5);
  static const maxRetryDelay = Duration(minutes: 5);

  final AssetBundle _bundle;
  final FontFamilyLoader _loadFamily;
  final bool _web;
  final DateTime Function() _now;
  final _packages = <String, Future<void>>{};
  final _loadedFamilies = <String>{};
  final _failures = <String, int>{};
  final _retryAt = <String, DateTime>{};
  Future<List<Map<String, dynamic>>>? _deferred;

  /// Loads the deferred fonts of Dart package [package], once. Does nothing
  /// outside the web, or when the package's fonts are in `FontManifest.json`
  /// (`flet debug` and web builds made before Flet 1.1.2).
  ///
  /// A failed load is retried by a later call, after [firstRetryDelay],
  /// doubling up to [maxRetryDelay]: callers run on every build (each Lucide
  /// icon, shadcn control and formula), so without a wait an app that is
  /// offline, or misses a font file, would request it on every frame.
  Future<void> load(String package) {
    if (!_web) return Future.value();
    final loading = _packages[package];
    if (loading != null) return loading;
    final retryAt = _retryAt[package];
    if (retryAt != null && _now().isBefore(retryAt)) return Future.value();
    return _packages[package] = _load(package).then((_) {
      _failures.remove(package);
      _retryAt.remove(package);
    }).catchError((Object error) {
      // Controls don't await this call: keep failures handled, and let a
      // later build retry once connectivity recovers.
      _packages.remove(package);
      final failures = (_failures[package] ?? 0) + 1;
      _failures[package] = failures;
      final delay = firstRetryDelay * (1 << (failures - 1).clamp(0, 16));
      _retryAt[package] =
          _now().add(delay > maxRetryDelay ? maxRetryDelay : delay);
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
