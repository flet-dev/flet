import 'dart:typed_data';

import 'package:flet/src/services/file_storage_space.dart';
import 'package:flutter_test/flutter_test.dart';

/// What every `ft.FileStorage` backend must do, run against a real one.
void fileStorageBackendContract(FileStorageBackend Function() create) {
  late FileStorageBackend b;
  final root = ["flet", "contract-${DateTime.now().microsecondsSinceEpoch}"];
  List<String> at(String name) => [...root, ...name.split("/")];
  Uint8List bytes(String s) => Uint8List.fromList(s.codeUnits);

  setUp(() => b = create());

  test("a missing file reads as null and deletes as false", () async {
    expect(await b.read(at("nope.bin")), isNull);
    expect(await b.delete(at("nope.bin")), isFalse);
    expect(await b.list(at("no-such-folder")), isEmpty);
  });

  test("writes, replaces, reads, lists and deletes", () async {
    await b.write(at("db/app.sqlite"), bytes("first"));
    await b.write(at("db/app.sqlite"), bytes("second, longer"));
    await b.write(at("notes.txt"), bytes("hi"));
    expect(String.fromCharCodes((await b.read(at("db/app.sqlite")))!),
        "second, longer");
    expect(await b.list(root), {"db/app.sqlite": 14, "notes.txt": 2});
    expect(await b.delete(at("notes.txt")), isTrue);
    expect(await b.list(root), {"db/app.sqlite": 14});
    await b.delete(at("db/app.sqlite"));
  });

  test("an empty file is a file", () async {
    await b.write(at("empty"), Uint8List(0));
    expect(await b.read(at("empty")), isEmpty);
    expect(await b.list(root), {"empty": 0});
    await b.delete(at("empty"));
  });

  test("a lock is exclusive until unlocked", () async {
    final name = "${root.join("/")}/lock";
    expect(await b.lock(name, const Duration(milliseconds: 200)), isTrue);
    expect(await b.lock(name, Duration.zero), isFalse);
    expect(await b.lock(name, const Duration(milliseconds: 100)), isFalse);
    final waiting = b.lock(name, const Duration(seconds: 2));
    b.unlock(name);
    expect(await waiting, isTrue);
    b.unlock(name);
    expect(await b.lock(name, Duration.zero), isTrue);
    b.unlock(name);
  });
}
