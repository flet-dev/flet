import '../models/control.dart';

class ReplacePageControlsPayload {
  final List<String> ids;
  final List<Control> controls;
  final bool remove;

  ReplacePageControlsPayload(
      {required this.ids, required this.controls, required this.remove});

  factory ReplacePageControlsPayload.fromJson(Map<String, dynamic> json) {
    var controlsJson = json['controls'] as List;
    final controls = controlsJson.map((j) => Control.fromJson(j)).toList();
    return ReplacePageControlsPayload(
        ids: List<String>.from(json['ids']),
        controls: controls,
        remove: json['remove'] as bool);
  }
}
