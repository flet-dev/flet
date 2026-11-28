/// An app's `ft.SharedPreferences` only ever reaches keys under its
/// [FletBackend.storagePrefix]: an embedded app can't
/// read, list or clear its host's keys.
library;

import 'package:flet/flet.dart';
import 'package:flet/src/services/shared_preferences.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  late SharedPreferences prefs;

  setUp(() async {
    SharedPreferences.setMockInitialValues({
      "settings.theme": "host-value",
      "app.1.todo": "guest one",
      "app.12.todo": "guest twelve",
    });
    prefs = await SharedPreferences.getInstance();
  });

  Future<dynamic> call(String prefix, String name, [Map? args]) =>
      invokeSharedPreferencesMethod(prefs, prefix, name, args ?? {});

  test("get and contains_key see only the app's own keys", () async {
    expect(await call("app.1.", "get", {"key": "todo"}), "guest one");
    expect(await call("app.1.", "get", {"key": "settings.theme"}), isNull);
    expect(await call("app.1.", "contains_key", {"key": "settings.theme"}),
        isFalse);
  });

  test("set and remove write under the prefix", () async {
    await call("app.1.", "set", {"key": "settings.theme", "value": "x"});
    expect(prefs.getString("settings.theme"), "host-value");
    expect(prefs.getString("app.1.settings.theme"), "x");
    await call("app.1.", "remove", {"key": "settings.theme"});
    expect(prefs.getString("settings.theme"), "host-value");
    expect(prefs.containsKey("app.1.settings.theme"), isFalse);
  });

  test("get_keys lists own keys without the prefix", () async {
    expect(await call("app.1.", "get_keys", {"key_prefix": ""}), ["todo"]);
    // `app.1.` must not match `app.12.`'s keys.
    expect(await call("app.1", "get_keys", {"key_prefix": ""}),
        containsAll([".todo", "2.todo"]));
  });

  test("clear removes only the app's own keys", () async {
    expect(await call("app.1.", "clear"), isTrue);
    expect(prefs.getKeys(), {"settings.theme", "app.12.todo"});
  });

  test("an empty prefix is the plain store", () async {
    expect(await call("", "get", {"key": "settings.theme"}), "host-value");
    expect(
        (await call("", "get_keys", {"key_prefix": "app."}) as List).length, 2);
    await call("", "clear");
    expect(prefs.getKeys(), isEmpty);
  });

  group("resolveStoragePrefix", () {
    final uri = Uri.parse("https://example.com/app");

    test("top-level takes the given prefix", () {
      expect(
          FletBackend.resolveStoragePrefix(
              storagePrefix: "app.1.", pageUri: uri),
          "app.1.");
    });

    test("top-level without one is empty off the web", () {
      expect(FletBackend.resolveStoragePrefix(pageUri: uri), "");
    });

    test("embedded nests under the host's prefix", () {
      expect(
          FletBackend.resolveStoragePrefix(
              storagePrefix: "x.", parentPrefix: "app.1.", pageUri: uri),
          "app.1.x.");
    });

    test("embedded without one is isolated by a hash of its URL", () {
      final prefix =
          FletBackend.resolveStoragePrefix(parentPrefix: "", pageUri: uri);
      expect(prefix, matches(RegExp(r"^fletapp\.[0-9a-f]{8}\.$")));
      expect(prefix, FletBackend.defaultEmbeddedStoragePrefix(uri.toString()));
      expect(
          prefix,
          isNot(FletBackend.defaultEmbeddedStoragePrefix(
              "https://example.com/other")));
    });

    test("embedded with an empty prefix shares the host's space", () {
      expect(
          FletBackend.resolveStoragePrefix(
              storagePrefix: "", parentPrefix: "app.1.", pageUri: uri),
          "app.1.");
    });

    test("the default hash is FNV-1a 32-bit", () {
      // Known FNV-1a values, so web and native agree.
      expect(FletBackend.defaultEmbeddedStoragePrefix(""), "fletapp.811c9dc5.");
      expect(
          FletBackend.defaultEmbeddedStoragePrefix("a"), "fletapp.e40c292c.");
      expect(FletBackend.defaultEmbeddedStoragePrefix("foobar"),
          "fletapp.bf9cf968.");
    });
  });

  group("quota", () {
    Future<dynamic> set(String prefix, String key, Object value, int quota) =>
        invokeSharedPreferencesMethod(
            prefs, prefix, "set", {"key": key, "value": value},
            quota: quota);

    test("a set past it fails and stores nothing", () async {
      // "app.1.todo" + "\"guest one\"" already takes 21 bytes.
      await expectLater(
          set("app.1.", "big", "x" * 100, 100), throwsA(isA<StateError>()));
      expect(prefs.containsKey("app.1.big"), isFalse);
      await set("app.1.", "small", "x" * 50, 100);
      expect(prefs.getString("app.1.small"), "x" * 50);
    });

    test("replacing a value counts only the new one", () async {
      await set("app.1.", "todo", "y" * 70, 100);
      await set("app.1.", "todo", "z" * 75, 100);
      expect(prefs.getString("app.1.todo"), "z" * 75);
    });

    test("other prefixes' keys don't count", () async {
      await set("app.12.", "note", "x" * 50, 100);
    });

    test("nested clients respect outer limits", () async {
      FletBackend app(String prefix, int quota, [FletBackend? parent]) =>
          FletBackend(
              pageUri: Uri.parse("mock"),
              assetsDir: "",
              multiView: false,
              extensions: [],
              parentFletBackend: parent,
              storagePrefix: prefix,
              fileStorageQuota: quota,
              sharedPreferencesQuota: quota);
      final root = app("app.1.", 50);
      final shared = app("", 100, root);
      final child = app("child.", 100, shared);
      expect(shared.fileStorageQuota, 50);
      expect(shared.sharedPreferencesQuota, 50);
      expect(child.fileStorageQuota, 100);
      expect(child.ancestorPreferenceQuotas, {"app.1.": 50});
      await expectLater(
          invokeSharedPreferencesMethod(prefs, child.storagePrefix, "set",
              {"key": "data", "value": "x" * 30},
              quota: child.sharedPreferencesQuota,
              ancestorQuotas: child.ancestorPreferenceQuotas),
          throwsStateError);
    });

    test("checks persisted values even with a stale tab cache", () async {
      final oldCache = prefs;
      SharedPreferences.setMockInitialValues({"app.1.external": "x" * 80});
      expect(oldCache.containsKey("app.1.external"), isFalse);
      await expectLater(
          invokeSharedPreferencesMethod(
              oldCache, "app.1.", "set", {"key": "new", "value": "x" * 20},
              quota: 100),
          throwsStateError);
    }, skip: !kIsWeb);

    test("concurrent clients share a single preference quota", () async {
      SharedPreferences.setMockInitialValues({});
      final first = await SharedPreferences.getInstance();
      SharedPreferences.setMockInitialValues({});
      final second = await SharedPreferences.getInstance();
      Future<bool> write(SharedPreferences cache, String key) async {
        try {
          await invokeSharedPreferencesMethod(
              cache, "app.", "set", {"key": key, "value": "x" * 55},
              quota: 100);
          return true;
        } on StateError {
          return false;
        }
      }

      final results =
          await Future.wait([write(first, "a"), write(second, "b")]);
      expect(results.where((ok) => ok), hasLength(1));
      await first.reload();
      expect(first.getKeys(), hasLength(1));
    }, skip: !kIsWeb);

    test("no quota, no limit", () async {
      await invokeSharedPreferencesMethod(
          prefs, "app.1.", "set", {"key": "big", "value": "x" * 100000});
      expect(prefs.getString("app.1.big")!.length, 100000);
    });
  });
}
