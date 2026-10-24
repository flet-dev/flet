/// Calls [onQueued] whenever [signalTapQueued] runs, until the returned function
/// is called.
void Function() listenForQueuedTaps(void Function() onQueued) => () {};

/// Tells the listening service, if any, that a response was queued.
void signalTapQueued() {}
