import 'dart:async';
import 'dart:io';
import 'dart:math';

import 'package:flutter/foundation.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

import 'file_storage_space.dart';

/// `ft.FileStorage` on desktop and mobile: a folder under the app support
/// directory. Writes go to a temporary file renamed over the target, so a
/// reader never sees half a file. Locks are held within this process.
FileStorageBackend createFileStorageBackend() => _FolderBackend();

/// The folder backend rooted at [base] instead of the app support directory.
@visibleForTesting
FileStorageBackend createFolderFileStorageBackend(String base) =>
    _FolderBackend(base: base);

/// Held locks, shared by every app in this process.
final Map<String, Completer<void>> _locks = {};

class _FolderBackend implements FileStorageBackend {
  _FolderBackend({String? base}) : _fixedBase = base;

  final String? _fixedBase;
  static Future<String>? _supportDir;

  Future<String> _path(List<String> segments) async {
    var base = _fixedBase ??
        await (_supportDir ??=
            getApplicationSupportDirectory().then((d) => d.path));
    return p.joinAll([base, ...segments]);
  }

  // POSIX record locks are process-scoped. Queue local callers before opening
  // the lock file, then hold the OS lock through the entire mutation.
  static final _mutations = <String, Future<void>>{};

  @override
  Future<T> mutate<T>(String folder, Future<T> Function() action) async {
    final path = await _path(["flet", ".locks", folder]);
    final finished = Completer<void>();
    final previous = _mutations[path];
    _mutations[path] = finished.future;
    try {
      await previous;
      final file = File(path);
      await file.parent.create(recursive: true);
      final handle = await file.open(mode: FileMode.append);
      try {
        await handle.lock(FileLock.blockingExclusive);
        return await action();
      } finally {
        // Closing releases the OS lock, including on error.
        await handle.close();
      }
    } finally {
      finished.complete();
      if (identical(_mutations[path], finished.future)) _mutations.remove(path);
    }
  }

  @override
  Future<Uint8List?> read(List<String> path) async {
    var file = File(await _path(path));
    try {
      return await file.readAsBytes();
    } on PathNotFoundException {
      return null;
    }
  }

  @override
  Future<void> write(List<String> path, Uint8List data) async {
    var target = File(await _path(path));
    await target.parent.create(recursive: true);
    var tmp = File("${target.path}.${Random().nextInt(1 << 32)}"
        "$fileStorageTempSuffix");
    try {
      await tmp.writeAsBytes(data, flush: true);
      await tmp.rename(target.path);
    } catch (_) {
      if (await tmp.exists()) await tmp.delete();
      rethrow;
    }
  }

  @override
  Future<bool> delete(List<String> path) async {
    var file = File(await _path(path));
    if (!await file.exists()) return false;
    await file.delete();
    return true;
  }

  @override
  Future<Map<String, int>> list(List<String> folder) async {
    var dir = Directory(await _path(folder));
    var out = <String, int>{};
    if (!await dir.exists()) return out;
    await for (var entity in dir.list(recursive: true, followLinks: false)) {
      if (entity is! File || entity.path.endsWith(fileStorageTempSuffix)) {
        continue;
      }
      var name = p.split(p.relative(entity.path, from: dir.path)).join("/");
      out[name] = await entity.length();
    }
    return out;
  }

  @override
  Future<bool> lock(String name, Duration timeout) async {
    var deadline = DateTime.now().add(timeout);
    while (_locks.containsKey(name)) {
      var left = deadline.difference(DateTime.now());
      if (left <= Duration.zero) return false;
      try {
        await _locks[name]!.future.timeout(left);
      } on TimeoutException {
        return false;
      }
    }
    _locks[name] = Completer<void>();
    return true;
  }

  @override
  void unlock(String name) {
    _locks.remove(name)?.complete();
  }
}
