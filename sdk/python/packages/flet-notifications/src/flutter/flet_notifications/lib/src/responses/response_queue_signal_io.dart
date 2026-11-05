import 'dart:isolate';
import 'dart:ui' show IsolateNameServer;

const String _portName = "flet_notifications_response_queue";

/// Calls [onQueued] whenever [signalResponseQueued] runs in any isolate of the
/// process, until the returned function is called.
void Function() listenForQueuedResponses(void Function() onQueued) {
  final port = ReceivePort();
  IsolateNameServer.removePortNameMapping(_portName);
  IsolateNameServer.registerPortWithName(port.sendPort, _portName);
  port.listen((_) => onQueued());
  return () {
    // A newer service may have taken over the name.
    if (IsolateNameServer.lookupPortByName(_portName) == port.sendPort) {
      IsolateNameServer.removePortNameMapping(_portName);
    }
    port.close();
  };
}

/// Tells the listening service, if any, that a response was queued.
void signalResponseQueued() {
  IsolateNameServer.lookupPortByName(_portName)?.send(null);
}
