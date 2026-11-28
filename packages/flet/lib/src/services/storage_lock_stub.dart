/// Native SharedPreferences updates its process-wide cache synchronously.
Future<T> withStorageLock<T>(String name, Future<T> Function() action) =>
    action();
