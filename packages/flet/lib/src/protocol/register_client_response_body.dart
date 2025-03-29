class RegisterClientResponseBody {
  final String? sessionId;
  final Map<String, dynamic> patch;
  final String? error;

  RegisterClientResponseBody(
      {required this.sessionId, required this.patch, required this.error});

  factory RegisterClientResponseBody.fromJson(Map<dynamic, dynamic> json) {
    return RegisterClientResponseBody(
        sessionId: json["session_id"],
        patch: Map<String, dynamic>.from(json["page_patch"]),
        error: json['error'] as String?);
  }
}
