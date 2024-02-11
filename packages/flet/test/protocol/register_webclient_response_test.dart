import 'dart:convert';

import 'package:flet/src/protocol/register_webclient_response.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("RegisterWebClientResponse with session deserialized", () {
    const myJsonAsString = '''{
    "appInactive": false,
    "session": {
      "id": "session-1234",
      "controls": {
        "page": {
          "i": "page",
          "t": "page",
          "p": "",
          "c": ["txt1", "stack1"],
          "hash": "aaa"
        }
      }
    }}''';

    final s = RegisterWebClientResponse.fromJson(json.decode(myJsonAsString));
    expect(s.session!.id, 'session-1234');
    expect(s.session!.controls.length, 1);
  });

  test("RegisterWebClientResponse with error deserialized", () {
    const myJsonAsString = '''{
    "error": "Page does not exist",
    "appInactive": false,
    "session": null
    }''';

    final s = RegisterWebClientResponse.fromJson(json.decode(myJsonAsString));
    expect(s.session == null, true);
    expect(s.error, "Page does not exist");
  });
}
