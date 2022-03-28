import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_view/protocol/message.dart';
import 'package:flet_view/protocol/update_control_props_request.dart';

void main() {
  test("UpdateControlPropsRequest serialize to message", () {
    final m = Message(
        action: MessageAction.updateControlProps,
        payload: UpdateControlPropsRequest(props: [
          {"i": "page", "winWidth": "100", "winHeight": "200"},
          {"i": "txt1", "value": "Hello, world!"},
        ]));

    final j = json.encode(m);

    expect(j,
        '{"action":"updateControlProps","payload":{"props":[{"i":"page","winWidth":"100","winHeight":"200"},{"i":"txt1","value":"Hello, world!"}]}}');
  });
}
