class RegisterClientRequestBody {
  final String? sessionId;
  final String pageName;
  final Map<String, dynamic> page;

  RegisterClientRequestBody(
      {required this.sessionId, required this.pageName, required this.page});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'session_id': sessionId,
        'page_name': pageName,
        'page': page
      };
}
