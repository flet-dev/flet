import 'package:flet/src/utils/networking.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("localhost address is private", () async {
    expect(await isPrivateHost("localhost"), true);
  });

  test("127.0.1.1 address is private", () async {
    expect(await isPrivateHost("127.0.1.1"), true);
  });

  test("192.168.0.1 address is private", () async {
    expect(await isPrivateHost("192.168.0.1"), true);
  });

  test("172.16.0.10 address is private", () async {
    expect(await isPrivateHost("172.16.0.10"), true);
  });

  test("10.0.5.100 address is private", () async {
    expect(await isPrivateHost("10.0.5.100"), true);
  });

  test("216.34.2.201 address is public", () async {
    expect(await isPrivateHost("216.34.2.201"), false);
  });

  test("45.3.2.2 address is public", () async {
    expect(await isPrivateHost("45.3.2.2"), false);
  });

  test("flutter.dev address is public", () async {
    expect(await isPrivateHost("flutter.dev"), false);
  });
}
