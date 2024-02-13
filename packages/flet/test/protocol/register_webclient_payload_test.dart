import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/protocol/session_payload.dart';

void main() {
  test("Session payload deserialized", () {
    const myJsonAsString = '''{
    "id": "session-1234",
    "controls": {
      "page": {
        "t": "page",
        "p": "",
        "i": "page",
        "c": []
      }
    }}''';

    final s = SessionPayload.fromJson(json.decode(myJsonAsString));
    expect(s.id, 'session-1234');
  });
}
