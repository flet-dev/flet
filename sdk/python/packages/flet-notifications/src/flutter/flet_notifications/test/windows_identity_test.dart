import 'package:flet_notifications/src/platforms/windows_identity.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const path = r"C:\Program Files\My App\my_app.exe";

  test("derives the AppUserModelID and a version 5 GUID of it", () {
    // Expected values computed independently with Python's uuid.uuid5.
    final identity = windowsIdentity(
        productName: " My App ", internalName: "My-App", executablePath: path);
    expect(identity.appName, "My App");
    expect(identity.appUserModelId, "Flet.MyApp.a80ccaf8");
    expect(identity.guid, "80060ba5-3ed9-5999-a98d-00cd5bb993f9");
  });

  test("is stable, ignoring the case of the path", () {
    final a = windowsIdentity(
        productName: "A", internalName: "app", executablePath: path);
    final b = windowsIdentity(
        productName: "A",
        internalName: "app",
        executablePath: path.toUpperCase());
    expect(b, a);
  });

  test("differs between apps and between install locations", () {
    final ids = {
      for (final (name, exe) in [
        ("app", path),
        ("other", path),
        ("app", r"D:\Apps\my_app.exe"),
      ])
        windowsIdentity(
            productName: "", internalName: name, executablePath: exe)
    };
    expect(ids.map((i) => i.appUserModelId).toSet(), hasLength(3));
    expect(ids.map((i) => i.guid).toSet(), hasLength(3));
  });

  test("uses fallbacks without version information", () {
    final identity = windowsIdentity(
        productName: "", internalName: "", executablePath: path);
    expect(identity.appName, "Flet App");
    expect(identity.appUserModelId, startsWith("Flet.App."));
  });

  test("keeps the AppUserModelID to Windows' character and length limits", () {
    final identity = windowsIdentity(
        productName: "",
        internalName: "${"é x" * 40}${"a" * 100}",
        executablePath: path);
    expect(identity.appUserModelId, matches(RegExp(r"^[A-Za-z0-9.]+$")));
    expect(identity.appUserModelId.length, lessThanOrEqualTo(128));
  });
}
