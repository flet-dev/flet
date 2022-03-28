import 'package:flet_view/protocol/message.dart';

class PageControlsBatchPayload {
  final List<Message> messages;

  PageControlsBatchPayload({required this.messages});

  factory PageControlsBatchPayload.fromJson(dynamic json) {
    var messagesJson = json as List;
    return PageControlsBatchPayload(
        messages: messagesJson.map((m) => Message.fromJson(m)).toList());
  }
}
