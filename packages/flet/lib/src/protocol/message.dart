enum MessageAction {
  registerClient(1),
  patchClient(2),
  controlEvent(3),
  updateControlProps(4),
  invokeMethod(5),
  sessionCrashed(6);

  final int value;
  const MessageAction(this.value);
}

class Message {
  final MessageAction action;
  final dynamic payload;

  Message({required this.action, required this.payload});

  dynamic toJson() => [action.value, payload.toJson()];

  factory Message.fromJson(List<dynamic> json) {
    return Message(
        action: MessageAction.values.firstWhere((e) => e.value == json[0]),
        payload: json[1]);
  }
}
