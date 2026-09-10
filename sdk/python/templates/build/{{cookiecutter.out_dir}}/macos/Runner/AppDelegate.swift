import Cocoa
import FlutterMacOS

// See main.swift for the entry point.

class AppDelegate: FlutterAppDelegate {
  override func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
    return true
  }

  override func applicationSupportsSecureRestorableState(_ app: NSApplication) -> Bool {
    return true
  }

  // NSApplication posts NSApplicationWillTerminateNotification immediately
  // before calling exit(), which runs __cxa_finalize_ranges and destroys the
  // C++ statics inside every loaded CPython extension module - pybind11 type
  // caster maps in matplotlib's ft2font, numpy's internals, and so on. The
  // embedded interpreter runs on a detached thread that is very likely still
  // executing at this point (an app with a render loop essentially always is),
  // and faults on whichever destroyed static it touches next.
  //
  // _exit skips the teardown entirely. Nothing here needs to be cleaned up
  // that the kernel will not reclaim, and see the termination contract in
  // docs/publish/macos.md: an exiting app makes no promise to run atexit
  // handlers or flush pending buffered writes.
  //
  // 0 is not overriding a requested status: -[NSApplication terminate:] always
  // exits 0, and the notification carries no exit code. A Python-requested exit
  // does not come through here - it goes through native_runtime.dart, which
  // hard-exits with the real code.
  override func applicationWillTerminate(_ notification: Notification) {
    _exit(0)
  }
}
