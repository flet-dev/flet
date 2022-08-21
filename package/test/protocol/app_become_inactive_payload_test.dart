import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/protocol/app_become_inactive_payload.dart';

void main() {
  test("AppBecomeInactivePayload payload deserialized", () {
    const myJsonAsString = '''{
    "message": "Application is inactive."
    }''';

    final s = AppBecomeInactivePayload.fromJson(json.decode(myJsonAsString));
    expect(s.message, "Application is inactive.");
  });
}
