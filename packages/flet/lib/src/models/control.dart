import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

import '../utils/colors.dart';

class Control extends Equatable {
  static const reservedProps = ['i', 'p', 't', 'c', 'n'];

  final String id;
  final String pid;
  final String type;
  final String? name;
  final List<String> childIds;
  final Map<String, String> attrs;
  final Map<String, dynamic> state = {};
  final Set<void Function()> onRemove = {};

  Control(
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
        type: (json['t'] as String).toLowerCase(),
        name: json['n'] as String?,
        childIds: List<String>.from(json['c']),
        attrs: attrs);
  }

  bool get disabled {
    return getBool("disabled", false)!;
  }

  bool? get adaptive {
    return getBool("adaptive");
  }

  bool get visible {
    return getBool("visible", true)!;
  }

  bool get isNonVisual {
    return [
      //"alertdialog",
      //"audio",
      "banner",
      //"bottomsheet",
      "clipboard",
      "filepicker",
      "hapticfeedback",
      "shakedetector",
      "snackbar"
    ].contains(type);
  }

  bool? getBool(String name, [bool? defValue]) {
    var r = attrs[name.toLowerCase()];
    return r != null ? r.toLowerCase() == "true" : defValue;
  }

  String? getString(String name, [String? defValue]) {
    return attrs[name.toLowerCase()] ?? defValue;
  }

  int? getInt(String name, [int? defValue]) {
    var r = attrs[name.toLowerCase()];
    if (r != null) {
      var i = int.tryParse(r);
      return i ?? defValue;
    }
    return defValue;
  }

  double? getDouble(String name, [double? defValue]) {
    var r = attrs[name.toLowerCase()];
    if (r != null && r.toLowerCase() == "inf") {
      return double.infinity;
    } else if (r != null) {
      var i = double.tryParse(r);
      return i ?? defValue;
    }
    return defValue;
  }

  DateTime? getDateTime(String name, [DateTime? defValue]) {
    var value = attrs[name.toLowerCase()];
    if (value == null) {
      return defValue;
    }
    try {
      return DateTime.parse(value);
    } catch (e) {
      return defValue;
    }
  }

  TimeOfDay? getTime(String name, [TimeOfDay? defValue]) {
    var value = attrs[name.toLowerCase()];
    if (value == null) {
      return defValue;
    }
    List<String> splitted = value.split(':');
    return TimeOfDay(
        hour: int.parse(splitted[0]), minute: int.parse(splitted[1]));
  }

  Color? getColor(String name, BuildContext? context, [Color? defValue]) {
    return parseColor(
        context != null ? Theme.of(context) : null, getString(name), defValue);
  }

  Control copyWith(
      {String? id,
      String? pid,
      String? type,
      String? name,
      List<String>? childIds,
      Map<String, String>? attrs,
      Map<String, dynamic>? state}) {
    Control c = Control(
        id: id ?? this.id,
        pid: pid ?? this.pid,
        type: type ?? this.type,
        name: name ?? this.name,
        childIds: childIds ?? this.childIds,
        attrs: attrs ?? this.attrs);
    for (var element in this.state.entries) {
      c.state[element.key] = element.value;
    }
    c.onRemove.addAll(onRemove);
    return c;
  }

  @override
  List<Object?> get props => [id, pid, type, name, childIds, attrs];
}
