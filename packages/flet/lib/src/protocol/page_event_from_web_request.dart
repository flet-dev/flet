class PageEventFromWebRequest {
  final String eventTarget;
  final String eventName;
  final String eventData;

  PageEventFromWebRequest(
      {required this.eventTarget,
      required this.eventName,
      required this.eventData});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'eventTarget': eventTarget,
        'eventName': eventName,
        'eventData': eventData
      };
}
