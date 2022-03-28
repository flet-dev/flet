import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet_view/protocol/message.dart';
import 'package:flet_view/protocol/register_webclient_request.dart';

void main() {
  test("RegisterWebClientRequest serialize to message", () {
    final m = Message(
        action: MessageAction.registerWebClient,
        payload: RegisterWebClientRequest(pageName: "test-page1"));

    final j = json.encode(m);
    expect(j,
        '{"action":"registerWebClient","payload":{"pageName":"test-page1","pageHash":null,"winWidth":null,"winHeight":null,"sessionId":null}}');
  });
}
