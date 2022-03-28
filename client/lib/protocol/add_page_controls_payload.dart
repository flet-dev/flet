import '../models/control.dart';

class AddPageControlsPayload {
  final List<String> trimIDs;
  final List<Control> controls;

  AddPageControlsPayload({required this.trimIDs, required this.controls});

  factory AddPageControlsPayload.fromJson(Map<String, dynamic> json) {
    var controlsJson = json['controls'] as List;
    final controls = controlsJson.map((j) => Control.fromJson(j)).toList();
    return AddPageControlsPayload(
        trimIDs: List<String>.from(json['trimIDs']), controls: controls);
  }
}
