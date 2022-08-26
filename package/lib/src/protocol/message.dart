enum MessageAction {
  registerWebClient,
  pageEventFromWeb,
  updateControlProps,
  appBecomeActive,
  appBecomeInactive,
  sessionCrashed,
  signout,
  addPageControls,
  replacePageControls,
  pageControlsBatch,
  appendControlProps,
  cleanControl,
  removeControl
}

class Message {
  final MessageAction action;
  final dynamic payload;

  Message({required this.action, required this.payload});

  Map<String, dynamic> toJson() =>
      <String, dynamic>{'action': action.name, 'payload': payload.toJson()};

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
        action: MessageAction.values
            .firstWhere((e) => e.name == json['action'] as String),
        payload: json['payload']);
  }
}
