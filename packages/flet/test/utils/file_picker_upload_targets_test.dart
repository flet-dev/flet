import 'package:file_picker/file_picker.dart';
import 'package:flet/src/utils/file_picker.dart';
import 'package:flutter_test/flutter_test.dart';

FilePickerUploadFile upload(int? id, String name) => FilePickerUploadFile(
    id: id, name: name, uploadUrl: "https://x/$name", method: "PUT");

void main() {
  final picked = [
    PlatformFile(name: "a.png", size: 1),
    PlatformFile(name: "b.png", size: 1),
    PlatformFile(name: "c.png", size: 1),
  ];

  test("each upload gets its own file when several are uploaded at once", () {
    final targets = resolveUploadTargets(
        [upload(0, "a.png"), upload(1, "b.png"), upload(2, "c.png")], picked);
    expect(targets.map((t) => t.$2?.name), ["a.png", "b.png", "c.png"]);
  });

  test("falls back to the name, and reports a missing file as null", () {
    final targets = resolveUploadTargets(
        [upload(null, "c.png"), upload(7, "zzz.png")], picked);
    expect(targets.map((t) => t.$2?.name), ["c.png", null]);
  });
}
