import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_view/protocol/session_crashed_payload.dart';

void main() {
  test("SessionCrashedPayload payload deserialized", () {
    const myJsonAsString = '''{
    "message": "Error while processing request!"
    }''';

    final s = SessionCrashedPayload.fromJson(json.decode(myJsonAsString));
    expect(s.message, "Error while processing request!");
  });
}
