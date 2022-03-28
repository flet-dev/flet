class SessionCrashedPayload {
  final String message;

  SessionCrashedPayload({required this.message});

  factory SessionCrashedPayload.fromJson(Map<String, dynamic> json) =>
      SessionCrashedPayload(message: json['message'] as String);
}
