import 'dart:async';
import 'dart:js_interop';
import 'dart:js_interop_unsafe';
import 'dart:typed_data';

import 'package:web/web.dart' as web;

import 'file_storage_space.dart';

/// `ft.FileStorage` on web: the origin private file system (OPFS), used from
/// the page, where the app's own Python can't reach it.
///
/// Writes use `createWritable()`, which commits atomically on `close()`
/// (Chrome 86+, Firefox 111+, Safari 26+). Locks are Web Locks, shared by
/// every tab of the origin.
FileStorageBackend createFileStorageBackend() => _OpfsBackend();

class _OpfsBackend implements FileStorageBackend {
  /// Held locks: completing one releases it.
  final Map<String, Completer<JSAny?>> _locks = {};

  /// Locks released but not yet free: Web Locks lets go of a lock some time
  /// after the promise holding it settles. Completes when it's free.
  final Map<String, Future<void>> _releasing = {};

  Future<web.FileSystemDirectoryHandle> _root() async {
    var navigator = web.window.navigator as JSObject;
    var storage = navigator["storage"] as JSObject?;
    if (storage == null || !storage.has("getDirectory")) {
      throw UnsupportedError(
          "FileStorage needs the browser's origin private file system, which "
          "this page doesn't have.");
    }
    return (storage as web.StorageManager).getDirectory().toDart;
  }

  /// The folder at [segments], or `null` if it doesn't exist and [create]
  /// is false.
  Future<web.FileSystemDirectoryHandle?> _dir(List<String> segments,
      {bool create = false}) async {
    var dir = await _root();
    for (var s in segments) {
      try {
        dir = await dir
            .getDirectoryHandle(s, web.FileSystemGetDirectoryOptions(create: create))
            .toDart;
      } catch (e) {
        if (!create && _isNotFound(e)) return null;
        rethrow;
      }
    }
    return dir;
  }

  Future<web.FileSystemFileHandle?> _file(List<String> path) async {
    var dir = await _dir(path.sublist(0, path.length - 1));
    if (dir == null) return null;
    try {
      return await dir.getFileHandle(path.last).toDart;
    } catch (e) {
      if (_isNotFound(e)) return null;
      rethrow;
    }
  }

  @override
  Future<Uint8List?> read(List<String> path) async {
    var handle = await _file(path);
    if (handle == null) return null;
    var file = await handle.getFile().toDart;
    return (await file.arrayBuffer().toDart).toDart.asUint8List();
  }

  @override
  Future<void> write(List<String> path, Uint8List data) async {
    var dir = await _dir(path.sublist(0, path.length - 1), create: true);
    var handle = await dir!
        .getFileHandle(path.last, web.FileSystemGetFileOptions(create: true))
        .toDart;
    if (!(handle as JSObject).has("createWritable")) {
      throw UnsupportedError(
          "FileStorage needs a browser that can write files to its origin "
          "private file system: Chrome 86+, Firefox 111+ or Safari 26+.");
    }
    var stream = await handle.createWritable().toDart;
    try {
      await stream.write(data.toJS).toDart;
      await stream.close().toDart;
    } catch (e) {
      // Drop the half-written swap file; the old contents stay.
      await stream.abort().toDart.catchError((_) => null);
      rethrow;
    }
  }

  @override
  Future<bool> delete(List<String> path) async {
    var dir = await _dir(path.sublist(0, path.length - 1));
    if (dir == null) return false;
    try {
      await dir.removeEntry(path.last).toDart;
      return true;
    } catch (e) {
      if (_isNotFound(e)) return false;
      rethrow;
    }
  }

  @override
  Future<Map<String, int>> list(List<String> folder) async {
    var out = <String, int>{};
    var dir = await _dir(folder);
    if (dir != null) await _walk(dir, "", out);
    return out;
  }

  Future<void> _walk(
      web.FileSystemDirectoryHandle dir, String prefix, Map<String, int> out) async {
    // FileSystemDirectoryHandle is an async iterable; package:web doesn't
    // bind values(), so step its iterator by hand.
    var iterator = (dir as JSObject).callMethod<JSObject>("values".toJS);
    while (true) {
      var step =
          await iterator.callMethod<JSPromise<JSObject>>("next".toJS).toDart;
      if ((step["done"] as JSBoolean?)?.toDart ?? true) break;
      var handle = step["value"] as web.FileSystemHandle;
      var name = "$prefix${handle.name}";
      if (handle.kind == "directory") {
        await _walk(handle as web.FileSystemDirectoryHandle, "$name/", out);
      } else {
        var file = await (handle as web.FileSystemFileHandle).getFile().toDart;
        out[name] = file.size;
      }
    }
  }

  @override
  Future<bool> lock(String name, Duration timeout) async {
    var locks = (web.window.navigator as JSObject)["locks"] as JSObject?;
    if (locks == null) {
      throw UnsupportedError("FileStorage locks need the Web Locks API.");
    }
    // This page just released it: wait until it's actually free, so an
    // unlock followed by a lock behaves as it does natively.
    await _releasing[name];
    var granted = Completer<bool>();
    var release = Completer<JSAny?>();
    JSPromise<JSAny?> onGranted(JSAny? lock) {
      if (lock == null) {
        // ifAvailable and someone else holds it.
        if (!granted.isCompleted) granted.complete(false);
        return Future<JSAny?>.value(null).toJS;
      }
      if (!granted.isCompleted) granted.complete(true);
      return release.future.toJS;
    }

    var options = timeout == Duration.zero
        ? web.LockOptions(ifAvailable: true)
        : web.LockOptions(signal: web.AbortSignal.timeout(timeout.inMilliseconds));
    // Settles once the lock is released (or the request is aborted).
    var done = (locks as web.LockManager)
        .request(name, options, onGranted.toJS)
        .toDart
        .then((_) {}, onError: (_) {
      // Aborted by the timeout before it was granted.
      if (!granted.isCompleted) granted.complete(false);
    });
    var ok = await granted.future;
    if (ok) {
      _locks[name] = release;
      _held[name] = done;
    }
    return ok;
  }

  /// For each held lock, when its request settles: after it's released.
  final Map<String, Future<void>> _held = {};

  @override
  void unlock(String name) {
    var release = _locks.remove(name);
    if (release == null) return;
    var done = _held.remove(name)!;
    _releasing[name] = done;
    done.whenComplete(() {
      if (identical(_releasing[name], done)) _releasing.remove(name);
    });
    release.complete(null);
  }

  /// Whether [e] is the DOMException OPFS throws for a missing entry.
  static bool _isNotFound(Object e) {
    try {
      if ((e as JSObject)["name"].dartify() == "NotFoundError") return true;
    } catch (_) {
      // Not a JS error object.
    }
    return e.toString().contains("NotFoundError");
  }
}
