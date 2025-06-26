import 'dart:core';

import 'package:flutter/material.dart';

class WeakValueMap<K, V extends Object> {
  final Map<K, _TrackedValue<V>> _map = {};
  late final Finalizer<K> _finalizer;

  WeakValueMap() {
    _finalizer = Finalizer((key) {
      debugPrint("WeakValueMap.finalizer: $key");
      _map.remove(key);
    });
  }

  void set(K key, V value) {
    // Detach old value if present
    final existing = _map[key];
    if (existing != null) {
      _finalizer.detach(existing.detachToken);
    }

    final tracked = _TrackedValue(value);
    _map[key] = tracked;

    // Attach finalizer to the actual object, using a unique token
    _finalizer.attach(value, key, detach: tracked.detachToken);
  }

  V? get(K key) => _map[key]?.ref.target;

  void remove(K key) {
    debugPrint("WeakValueMap.remove: $key");
    final tracked = _map.remove(key);
    if (tracked != null) {
      _finalizer.detach(tracked.detachToken);
    }
  }

  int get length => _map.length;
}

class _TrackedValue<V extends Object> {
  final WeakReference<V> ref;
  final Object detachToken = Object();

  _TrackedValue(V value) : ref = WeakReference(value);
}
