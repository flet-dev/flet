import 'dart:core';

import 'package:flutter/material.dart';

class WeakValueMap<K, V extends Object> {
  final Map<K, WeakReference<V>> _map = {};
  late final Finalizer<K> _finalizer;

  WeakValueMap() {
    _finalizer = Finalizer((key) {
      _map.remove(key);
    });
  }

  void set(K key, V value) {
    var ref = WeakReference(value);
    _map[key] = ref;
    _finalizer.attach(value, key);
  }

  V? get(K key) => _map[key]?.target;

  void remove(K key) {
    debugPrint("WeakValueMap.remove: $key");
    var ref = _map.remove(key);
    if (ref?.target != null) {
      _finalizer.detach(ref?.target as Object);
    }
  }

  int get length => _map.length;
}
