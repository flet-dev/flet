import 'dart:convert';
import 'dart:typed_data';

import 'package:crypto/crypto.dart';

/// Where `ft.FileStorage` keeps an app's files: OPFS on web, the app support
/// directory elsewhere. Paths are lists of already-validated segments.
abstract class FileStorageBackend {
  /// The file's bytes, or `null` if there's no such file.
  Future<Uint8List?> read(List<String> path);

  /// Replaces the file atomically: a reader sees the old bytes or the new
  /// ones, never a mix. Creates parent folders.
  Future<void> write(List<String> path, Uint8List data);

  /// Serializes mutations of a folder across clients, including quota accounting.
  Future<T> mutate<T>(String folder, Future<T> Function() action);

  /// Whether a file was removed.
  Future<bool> delete(List<String> path);

  /// Every file under [folder], by its path relative to [folder] (segments
  /// joined with `/`), with its size in bytes.
  Future<Map<String, int>> list(List<String> folder);

  /// Takes the exclusive lock called [name] (shared by every app instance
  /// using the same backend: on web, every tab of the origin). Waits up to
  /// [timeout]; `false` if it couldn't. [Duration.zero] doesn't wait.
  Future<bool> lock(String name, Duration timeout);

  /// Releases a lock taken with [lock].
  void unlock(String name);
}

/// A name couldn't be used as a file name in `ft.FileStorage`.
class FileStorageNameError implements Exception {
  final String message;
  FileStorageNameError(this.message);
  @override
  String toString() => message;
}

/// A write would take the app past its storage quota.
class FileStorageQuotaError implements Exception {
  final String message;
  FileStorageQuotaError(this.message);
  @override
  String toString() => message;
}

/// Reserved suffix for native temporary files and the OPFS staging entry.
const fileStorageTempSuffix = ".flet-tmp";

const _maxNameLength = 1024;
const _maxSegmentLength = 255;
const _maxDepth = 16;
final _forbidden = RegExp(r'[\\:*?"<>|\x00-\x1f\x7f]');

/// The segments of a file [name] an app passed, or a [FileStorageNameError].
///
/// The same rules on every platform, so a name that works in a web preview
/// works in the built app: segments separated by `/`; none empty, `.` or
/// `..`; none with `\ : * ? " < > |` or control characters; none ending with
/// [fileStorageTempSuffix] or with a space or dot (Windows drops those).
List<String> fileStorageSegments(String name) {
  if (name.isEmpty) throw FileStorageNameError("File name is empty.");
  if (name.length > _maxNameLength) {
    throw FileStorageNameError(
        "File name is longer than $_maxNameLength characters.");
  }
  var segments = name.split("/");
  if (segments.length > _maxDepth) {
    throw FileStorageNameError(
        "File name has more than $_maxDepth folders: $name");
  }
  for (var s in segments) {
    if (s.isEmpty || s == "." || s == "..") {
      throw FileStorageNameError(
          "File name can't have an empty, \".\" or \"..\" part: $name");
    }
    if (s.length > _maxSegmentLength ||
        _forbidden.hasMatch(s) ||
        s.endsWith(" ") ||
        s.endsWith(".") ||
        s.endsWith(fileStorageTempSuffix)) {
      throw FileStorageNameError("Not a valid file name: $name");
    }
  }
  return segments;
}

/// A bounded, case-stable directory name even on case-insensitive filesystems.
String fileStorageFolder(String prefix) =>
    prefix.isEmpty ? "root" : "p-${sha256.convert(utf8.encode(prefix))}";

/// One app's space in `ft.FileStorage`: its own folder, an optional quota
/// and the locks it holds. Runs the service's methods.
class FileStorageSpace {
  final FileStorageBackend backend;
  final String folder;

  /// Most bytes the app may keep, or `null` for no limit.
  final int? quota;

  final Set<String> _held = {};
  bool _disposed = false;

  FileStorageSpace(this.backend, String prefix, {this.quota})
      : folder = fileStorageFolder(prefix);

  List<String> get _root => ["flet", folder];

  List<String> _path(String name) => [..._root, ...fileStorageSegments(name)];

  String _lockName(String name) =>
      "flet.file_storage/$folder/${fileStorageSegments(name).join("/")}";

  Future<dynamic> invoke(String method, dynamic args) async {
    switch (method) {
      case "read":
        return backend.read(_path(args["name"]));
      case "write":
        return backend.mutate(
            folder, () => _write(args["name"], _bytes(args["data"])));
      case "delete":
        return backend.mutate(
            folder, () => backend.delete(_path(args["name"])));
      case "exists":
        var segments = fileStorageSegments(args["name"]);
        return (await backend.list(_root)).containsKey(segments.join("/"));
      case "list":
        String prefix = args["prefix"] ?? "";
        var names = (await backend.list(_root))
            .keys
            .where((n) => n.startsWith(prefix))
            .toList()
          ..sort();
        return names;
      case "size":
        return (await backend.list(_root)).values.fold<int>(0, (a, b) => a + b);
      case "lock":
        var name = _lockName(args["name"]);
        if (_disposed) return false;
        if (_held.contains(name)) return true;
        var ms = ((args["timeout"] ?? 5.0) as num) * 1000;
        var ok = await backend.lock(name, Duration(milliseconds: ms.round()));
        if (ok && _disposed) {
          backend.unlock(name);
          return false;
        }
        if (ok) _held.add(name);
        return ok;
      case "unlock":
        var name = _lockName(args["name"]);
        if (_held.remove(name)) backend.unlock(name);
        return null;
      default:
        throw Exception("Unknown FileStorage method: $method");
    }
  }

  Future<void> _write(String name, Uint8List data) async {
    var path = _path(name);
    var limit = quota;
    if (limit != null) {
      var files = await backend.list(_root);
      var used = files.values.fold<int>(0, (a, b) => a + b);
      var after = used - (files[path.skip(2).join("/")] ?? 0) + data.length;
      if (after > limit) {
        throw FileStorageQuotaError(
            "Writing $name (${data.length} bytes) would take this app's "
            "FileStorage to $after bytes, over its $limit-byte quota.");
      }
    }
    await backend.write(path, data);
  }

  /// Releases every lock this space still holds: the app went away.
  void releaseLocks() {
    _disposed = true;
    for (var name in _held) {
      backend.unlock(name);
    }
    _held.clear();
  }

  static Uint8List _bytes(dynamic data) {
    if (data is Uint8List) return data;
    if (data is List) return Uint8List.fromList(List<int>.from(data));
    throw ArgumentError("FileStorage.write() takes bytes.");
  }
}
