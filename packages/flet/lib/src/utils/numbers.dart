import 'package:flutter/material.dart';

import '../models/control.dart';
import 'material_state.dart';

double? parseDouble(dynamic value, [double? defaultValue]) {
  if (value is double) {
    return value;
  } else if (value is String && value.toLowerCase() == "inf") {
    return double.infinity;
  } else if (value == null) {
    return defaultValue;
  } else {
    return double.tryParse(value.toString()) ?? defaultValue;
  }
}

WidgetStateProperty<double?>? parseWidgetStateDouble(dynamic value,
    {double? defaultDouble, WidgetStateProperty<double?>? defaultValue}) {
  if (value == null) return defaultValue;
  return getWidgetStateProperty<double?>(
      value, (jv) => parseDouble(jv), defaultDouble);
}

int? parseInt(dynamic value, [int? defaultValue]) {
  if (value is int) {
    return value;
  } else if (value == null) {
    return defaultValue;
  } else {
    return int.tryParse(value.toString()) ?? defaultValue;
  }
}

WidgetStateProperty<int?>? parseWidgetStateInt(dynamic value,
    {int? defaultInt, WidgetStateProperty<int?>? defaultValue}) {
  if (value == null) return defaultValue;
  return getWidgetStateProperty<int?>(value, (jv) => parseInt(jv), defaultInt);
}

bool? parseBool(dynamic value, [bool? defaultValue]) {
  if (value is bool) {
    return value;
  } else if (value == null) {
    return defaultValue;
  } else {
    return "true" == value.toString().toLowerCase();
  }
}

WidgetStateProperty<bool?>? parseWidgetStateBool(dynamic value,
    {bool? defaultBool, WidgetStateProperty<bool?>? defaultValue}) {
  if (value == null) return defaultValue;
  return getWidgetStateProperty<bool?>(
      value, (jv) => parseBool(jv), defaultBool);
}

extension LiteralParsers on Control {
  bool? getBool(String propertyName, [bool? defaultValue]) {
    return get<bool>(propertyName, defaultValue);
  }

  String? getString(String propertyName, [String? defaultValue]) {
    return get<String>(propertyName, defaultValue);
  }

  int? getInt(String propertyName, [int? defaultValue]) {
    return get<int>(propertyName, defaultValue);
  }

  double? getDouble(String propertyName, [double? defaultValue]) {
    return get<double>(propertyName, defaultValue);
  }

  DateTime? getDateTime(String propertyName, [DateTime? defaultValue]) {
    return get<DateTime>(propertyName, defaultValue);
  }

  WidgetStateProperty<double?>? getWidgetStateDouble(String propertyName,
      {double? defaultDouble, WidgetStateProperty<double?>? defaultValue}) {
    return parseWidgetStateDouble(get(propertyName),
        defaultDouble: defaultDouble, defaultValue: defaultValue);
  }

  WidgetStateProperty<int?>? getWidgetStateInt(String propertyName,
      {int? defaultInt, WidgetStateProperty<int?>? defaultValue}) {
    return parseWidgetStateInt(get(propertyName),
        defaultInt: defaultInt, defaultValue: defaultValue);
  }

  WidgetStateProperty<bool?>? getWidgetStateBool(String propertyName,
      {bool? defaultBool, WidgetStateProperty<bool?>? defaultValue}) {
    return parseWidgetStateBool(get(propertyName),
        defaultBool: defaultBool, defaultValue: defaultValue);
  }
}
