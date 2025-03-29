enum MessageAction {
  registerClient(1),
  patchControl(2),
  controlEvent(3),
  updateControl(4),
  invokeControlMethod(5),
  sessionCrashed(6);

  final int value;
  const MessageAction(this.value);
}

class Message {
  final MessageAction action;
  final dynamic payload;

  Message({required this.action, required this.payload});

  dynamic toJson() => [action.value, payload];

  factory Message.fromJson(List<dynamic> json) {
    return Message(
        action: MessageAction.values.firstWhere((e) => e.value == json[0]),
        payload: json[1]);
  }
}
