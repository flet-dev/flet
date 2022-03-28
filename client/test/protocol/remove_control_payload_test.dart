import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_view/protocol/remove_control_payload.dart';

void main() {
  test("RemoveControlPayload payload deserialized", () {
    const myJsonAsString = '''{
    "ids": ["c1", "c2"]
    }''';

    final s = RemoveControlPayload.fromJson(json.decode(myJsonAsString));
    expect(s.ids.length, 2);
  });
}
