import 'dart:async';

import 'package:flutter/foundation.dart';

import '../utils/weak_value_map.dart';

typedef InvokeControlMethodCallback = Future<dynamic> Function(
    String name, dynamic args);

/// Represents a node or control in the UI tree.
///
/// This class extends `ChangeNotifier`, allowing it to notify listeners
/// whenever any part of its data changes. It uses a unified properties
/// map to store all nested data. Any value (or list element) in the
/// properties map that is a `Map` containing a "_c" key is automatically
/// transformed into a `Control`.
class Control extends ChangeNotifier {
  final int id;
  final String type;
  final Map<String, dynamic> properties;
  bool notifyParent = false;
  final List<String> _notifyParentProperties = ["visible"];
  WeakReference<Control>? _parent;
  Completer<void>? _listenerAddedCompleter;
  final List<InvokeControlMethodCallback> _invokeMethodListeners = [];

  Control(
      {required this.id,
      required this.type,
      required this.properties,
      Control? parent}) {
    if (parent != null) {
      _parent = WeakReference(parent);
    }
  }

  Control? get parent => _parent?.target;

  bool get disabled =>
      properties["disabled"] == true || (parent?.disabled ?? false);

  bool? get adaptive => properties["adaptive"] ?? parent?.adaptive;

  bool get visible =>
      !properties.containsKey("visible") || properties["visible"];

  T? get<T>(String propertyName, [T? defValue]) {
    return properties.containsKey(propertyName)
        ? T == double && properties[propertyName] is int
            ? properties[propertyName].toDouble()
            : properties[propertyName]
        : defValue;
  }

  bool? getBool(String propertyName, [bool? defValue]) {
    return get<bool>(propertyName, defValue);
  }

  String? getString(String propertyName, [String? defValue]) {
    return get<String>(propertyName, defValue);
  }

  int? getInt(String propertyName, [int? defValue]) {
    return get<int>(propertyName, defValue);
  }

  double? getDouble(String propertyName, [double? defValue]) {
    return get<double>(propertyName, defValue);
  }

  /// Returns the [Control] for the given [propertyName], or `null` if not found, not a [Control],
  /// or not visible when [visibleOnly] is `true` (default).
  Control? child(String propertyName, {bool visibleOnly = true}) {
    final child = properties[propertyName];
    if (child is! Control) return null;
    return (visibleOnly && !child.visible) ? null : child;
  }

  /// Returns a list of [Control]s from the specified [propertyName].
  ///
  /// If [visibleOnly] is `true` (default), only includes visible controls.
  ///
  /// Returns an empty list if the property is missing or null.
  List<Control> children(String propertyName, {bool visibleOnly = true}) {
    return List<Control>.from(properties[propertyName] ?? [])
        .where((c) => !visibleOnly || c.visible)
        .toList();
  }

  /// Creates a ControlNode from MessagePack–decoded data.
  factory Control.fromMap(Map<dynamic, dynamic> data,
      {Control? parent, WeakValueMap<int, Control>? controlsIndex}) {
    if (!data.containsKey("_c")) {
      throw Exception("Missing _c field in data: $data");
    }
    String type = data["_c"];
    int id = data["_i"];
    Map<String, dynamic> props = {};
    var newControl =
        Control(id: id, type: type, properties: props, parent: parent);
    controlsIndex?.set(newControl.id, newControl);
    data.forEach((key, value) {
      if (key == "_i" || key == "_c") return;
      props[key] = _transformIfControl(value, newControl, controlsIndex);
    });
    return newControl;
  }

  ///
  /// Applies a patch (in MessagePack–decoded form) to this ControlNode.
  /// It updates nested ControlNodes or plain data structures accordingly.
  ///
  void applyPatch(Map<dynamic, dynamic> patch,
      {WeakValueMap<int, Control>? controlsIndex, bool shouldNotify = true}) {
    debugPrint("Control($id).applyPatch: $patch, shouldNotify = $shouldNotify");
    bool changed = false;
    bool notifyParentPropertyChanged = false;
    patch.forEach((key, patchValue) {
      if (patchValue is Map) {
        if (properties.containsKey(key)) {
          var current = properties[key];
          if (current is Control) {
            current.applyPatch(patchValue,
                controlsIndex: controlsIndex, shouldNotify: shouldNotify);
          } else if (current is List) {
            var merged =
                mergeList(current, patchValue, controlsIndex, shouldNotify);
            if (merged != current) {
              properties[key] = merged;
              changed = true;
            }
          } else if (current is Map) {
            var merged =
                mergeMap(current, patchValue, controlsIndex, shouldNotify);
            if (merged != current) {
              properties[key] = merged;
              changed = true;
            }
          } else {
            properties[key] =
                _transformIfControl(patchValue, this, controlsIndex);
            changed = true;
          }
        } else {
          properties[key] =
              _transformIfControl(patchValue, this, controlsIndex);
          changed = true;
        }
      } else if (patchValue is List) {
        properties[key] = patchValue
            .map((e) => _transformIfControl(e, this, controlsIndex))
            .toList();
        changed = true;
      } else {
        if (properties[key] != patchValue) {
          properties[key] = patchValue;
          changed = true;
          if (_notifyParentProperties.contains(key)) {
            notifyParentPropertyChanged = true;
          }
        }
      }
    });
    if (changed) {
      if (shouldNotify) {
        notify();
      }
      if (notifyParentPropertyChanged) {
        _parent?.target?.notify();
      }
    }
  }

  void notify() {
    if (notifyParent) {
      _parent?.target?.notify();
    } else {
      debugPrint("$type($id) changed.");
      notifyListeners();
    }
  }

  static dynamic _transformIfControl(dynamic value, Control? parent,
      WeakValueMap<int, Control>? controlsIndex) {
    //debugPrint("_transformIfControl: $value");
    if (value is Map && value.containsKey("_c")) {
      return Control.fromMap(value,
          parent: parent, controlsIndex: controlsIndex);
    } else if (value is List &&
        value.isNotEmpty &&
        value.first is Map &&
        (value.first as Map).containsKey("_c")) {
      return value.map((e) {
        if (e is Map) {
          return Control.fromMap(e,
              parent: parent, controlsIndex: controlsIndex);
        }
        return e;
      }).toList();
    }
    return value;
  }

  /// Helper: recursively merge a patch Map into a plain Map.
  Map<dynamic, dynamic> mergeMap(
      Map<dynamic, dynamic> oldMap,
      Map<dynamic, dynamic> patch,
      WeakValueMap<int, Control>? controlsIndex,
      bool notify) {
    //debugPrint("Merge map: $oldMap, $patch");
    bool changed = false;
    Map<dynamic, dynamic> newMap = Map<String, dynamic>.from(oldMap);
    patch.forEach((k, v) {
      if (k == "\$d" && v is List) {
        for (var deleteKey in v) {
          newMap.remove(deleteKey);
        }
      } else {
        if (newMap.containsKey(k) && newMap[k] is Map && v is Map) {
          var merged = mergeMap(newMap[k], v, controlsIndex, notify);
          if (merged != newMap[k]) {
            newMap[k] = merged;
            changed = true;
          }
        } else if (newMap.containsKey(k) && newMap[k] is List && v is Map) {
          var merged = mergeList(newMap[k], v, controlsIndex, notify);
          if (merged != newMap[k]) {
            newMap[k] = merged;
            changed = true;
          }
        } else {
          if (!newMap.containsKey(k) || newMap[k] != v) {
            newMap[k] = _transformIfControl(v, this, controlsIndex);
            changed = true;
          }
        }
      }
    });
    return changed ? newMap : oldMap;
  }

  /// Helper: recursively merge a patch Map into a plain List.
  List<dynamic> mergeList(List<dynamic> oldList, Map patch,
      WeakValueMap<int, Control>? controlsIndex, bool notify) {
    //debugPrint("Merge list: $oldList, $patch");
    bool changed = false;
    List<dynamic> newList = List<dynamic>.from(oldList);
    patch.forEach((k, v) {
      if (k.toString() == "\$d") {
        if (v is List) {
          List<int> indices = List<int>.from(v);
          for (int index in indices) {
            if (index >= 0 && index < newList.length) {
              newList.removeAt(index);
              changed = true;
            }
          }
        }
      } else {
        int index = int.tryParse(k.toString()) ?? -1;
        if (v is Map && v.containsKey("\$a")) {
          if (index < 0 || index > newList.length) {
            throw Exception(("Index is out of range: $patch"));
          }
          newList.insert(
              index, _transformIfControl(v["\$a"], this, controlsIndex));
          changed = true;
        } else {
          if (index < 0 || index >= newList.length) {
            throw Exception(("Index is out of range: $patch"));
          }
          if (newList[index] is Map) {
            var merged = mergeMap(newList[index], v, controlsIndex, notify);
            if (merged != newList[index]) {
              newList[index] = merged;
              changed = true;
            }
          } else if (newList[index] is List) {
            var merged = mergeList(newList[index], v, controlsIndex, notify);
            if (merged != newList[index]) {
              newList[index] = merged;
              changed = true;
            }
          } else if (newList[index] is Control) {
            (newList[index] as Control).applyPatch(v,
                controlsIndex: controlsIndex, shouldNotify: notify);
          } else {
            newList[index] = _transformIfControl(v, this, controlsIndex);
            changed = true;
          }
        }
      }
    });
    return changed ? newList : oldList;
  }

  addInvokeMethodListener(InvokeControlMethodCallback listener) {
    _invokeMethodListeners.add(listener);

    // If someone was waiting for a listener to be added, complete the future
    if (_listenerAddedCompleter != null &&
        !_listenerAddedCompleter!.isCompleted) {
      _listenerAddedCompleter!.complete();
      _listenerAddedCompleter = null;
    }
  }

  removeInvokeMethodListener(InvokeControlMethodCallback listener) {
    _invokeMethodListeners.remove(listener);
  }

  Future<dynamic> invokeMethod(
      String name, dynamic args, Duration timeout) async {
    debugPrint("$type($id).$name($args)");

    // If no listeners, wait until one is added or timeout occurs
    if (_invokeMethodListeners.isEmpty) {
      _listenerAddedCompleter = Completer<void>();

      try {
        await Future.any([
          _listenerAddedCompleter!.future,
          Future.delayed(
              timeout,
              () => throw TimeoutException(
                  "No invoke method listeners registered within $timeout")),
        ]);
      } catch (e) {
        rethrow;
      }
    }

    if (_invokeMethodListeners.isEmpty) {
      throw Exception("No invoke method listeners registered.");
    }
    List<dynamic> results = [];
    for (var listener in _invokeMethodListeners) {
      results.add(await listener(name, args));
    }
    return results.length == 1 ? results[0] : results;
  }

  Map<String, dynamic> toJson() {
    return Map.fromEntries(
      properties.entries.where((e) => e.value != null).map((e) {
        if (e.value is Control) {
          return MapEntry(e.key, (e.value as Control).toJson());
        } else if (e.value is List &&
            e.value.isNotEmpty &&
            e.value.first is Control) {
          return MapEntry(e.key,
              (e.value as List).map((c) => (c as Control).toJson()).toList());
        } else {
          return MapEntry(e.key, e.value);
        }
      }),
    );
  }

  @override
  String toString() {
    return toJson().toString();
  }
}
