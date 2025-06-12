import 'dart:async';

import 'package:collection/collection.dart';
import 'package:flutter/foundation.dart';

import '../flet_backend.dart';

typedef InvokeControlMethodCallback = Future<dynamic> Function(
    String name, dynamic args);

enum OperationType {
  unknown(-1),
  replace(0),
  add(1),
  remove(2),
  move(3);

  final int value;

  const OperationType(this.value);

  static OperationType? fromInt(int value) {
    return OperationType.values.firstWhere(
      (e) => e.value == value,
      orElse: () => unknown, // return unknown if not found
    );
  }
}

class PatchTarget {
  final dynamic obj;
  final Control control;

  const PatchTarget(this.obj, this.control);
}

/// Represents a node or control in the UI tree.
///
/// This class extends `ChangeNotifier`, allowing it to notify listeners
/// whenever any part of its data changes. It uses a unified properties
/// map to store all nested data. Any value (or list element) in the
/// properties map that is a `Map` containing a "_c" key is automatically
/// transformed into a `Control`.
class Control extends ChangeNotifier {
  static const DeepCollectionEquality _equality = DeepCollectionEquality();
  final int id;
  final String type;
  final Map<String, dynamic> properties;
  bool notifyParent = false;
  final List<String> _notifyParentProperties = ["visible"];
  WeakReference<Control>? _parent;
  late final WeakReference<FletBackend> _backend;
  Completer<void>? _listenerAddedCompleter;
  final List<InvokeControlMethodCallback> _invokeMethodListeners = [];

  Control({
    required this.id,
    required this.type,
    required this.properties,
    required FletBackend backend,
    Control? parent,
  }) {
    if (parent != null) {
      _parent = WeakReference(parent);
    }
    _backend = WeakReference(backend);
  }

  Control? get parent => _parent?.target;

  FletBackend get backend => _backend.target!;

  bool get disabled =>
      properties["disabled"] == true || (parent?.disabled ?? false);

  bool? get adaptive => properties["adaptive"] ?? parent?.adaptive;

  bool get visible =>
      !properties.containsKey("visible") || properties["visible"];

  T? get<T>(String propertyName, [T? defaultValue]) {
    return properties.containsKey(propertyName) &&
            properties[propertyName] != null
        ? T == double && properties[propertyName] is int
            ? properties[propertyName].toDouble()
            : T == String
                ? properties[propertyName].toString()
                : properties[propertyName]
        : defaultValue;
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

  /// Triggers a control event.
  ///
  /// This method checks if the control has an event handler for the given
  /// [eventName] and triggers the event if the application is not in a loading state.
  ///
  /// - [eventName]: The name of the event to trigger.
  /// - [eventData]: Optional data to pass along with the event.
  void triggerEvent(String eventName, [dynamic data]) {
    return backend.triggerControlEvent(this, eventName, data);
  }

  /// Updates the properties of this control.
  ///
  /// The [props] map contains key-value pairs where the key is the property
  /// name and the value is the new value for that property.
  ///
  /// - [props]: A map of property names and their corresponding new values.
  /// - [dart]: A boolean indicating whether to apply the patch in Dart. Defaults to `true`.
  /// - [python]: A boolean indicating whether to send the update to the Python backend. Defaults to `true`.
  /// - [notify]: A boolean indicating whether to notify listeners after applying the patch. Defaults to `false`.
  ///
  /// This method is typically used to modify the state of a control dynamically.
  void updateProperties(Map<String, dynamic> props,
      {bool dart = true, bool python = true, bool notify = false}) {
    return backend.updateControl(id, props,
        dart: dart, python: python, notify: notify);
  }

  /// Creates a ControlNode from MessagePack–decoded data.
  factory Control.fromMap(Map<dynamic, dynamic> data, FletBackend backend,
      {Control? parent}) {
    if (!data.containsKey("_c")) {
      throw Exception("Missing _c field in data: $data");
    }
    String type = data["_c"];
    int id = data["_i"];
    Map<String, dynamic> props = {};
    var newControl = Control(
        id: id,
        type: type,
        properties: props,
        backend: backend,
        parent: parent);
    backend.controlsIndex.set(newControl.id, newControl);
    data.forEach((key, value) {
      if (key == "_i" || key == "_c") return;
      props[key] = _transformIfControl(value, newControl, backend);
    });
    return newControl;
  }

  bool update(Map<dynamic, dynamic> props, {bool shouldNotify = false}) {
    final changes = <String>[];
    _mergeMaps(this, properties, props, changes, '');
    if (changes.isNotEmpty) {
      if (shouldNotify) {
        notify();
      }
      if (changes.any((prop) => _notifyParentProperties.contains(prop))) {
        _parent?.target?.notify();
      }
    }
    return changes.isNotEmpty;
  }

  void _mergeMaps(
    Control? parent,
    Map<dynamic, dynamic> dst,
    Map<dynamic, dynamic> src,
    List<String> changes,
    String prefix,
  ) {
    for (var entry in src.entries) {
      final key = entry.key;
      final fullKey = prefix.isEmpty ? key : '$prefix.$key';

      if (dst[key] is Map && entry.value is Map) {
        _mergeMaps(parent, dst[key], entry.value, changes, fullKey);
      } else if (dst[key] is Control && entry.value is Map) {
        _mergeMaps(parent, dst[key].properties, entry.value, changes, fullKey);
      } else if (dst[key] != entry.value) {
        dst[key] = _transformIfControl(entry.value, parent, backend);
        changes.add(fullKey);
      }
    }
  }

  ///
  /// Applies a patch (in MessagePack–decoded form) to this ControlNode.
  /// It updates nested ControlNodes or plain data structures accordingly.
  ///
  /// Patch format:
  /// patch := [[<tree_index>],<operation 1>, <operation 2>, ...]
  ///
  /// operation := <move_operation> | <remove_operation> | <other_operation>
  /// move_operation := [3, <src_tree_node_index>, <src_index>,
  ///      <dst_tree_node_index>, <dst_index>]
  /// remove_operation := [2, <tree_node_index>, <index>]
  /// other_operation := [0|1, <tree_node_index>, <property|index>, <value>]
  ///
  /// type:
  ///   Replace = 0
  ///   Add = 1
  ///   Remove = 2
  ///   Move = 3
  ///
  /// tree_index := [[0, {"property|position 1": [index, {"property|position 2"}], ...}]
  ///
  /// Example:
  ///  [
  ///     0,
  ///     {
  ///        "data_series":[
  ///           1,
  ///           {
  ///              0:[
  ///                 2,
  ///                 {
  ///                    "data_points":[
  ///                       3,
  ///                       {
  ///                          1:[
  ///                             4
  ///                          ]
  ///                       }
  ///                    ]
  ///                 }
  ///              ]
  ///           }
  ///        ],
  ///     }
  ///  ]
  ///
  /// Tree is converted to a Map with index as a key and Control,
  /// or other object, or map, or list, as a value:
  ///
  /// 0: <Control> # root control .applyPatch is called against
  /// 1: <List>    # "data_series" collection
  /// 2: <Control> # "data_series[0]" DataSeries control
  /// 3: <List>    # "data_series[0]["data_points"]" list of datapoints
  /// 4: <Control> # "data_series[0]["data_points"][1]" DataPoint control
  void applyPatch(List<dynamic> patch, FletBackend backend,
      {bool shouldNotify = true}) {
    debugPrint("Control($id).applyPatch: $patch, shouldNotify = $shouldNotify");

    if (patch.length < 2) {
      throw Exception(
          "Patch must be a list with at least 2 elements: tree_index, operation");
    }

    // build map of "to-be-patched" tree nodes
    Map<int, PatchTarget> treeIndex = {};
    buildTreeIndex(Control control, dynamic obj, List<dynamic> node) {
      // node[0] - index
      // node[1] - map of child properties or indexes
      treeIndex[node[0]] =
          PatchTarget(obj is Control ? obj.properties : obj, control);
      if (node.length > 1 && node[1] is Map) {
        for (var entry in (node[1] as Map).entries) {
          // key - property name or list index
          // value - child node
          dynamic child;
          if (obj is Control) {
            child = obj.properties[entry.key];
          } else if (obj is Map) {
            child = obj[entry.key];
          } else if (obj is List) {
            child = obj[entry.key];
          }
          if (child is Control) {
            control = child;
          }
          buildTreeIndex(control, child, entry.value);
        }
      }
    }

    buildTreeIndex(this, this, patch[0]);
    //debugPrint("TREE INDEX: $treeIndex");

    // apply patch commands
    for (int i = 1; i < patch.length; i++) {
      var op = patch[i] as List<dynamic>;
      var opType = OperationType.fromInt(op[0]);
      if (opType == OperationType.replace) {
        // REPLACE
        var node = treeIndex[op[1]]!;
        var key = op[2];
        var value = op[3];
        node.obj[key] = _transformIfControl(value, node.control, backend);
        if (shouldNotify) {
          node.control.notify();
        }
        if (key is String) {
          node.control.notifyParentIfPropertyChanged(key);
        }
      } else if (opType == OperationType.add) {
        // ADD
        var node = treeIndex[op[1]]!;
        var index = op[2];
        var value = op[3];
        if (node.obj is! List) {
          throw Exception("Add operation can be applied to lists only: $op");
        }
        node.obj
            .insert(index, _transformIfControl(value, node.control, backend));
        if (shouldNotify) {
          node.control.notify();
        }
      } else if (opType == OperationType.remove) {
        // REMOVE
        var node = treeIndex[op[1]]!;
        var index = op[2];
        if (node.obj is! List) {
          throw Exception("Remove operation can be applied to lists only: $op");
        }
        node.obj.removeAt(index);
        if (shouldNotify) {
          node.control.notify();
        }
      } else if (opType == OperationType.move) {
        // MOVE
        var fromNode = treeIndex[op[1]]!;
        var fromIndex = op[2];
        var toNode = treeIndex[op[3]]!;
        var toIndex = op[4];
        if (fromNode.obj is! List || toNode.obj is! List) {
          throw Exception("Move operation can be applied to lists only: $op");
        }
        toNode.obj.insert(toIndex, fromNode.obj.removeAt(fromIndex));
        if (shouldNotify) {
          fromNode.control.notify();
        }
        if (shouldNotify) {
          toNode.control.notify();
        }
      } else {
        throw Exception("Unknown patch operation: ${op[0]}");
      }
    }
  }

  void notify() {
    debugPrint("Notify $type($id)");
    if (notifyParent) {
      _parent?.target?.notify();
    } else {
      notifyListeners();
    }
  }

  void notifyParentIfPropertyChanged(String name) {
    if (_notifyParentProperties.contains(name)) {
      debugPrint("notifyParentIfPropertyChanged: $type($id).$name");
      _parent?.target?.notify();
    }
  }

  static dynamic _transformIfControl(
      dynamic value, Control? parent, FletBackend backend) {
    //debugPrint("_transformIfControl: $value");
    if (value is Map && value.containsKey("_c")) {
      return Control.fromMap(value, backend, parent: parent);
    } else if (value is List &&
        value.isNotEmpty &&
        value.first is Map &&
        (value.first as Map).containsKey("_c")) {
      return value.map((e) {
        if (e is Map) {
          return Control.fromMap(e, backend, parent: parent);
        }
        return e;
      }).toList();
    }
    return value;
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

  Map<String, dynamic> toMap() {
    return Map.fromEntries(
      properties.entries.where((e) => e.value != null).map((e) {
        if (e.value is Control) {
          return MapEntry(e.key, (e.value as Control).toMap());
        } else if (e.value is List &&
            e.value.isNotEmpty &&
            e.value.first is Control) {
          return MapEntry(e.key,
              (e.value as List).map((c) => (c as Control).toMap()).toList());
        } else {
          return MapEntry(e.key, e.value);
        }
      }),
    );
  }

  @override
  String toString() {
    return toMap().toString();
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        other is Control &&
            other.id == id &&
            other.type == type &&
            _equality.equals(other.properties, properties);
  }

  @override
  int get hashCode => Object.hash(
        id,
        type,
        _equality.hash(properties),
      );
}
