import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/protocol/message.dart';
import 'package:flet/src/protocol/remove_control_payload.dart';

void main() {
  test("Message parse from JSON", () {
    const s = '''
    {
      "action": "removeControl",
      "payload": {
        "ids": ["i1", "i2"]
      }
    }
''';

    final m = Message.fromJson(json.decode(s));
    expect(m.action, MessageAction.removeControl);

    if (m.action == MessageAction.removeControl) {
      final payload = RemoveControlPayload.fromJson(m.payload);
      expect(payload.ids.length, 2);
    }
  });
}
