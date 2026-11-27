import 'package:flet_secure_storage/src/secure_storage.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';

/// An app's `SecureStorage` only reaches keys under its storage prefix: an
/// embedded app can't read, list or clear its host's keys.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late FlutterSecureStorage storage;

  Future<dynamic> call(String prefix, String name, [Map? args]) =>
      invokeSecureStorageMethod(storage, prefix, name, args ?? {});

  setUp(() {
    FlutterSecureStorage.setMockInitialValues({
      "settings.theme": "host-value",
      "app.1.todo": "mine",
      "app.12.todo": "other",
    });
    storage = const FlutterSecureStorage();
  });

  test("reads and writes only under the prefix", () async {
    expect(await call("app.1.", "get", {"key": "todo"}), "mine");
    expect(await call("app.1.", "get", {"key": "settings.theme"}), isNull);
    expect(await call("app.1.", "contains_key", {"key": "settings.theme"}), isFalse);
    await call("app.1.", "set", {"key": "settings.theme", "value": "x"});
    expect(await storage.read(key: "settings.theme"), "host-value");
    expect(await storage.read(key: "app.1.settings.theme"), "x");
    await call("app.1.", "remove", {"key": "settings.theme"});
    expect(await storage.read(key: "settings.theme"), "host-value");
    expect(await storage.containsKey(key: "app.1.settings.theme"), isFalse);
  });

  test("get_all lists only its own keys, without the prefix", () async {
    expect(await call("app.1.", "get_all"), {"todo": "mine"});
  });

  test("clear removes only its own keys", () async {
    await call("app.1.", "clear");
    expect(await storage.readAll(), {"settings.theme": "host-value", "app.12.todo": "other"});
  });

  test("an empty prefix is the plain store", () async {
    expect(await call("", "get", {"key": "settings.theme"}), "host-value");
    expect((await call("", "get_all") as Map).length, 3);
    await call("", "clear");
    expect(await storage.readAll(), isEmpty);
  });
}
