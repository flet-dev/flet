import 'session_payload.dart';

class RegisterWebClientResponse {
  final SessionPayload? session;
  final bool appInactive;
  final String? error;

  RegisterWebClientResponse(
      {this.session, required this.appInactive, this.error});

  factory RegisterWebClientResponse.fromJson(Map<String, dynamic> json) {
    return RegisterWebClientResponse(
        session: json['session'] != null
            ? SessionPayload.fromJson(json['session'])
            : null,
        appInactive: json['appInactive'] as bool,
        error: json['error'] as String?);
  }
}
