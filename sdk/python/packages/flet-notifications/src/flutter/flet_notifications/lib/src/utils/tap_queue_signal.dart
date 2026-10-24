/// Wakes the service when a background isolate queues a notification response.
///
/// Background isolates run in the app's process, so they reach the main isolate
/// through [IsolateNameServer]. The web has no background isolates, and no
/// `dart:isolate`.
library;

export 'tap_queue_signal_stub.dart'
    if (dart.library.io) 'tap_queue_signal_io.dart';
