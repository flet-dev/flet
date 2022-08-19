import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/protocol/append_control_props_request.dart';

void main() {
  test("AppendControlPropsPayload payload deserialized", () {
    const myJsonAsString = '''{
    "props": [
      {
        "i": "txt1",
        "value": "Text A"
      },
      {
        "i": "stack1",
        "align": "center"
      }
    ]}''';

    final s = AppendControlPropsPayload.fromJson(json.decode(myJsonAsString));
    expect(s.props.length, 2);
  });
}
