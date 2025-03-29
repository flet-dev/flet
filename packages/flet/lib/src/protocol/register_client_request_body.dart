import '../models/control.dart';

class RegisterClientRequestBody {
  final String? sessionId;
  final String pageName;
  final Control page;

  RegisterClientRequestBody(
      {required this.sessionId, required this.pageName, required this.page});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'session_id': sessionId,
        'page_name': pageName,
        'page': page.toJson()
      };
}
