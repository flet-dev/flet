import Cocoa

// Python's multiprocessing spawn/forkserver paths, including the resource
// tracker, create child processes by re-executing sys.executable with a
// CPython-style command line. In a flet-built macOS app, sys.executable is this
// app binary. Detect that argv shape before AppKit/Flutter initialization and
// run the embedded interpreter headlessly instead of starting another GUI app.
// See: https://github.com/flet-dev/flet/issues/4283
//
// These optional entry points live in dart_bridge, which is force-loaded into
// the host binary by serious_python_darwin. Resolve them dynamically from the
// current process image, similar to Dart FFI's DynamicLibrary.process(), so apps
// built with older dart_bridge versions still link and launch; they just won't
// have multiprocessing child interception.
private typealias SPArgvFn = @convention(c) (
  Int32, UnsafeMutablePointer<UnsafeMutablePointer<CChar>?>?
) -> Int32

private let processHandle = dlopen(nil, RTLD_NOW)

private func spResolve(_ name: String) -> SPArgvFn? {
  guard let processHandle,
        let sym = dlsym(processHandle, name) else {
    return nil
  }
  return unsafeBitCast(sym, to: SPArgvFn.self)
}

if let isMpInvocation = spResolve("serious_python_is_mp_invocation"),
   let runPythonMain = spResolve("serious_python_main"),
   isMpInvocation(CommandLine.argc, CommandLine.unsafeArgv) != 0
{
  exit(runPythonMain(CommandLine.argc, CommandLine.unsafeArgv))
}

// Not a multiprocessing child process, or the interception hooks are unavailable:
// continue with the normal macOS Flutter app launch.
_ = NSApplicationMain(CommandLine.argc, CommandLine.unsafeArgv)
