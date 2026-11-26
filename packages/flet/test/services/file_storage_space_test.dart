/// `ft.FileStorage`'s rules, on an in-memory backend: an app reaches only its
/// own folder, names are checked the same way everywhere, quotas hold, and
/// locks are released with the app.
library;

import 'dart:typed_data';

import 'package:flet/src/services/file_storage_space.dart';
import 'package:flutter_test/flutter_test.dart';

class _MemoryBackend implements FileStorageBackend {
  final files = <String, Uint8List>{};
  final locks = <String>{};

  @override
  Future<Uint8List?> read(List<String> path) async => files[path.join("/")];

  @override
  Future<void> write(List<String> path, Uint8List data) async =>
      files[path.join("/")] = data;

  @override
  Future<bool> delete(List<String> path) async =>
      files.remove(path.join("/")) != null;

  @override
  Future<Map<String, int>> list(List<String> folder) async {
    final prefix = "${folder.join("/")}/";
    return {
      for (final e in files.entries)
        if (e.key.startsWith(prefix)) e.key.substring(prefix.length): e.value.length,
    };
  }

  @override
  Future<bool> lock(String name, Duration timeout) async => locks.add(name);

  @override
  void unlock(String name) => locks.remove(name);
}

void main() {
  late _MemoryBackend backend;
  setUp(() => backend = _MemoryBackend());

  FileStorageSpace space(String prefix, {int? quota}) =>
      FileStorageSpace(backend, prefix, quota: quota);
  Uint8List bytes(int n) => Uint8List(n);

  group("names", () {
    test("plain and nested names are fine", () {
      expect(fileStorageSegments("app.sqlite"), ["app.sqlite"]);
      expect(fileStorageSegments("db/2026/app.sqlite"), ["db", "2026", "app.sqlite"]);
      expect(fileStorageSegments(".hidden"), [".hidden"]);
    });

    test("names that could leave the app's folder are refused", () {
      for (final name in [
        "",
        "/abs",
        "a//b",
        "a/",
        ".",
        "..",
        "../host.txt",
        "a/../../b",
        "a\\b",
        "c:file",
        "a\u0000b",
        "what?",
        "trailing.",
        "trailing ",
        "x.flet-tmp",
        "a/" * 20 + "b",
        "x" * 300,
      ]) {
        expect(() => fileStorageSegments(name),
            throwsA(isA<FileStorageNameError>()), reason: name);
      }
    });
  });

  group("folders", () {
    test("a top-level app and embedded apps never share one", () {
      expect(fileStorageFolder(""), "root");
      expect(fileStorageFolder("app.abc."), "p.app.abc.");
      expect(fileStorageFolder("root"), "p.root");
      expect(fileStorageFolder("a/b."), "p.a%2Fb.");
      expect(fileStorageFolder("x~(1)"), "p.x%7E%281%29");
      expect(fileStorageFolder("app.1."), isNot(fileStorageFolder("app.1.x.")));
    });

    test("each app sees only its own files", () async {
      final host = space("");
      final guest = space("app.1.");
      await host.invoke("write", {"name": "secret.txt", "data": bytes(3)});
      await guest.invoke("write", {"name": "notes.txt", "data": bytes(2)});
      expect(await guest.invoke("read", {"name": "secret.txt"}), isNull);
      expect(await guest.invoke("exists", {"name": "secret.txt"}), isFalse);
      expect(await guest.invoke("list", {}), ["notes.txt"]);
      expect(await guest.invoke("delete", {"name": "secret.txt"}), isFalse);
      expect(await host.invoke("list", {}), ["secret.txt"]);
      expect(backend.files.keys,
          {"flet/root/secret.txt", "flet/p.app.1./notes.txt"});
    });
  });

  test("write takes bytes or a list of ints", () async {
    final s = space("app.1.");
    await s.invoke("write", {"name": "a", "data": Uint8List.fromList([1, 2])});
    await s.invoke("write", {"name": "b", "data": [3, 4, 5]});
    expect(await s.invoke("read", {"name": "b"}), [3, 4, 5]);
    expect(() => s.invoke("write", {"name": "c", "data": "text"}),
        throwsArgumentError);
  });

  test("list filters by prefix and sorts; size adds up", () async {
    final s = space("app.1.");
    for (final n in ["b/2", "a", "b/1", "c"]) {
      await s.invoke("write", {"name": n, "data": bytes(10)});
    }
    expect(await s.invoke("list", {}), ["a", "b/1", "b/2", "c"]);
    expect(await s.invoke("list", {"prefix": "b/"}), ["b/1", "b/2"]);
    expect(await s.invoke("size", {}), 40);
  });

  group("quota", () {
    test("a write past it fails and changes nothing", () async {
      final s = space("app.1.", quota: 100);
      await s.invoke("write", {"name": "a", "data": bytes(60)});
      await expectLater(s.invoke("write", {"name": "b", "data": bytes(41)}),
          throwsA(isA<FileStorageQuotaError>()));
      expect(await s.invoke("list", {}), ["a"]);
      await s.invoke("write", {"name": "b", "data": bytes(40)});
    });

    test("replacing a file counts only the difference", () async {
      final s = space("app.1.", quota: 100);
      await s.invoke("write", {"name": "db", "data": bytes(90)});
      await s.invoke("write", {"name": "db", "data": bytes(100)});
      expect(await s.invoke("size", {}), 100);
    });

    test("another app's files don't count", () async {
      await space("").invoke("write", {"name": "big", "data": bytes(500)});
      await space("app.1.", quota: 100)
          .invoke("write", {"name": "a", "data": bytes(100)});
    });
  });

  group("locks", () {
    test("are scoped to the app's folder and reentrant", () async {
      final a = space("app.1.");
      final b = space("app.2.");
      expect(await a.invoke("lock", {"name": "db"}), isTrue);
      expect(await a.invoke("lock", {"name": "db"}), isTrue);
      expect(await b.invoke("lock", {"name": "db"}), isTrue);
      expect(backend.locks,
          {"flet.file_storage/p.app.1./db", "flet.file_storage/p.app.2./db"});
      await a.invoke("unlock", {"name": "db"});
      expect(backend.locks, {"flet.file_storage/p.app.2./db"});
    });

    test("an app can't release a lock it doesn't hold", () async {
      await space("app.1.").invoke("lock", {"name": "db"});
      await space("app.1.").invoke("unlock", {"name": "db"});
      expect(backend.locks, {"flet.file_storage/p.app.1./db"});
    });

    test("go away with the app", () async {
      final s = space("app.1.");
      await s.invoke("lock", {"name": "a"});
      await s.invoke("lock", {"name": "b"});
      s.releaseLocks();
      expect(backend.locks, isEmpty);
    });

    test("names are checked too", () async {
      expect(() => space("app.1.").invoke("lock", {"name": "../x"}),
          throwsA(isA<FileStorageNameError>()));
    });
  });
}
