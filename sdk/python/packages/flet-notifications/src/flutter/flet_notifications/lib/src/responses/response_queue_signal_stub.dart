/// Calls [onQueued] whenever [signalResponseQueued] runs, until the returned function
/// is called.
void Function() listenForQueuedResponses(void Function() onQueued) => () {};

/// Tells the listening service, if any, that a response was queued.
void signalResponseQueued() {}
