import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/protocol/replace_page_controls_payload.dart';

void main() {
  test("ReplacePageControlsPayload payload deserialized", () {
    const myJsonAsString = '''{
    "remove": true,
    "ids": ["c1", "c2"],
    "controls": [
      {
        "i": "txt1",
        "t": "text",
        "p": "page",
        "c": [],
        "value": "Text A"
      },
      {
        "i": "stack1",
        "t": "stack",
        "p": "page",
        "c": ["txt2"],
        "align": "center"
      }
    ]}''';

    final s = ReplacePageControlsPayload.fromJson(json.decode(myJsonAsString));
    expect(s.ids.length, 2);
    expect(s.controls.length, 2);
    expect(s.remove, true);
  });
}
