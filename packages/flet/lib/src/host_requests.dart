import 'dart:async';
import 'dart:typed_data';

/// Requests an embedded app has sent to its host and is waiting on.
///
/// Every request gets an id unique in this process, so a reply meant for a
/// request of an earlier run of the embedded app (it reloaded while its host
/// was answering) can't complete a request of the new one.
///
/// A reply is a map: `{"result": value}`, or `{"error": {"kind": ...,
/// "message": ...}}` with `kind` one of [hostRequestErrorKinds].
class HostRequests {
  HostRequests({
    required this.send,
    this.maxPending = 16,
    this.maxArgsSize = 64 * 1024,
  });

  /// Sends a request to the host.
  final void Function(int id, String name, dynamic args) send;

  /// The most requests waiting on the host at once; more fail at once.
  final int maxPending;

  /// The largest `args`, roughly in bytes, that is sent to the host.
  final int maxArgsSize;

  static int _nextId = 0;
  final Map<int, _Pending> _pending = {};

  int get pendingCount => _pending.length;

  /// Sends [name] with [args] to the host and waits for its reply, or for
  /// [timeout].
  Future<Map<String, dynamic>> request(String name, dynamic args,
      {Duration? timeout}) {
    if (name.isEmpty) {
      return Future.value(
          hostRequestError("failed", "The request has no name."));
    }
    if (_pending.length >= maxPending) {
      return Future.value(hostRequestError("failed",
          "Too many requests are waiting on the host (at most $maxPending)."));
    }
    if (approximateSize(args) > maxArgsSize) {
      return Future.value(hostRequestError("failed",
          "The request's args are too large (at most $maxArgsSize bytes)."));
    }
    final id = ++_nextId;
    final pending = _Pending();
    _pending[id] = pending;
    if (timeout != null) {
      pending.timer = Timer(timeout, () {
        if (_pending.remove(id) != null) {
          pending.completer.complete(
              hostRequestError("timeout", "The host didn't answer in time."));
        }
      });
    }
    send(id, name, args);
    return pending.completer.future;
  }

  /// Completes request [id] with the host's [reply]. Returns `false` for an
  /// id that isn't waiting: unknown, timed out or already answered.
  bool complete(int id, Map reply) {
    final pending = _pending.remove(id);
    if (pending == null) return false;
    pending.timer?.cancel();
    final error = reply["error"];
    if (error is Map) {
      final kind = error["kind"];
      pending.completer.complete(hostRequestError(
          hostRequestErrorKinds.contains(kind) ? kind : "failed",
          (error["message"] ?? "").toString()));
    } else {
      pending.completer.complete({"result": reply["result"]});
    }
    return true;
  }

  /// Fails every waiting request with [kind] and [message].
  void cancelAll(String kind, String message) {
    final pending = _pending.values.toList();
    _pending.clear();
    for (final p in pending) {
      p.timer?.cancel();
      p.completer.complete(hostRequestError(kind, message));
    }
  }
}

class _Pending {
  final completer = Completer<Map<String, dynamic>>();
  Timer? timer;
}

/// What can go wrong with a request to the host:
/// - `not_embedded`: the app isn't embedded in another;
/// - `unhandled`: the host doesn't handle requests, or not this one;
/// - `refused`: the host declined it, e.g. its user said no;
/// - `failed`: the host failed to answer it, or the request was too large;
/// - `timeout`: the host didn't answer in time.
const hostRequestErrorKinds = {
  "not_embedded",
  "unhandled",
  "refused",
  "failed",
  "timeout",
};

Map<String, dynamic> hostRequestError(String kind, String message) => {
      "error": {"kind": kind, "message": message}
    };

/// The rough size, in bytes, of a value made of maps, lists, strings,
/// bytes, numbers, booleans and nulls.
int approximateSize(dynamic value) {
  if (value == null || value is bool || value is num) return 8;
  if (value is String) return value.length;
  if (value is Uint8List) return value.length;
  if (value is Map) {
    var size = 0;
    value.forEach((k, v) => size += approximateSize(k) + approximateSize(v));
    return size;
  }
  if (value is Iterable) {
    return value.fold(0, (size, v) => size + approximateSize(v));
  }
  return value.toString().length;
}
