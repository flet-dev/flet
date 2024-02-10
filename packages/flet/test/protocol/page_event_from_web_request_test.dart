import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/protocol/message.dart';
import 'package:flet/src/protocol/page_event_from_web_request.dart';

void main() {
  test("PageEventFromWebRequest serialize to message", () {
    final m = Message(
        action: MessageAction.pageEventFromWeb,
        payload: PageEventFromWebRequest(
            eventTarget: "page", eventName: "resize", eventData: "100x200"));

    final j = json.encode(m);

    expect(j,
        '{"action":"pageEventFromWeb","payload":{"eventTarget":"page","eventName":"resize","eventData":"100x200"}}');
  });
}
