import 'dart:convert';

import 'package:flet/src/protocol/message.dart';
import 'package:flet/src/protocol/update_control_props_request.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("UpdateControlPropsRequest serialize to message", () {
    final m = Message(
        action: MessageAction.updateControlProps,
        payload: UpdateControlPropsRequest(props: [
          {"i": "page", "width": "100", "height": "200"},
          {"i": "txt1", "value": "Hello, world!"},
        ]));

    final j = json.encode(m);

    expect(j,
        '{"action":"updateControlProps","payload":{"props":[{"i":"page","width":"100","height":"200"},{"i":"txt1","value":"Hello, world!"}]}}');
  });
}
