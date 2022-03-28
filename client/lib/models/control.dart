import 'package:equatable/equatable.dart';

class Control extends Equatable {
  static const reservedProps = ['i', 'p', 't', 'c'];

  final String id;
  final String pid;
  final String type;
  final List<String> childIds;
  final Map<String, String> attrs;

  const Control(
      {required this.id,
      required this.pid,
      required this.type,
      required this.childIds,
      required this.attrs});

  factory Control.fromJson(Map<String, dynamic> json) {
    Map<String, String> attrs = {};
    for (var key in json.keys) {
      if (!reservedProps.contains(key)) {
        attrs[key] = json[key] as String;
      }
    }
    return Control(
        id: json['i'] as String,
        pid: json['p'] as String,
        type: json['t'] as String,
        childIds: List<String>.from(json['c']),
        attrs: attrs);
  }

  Control copyWith(
          {String? id,
          String? pid,
          String? type,
          List<String>? childIds,
          Map<String, String>? attrs}) =>
      Control(
          id: id ?? this.id,
          pid: pid ?? this.pid,
          type: type ?? this.type,
          childIds: childIds ?? this.childIds,
          attrs: attrs ?? this.attrs);

  @override
  List<Object?> get props => [id, pid, type, childIds, attrs];
}
