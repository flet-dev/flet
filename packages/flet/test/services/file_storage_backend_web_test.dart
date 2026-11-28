@TestOn('browser')
library;

import 'dart:async';
import 'dart:js_interop';
import 'dart:js_interop_unsafe';
import 'dart:typed_data';

import 'package:flet/src/services/file_storage_backend_web.dart';
import 'package:flutter_test/flutter_test.dart';

import 'file_storage_backend_contract.dart';

/// The OPFS backend in a real browser: `flutter test --platform chrome`.
void main() {
  fileStorageBackendContract(createFileStorageBackend);

  test("an unsuccessful first write never publishes the target", () async {
    final backend = createFileStorageBackend();
    final folder = ["flet", "publish-${DateTime.now().microsecondsSinceEpoch}"];
    final path = [...folder, "notes"];
    final constructor = globalContext["FileSystemFileHandle"] as JSObject;
    final prototype = constructor["prototype"] as JSObject;
    final move = prototype["move"];
    final publishing = Completer<void>();
    final finish = Completer<JSAny?>();
    prototype["move"] = ((JSString name) {
      publishing.complete();
      return finish.future.toJS;
    }).toJS;
    try {
      final failure =
          expectLater(backend.write(path, Uint8List(1)), throwsA(anything));
      await publishing.future;
      expect(await backend.read(path), isNull);
      expect(await backend.list(folder), isEmpty);
      finish.completeError(StateError("publish failed"));
      await failure;
      expect(await backend.read(path), isNull);
      expect(await backend.list(folder), isEmpty);
    } finally {
      prototype["move"] = move;
    }
    await backend.write(path, Uint8List(1));
    expect(await backend.read(path), [0]);
    await backend.delete(path);
  });
}
