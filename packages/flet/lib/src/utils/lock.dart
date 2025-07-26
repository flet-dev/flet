import 'dart:async';

class Lock {
  Completer<void>? _completer;

  /// Lock is considered acquired if completer is not null.
  bool get isLocked => _completer != null;

  /// Acquires the lock. Waits if already locked.
  Future<void> acquire() async {
    while (_completer != null) {
      await _completer!.future; // Wait for the current lock to release
    }
    _completer = Completer<void>();
  }

  /// Releases the lock.
  void release() {
    _completer?.complete();
    _completer = null;
  }
}
