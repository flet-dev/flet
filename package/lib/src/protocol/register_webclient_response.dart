import 'session_payload.dart';

class RegisterWebClientResponse {
  final SessionPayload? session;
  final String? error;

  RegisterWebClientResponse({this.session, this.error});

  factory RegisterWebClientResponse.fromJson(Map<String, dynamic> json) {
    return RegisterWebClientResponse(
        session: json['session'] != null
            ? SessionPayload.fromJson(json['session'])
            : null,
        error: json['error'] as String?);
  }
}
