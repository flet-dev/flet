import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/protocol/session_payload.dart';

void main() {
  test("Session payload deserialized", () {
    const myJsonAsString = '''{
    "id": "session-1234",
    "controls": {
      "page": {
        "i": "page",
        "t": "page",
        "p": "",
        "c": ["txt1", "stack1"],
        "hash": "aaa"
      },
      "txt1": {
        "i": "txt1",
        "t": "text",
        "p": "page",
        "c": [],
        "value": "Text A"
      },
      "stack1": {
        "i": "stack1",
        "t": "stack",
        "p": "page",
        "c": ["txt2"],
        "align": "center"
      },
      "txt2": {
        "i": "txt2",
        "t": "text",
        "p": "stack1",
        "c": [],
        "value": "Text B",
        "color": "red"
      }
    }}''';

    final s = SessionPayload.fromJson(json.decode(myJsonAsString));
    expect(s.id, 'session-1234');
    expect(s.controls.length, 4);
    expect(s.controls['page']!.attrs.length, 1);
    expect(s.controls['txt1']!.attrs.length, 1);
    expect(s.controls['stack1']!.attrs.length, 1);
    expect(s.controls['txt2']!.attrs.length, 2);
    expect(s.controls['txt2']!.attrs["color"], "red");
    expect(s.controls['txt2']!.attrs["value"], "Text B");
  });
}
