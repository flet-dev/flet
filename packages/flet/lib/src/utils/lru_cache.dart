class LruCache<K, V> {
  LruCache(this.capacity) : assert(capacity > 0);
  final int capacity;
  final _map = <K, V>{};

  V? get(K key) {
    final val = _map.remove(key);
    if (val != null) _map[key] = val; // mark MRU
    return val;
  }

  void set(K key, V value) {
    if (_map.containsKey(key)) {
      _map.remove(key);
    } else if (_map.length >= capacity) {
      _map.remove(_map.keys.first); // evict LRU
    }
    _map[key] = value;
  }
}
