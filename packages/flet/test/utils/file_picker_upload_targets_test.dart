import 'dart:typed_data';

import 'package:cross_file/cross_file.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flet/src/utils/file_picker.dart';
import 'package:flutter_test/flutter_test.dart';

/// A picked file for the tests (file_picker's PlatformFile is abstract).
final class _File extends PlatformFile {
  _File(this.name, this.size);

  @override
  final String name;
  final int size;

  @override
  Uri get uri => Uri.file("/tmp/$name");

  @override
  XFile get xFile => XFile(uri.toFilePath());

  @override
  int? lengthSync() => size;

  @override
  Future<int?> length() async => size;

  @override
  Future<Uint8List> readAsBytes() async => Uint8List(size);

  @override
  Stream<Uint8List> readAsByteStream() => Stream.value(Uint8List(size));
}

FilePickerUploadFile upload(int? id, String? name) => FilePickerUploadFile(
    id: id, name: name, uploadUrl: "https://x/$name", method: "PUT");

void main() {
  late Map<int, PlatformFile> picked;

  setUp(() {
    picked = {
      0: _File("a.png", 1),
      1: _File("b.png", 1),
      2: _File("c.png", 1),
    };
  });

  test("each upload gets its own file when several are uploaded at once", () {
    final targets = takeUploadTargets(
        [upload(0, "a.png"), upload(1, "b.png"), upload(2, "c.png")], picked);
    expect(targets.map((t) => t.$2?.name), ["a.png", "b.png", "c.png"]);
    expect(picked, isEmpty);
  });

  test("original IDs remain valid across separate upload calls", () {
    final first = takeUploadTargets([upload(0, "a.png")], picked);
    final second = takeUploadTargets([upload(1, "b.png")], picked);
    final third = takeUploadTargets([upload(2, null)], picked);

    expect(first.single.$2?.name, "a.png");
    expect(second.single.$2?.name, "b.png");
    expect(third.single.$2?.name, "c.png");
  });

  test("out-of-order and name-based uploads preserve remaining IDs", () {
    takeUploadTargets([upload(null, "b.png")], picked);
    expect(picked.keys, [0, 2]);
    final targets =
        takeUploadTargets([upload(2, null), upload(0, null)], picked);
    expect(targets.map((t) => t.$2?.name), ["c.png", "a.png"]);
  });

  test("falls back to the name, and reports missing files as null", () {
    final targets = takeUploadTargets([
      upload(null, "c.png"),
      upload(7, "b.png"),
      upload(7, "zzz.png"),
      upload(null, null),
    ], picked);
    expect(targets.map((t) => t.$2?.name), ["c.png", "b.png", null, null]);
  });

  test("a consumed ID never resolves to a different remaining file", () {
    takeUploadTargets([upload(0, "a.png")], picked);
    final targets = takeUploadTargets([upload(0, "a.png")], picked);
    expect(targets.single.$2, isNull);
    expect(picked.keys, [1, 2]);
  });

  test("reserves streams against duplicate and overlapping uploads", () {
    final first =
        takeUploadTargets([upload(0, "a.png"), upload(0, "a.png")], picked);
    // A second call can arrive before the first upload finishes or fails.
    final overlapping = takeUploadTargets([upload(0, "a.png")], picked);
    expect(first.map((t) => t.$2?.name), ["a.png", null]);
    expect(overlapping.single.$2, isNull);
  });

  test("IDs distinguish files with the same name", () {
    final a = _File("same.png", 1);
    final b = _File("same.png", 2);
    picked = {0: a, 1: b};
    expect(
        takeUploadTargets([upload(1, "same.png")], picked).single.$2, same(b));
    expect(
        takeUploadTargets([upload(0, "same.png")], picked).single.$2, same(a));
  });
}
