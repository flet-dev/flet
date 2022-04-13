import 'package:equatable/equatable.dart';
import 'package:flet_view/models/control_type.dart';

class Control extends Equatable {
  static const reservedProps = ['i', 'p', 't', 'c', 'n'];

  final String id;
  final String pid;
  final ControlType type;
  final String? name;
  final List<String> childIds;
  final Map<String, String> attrs;

  const Control(
      {required this.id,
      required this.pid,
      required this.type,
      required this.name,
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
        type: ControlType.values.firstWhere(
            (t) => t.name.toLowerCase() == (json['t'] as String).toLowerCase()),
        name: json['n'] as String?,
        childIds: List<String>.from(json['c']),
        attrs: attrs);
  }

  bool? attrBool(String name, [bool? defValue]) {
    var r = attrs[name.toLowerCase()];
    return r != null ? r.toLowerCase() == "true" : defValue;
  }

  String? attrString(String name, [String? defValue]) {
    return attrs[name.toLowerCase()] ?? defValue;
  }

  int? attrInt(String name, [int? defValue]) {
    var r = attrs[name.toLowerCase()];
    if (r != null) {
      var i = int.tryParse(r);
      return i ?? defValue;
    }
    return defValue;
  }

  double? attrDouble(String name, [double? defValue]) {
    var r = attrs[name.toLowerCase()];
    if (r != null) {
      var i = double.tryParse(r);
      return i ?? defValue;
    }
    return defValue;
  }

  Control copyWith(
          {String? id,
          String? pid,
          ControlType? type,
          String? name,
          List<String>? childIds,
          Map<String, String>? attrs}) =>
      Control(
          id: id ?? this.id,
          pid: pid ?? this.pid,
          type: type ?? this.type,
          name: name ?? this.name,
          childIds: childIds ?? this.childIds,
          attrs: attrs ?? this.attrs);

  @override
  List<Object?> get props => [id, pid, type, name, childIds, attrs];
}
