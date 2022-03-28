import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_view/protocol/clean_control_payload.dart';

void main() {
  test("CleanControlPayload payload deserialized", () {
    const myJsonAsString = '''{
    "ids": ["c1", "c2"]
    }''';

    final s = CleanControlPayload.fromJson(json.decode(myJsonAsString));
    expect(s.ids.length, 2);
  });
}
