import 'dart:convert';

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

  bool get isDisabled {
    return attrBool("disabled", false)!;
  }

  bool get isVisible {
    return attrBool("visible", true)!;
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
    if (r != null && r.toLowerCase() == "inf") {
      return double.infinity;
    } else if (r != null) {
      var i = double.tryParse(r);
      return i ?? defValue;
    }
    return defValue;
  }

  DateTime? attrDateTime(String name, [DateTime? defValue]) {
    var value = attrs[name.toLowerCase()];
    if (value == null) {
      return defValue;
    }
    return DateTime.parse(value);
  }

  TimeOfDay? attrTime(String name, [TimeOfDay? defValue]) {
    var value = attrs[name.toLowerCase()];
    if (value == null) {
      return defValue;
    }
    List<String> splitted = value.split(':');
    return TimeOfDay(
        hour: int.parse(splitted[0]), minute: int.parse(splitted[1]));
  }

  Color? attrColor(String name, BuildContext? context, [Color? defValue]) {
    return HexColor.fromString(context != null ? Theme.of(context) : null,
            attrString(name, "")!) ??
        defValue;
  }

  List? attrList(String name, [List? defValue = const []]) {
    var l = attrString(name);
    if (l == null) {
      return defValue;
    } else {
      try {
        return jsonDecode(l) as List;
      } catch (e) {
        debugPrint("attrList error while parsing $name: $e");
        return defValue;
      }
    }
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
