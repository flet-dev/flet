import '../models/control.dart';

class SessionPayload {
  final String id;
  final Map<String, Control> controls;

  SessionPayload({required this.id, required this.controls});

  factory SessionPayload.fromJson(Map<String, dynamic> json) {
    Map<String, Control> controls = {};
    for (var key in json['controls'].keys) {
      controls[key] = Control.fromJson(json['controls'][key]);
    }
    return SessionPayload(id: json['id'] as String, controls: controls);
  }
}
