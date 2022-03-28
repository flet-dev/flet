import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_view/protocol/add_page_controls_payload.dart';

void main() {
  test("AddPageControlsPayload payload deserialized", () {
    const myJsonAsString = '''{
    "trimIDs": ["c1", "c2"],
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

    final s = AddPageControlsPayload.fromJson(json.decode(myJsonAsString));
    expect(s.trimIDs.length, 2);
    expect(s.controls.length, 2);
  });
}
