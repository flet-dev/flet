class SessionCrashedBody {
  final String message;

  SessionCrashedBody({required this.message});

  factory SessionCrashedBody.fromJson(Map<dynamic, dynamic> json) =>
      SessionCrashedBody(message: json['message'] as String);
}
