import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'package:web/web.dart' as web;

/// Holds an exclusive Web Lock until the Dart operation settles. Keep its
/// result in Dart so callers also receive the original exception and stack.
Future<T> withStorageLock<T>(String name, Future<T> Function() action) async {
  final locks = (web.window.navigator as JSObject)["locks"] as web.LockManager?;
  if (locks == null) {
    throw UnsupportedError(
        "Coordinating storage writes needs the Web Locks API.");
  }
  late Future<T> result;
  JSPromise<JSAny?> run(JSAny? lock) {
    result = Future.sync(action);
    return result.then<JSAny?>((_) => null, onError: (Object _) => null).toJS;
  }

  await locks.request(name, run.toJS).toDart;
  return result;
}
