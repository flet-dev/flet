import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_view/protocol/update_control_props_payload.dart';

void main() {
  test("UpdateControlPropsPayload payload deserialized", () {
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

    final s = UpdateControlPropsPayload.fromJson(json.decode(myJsonAsString));
    expect(s.props.length, 2);
  });
}
