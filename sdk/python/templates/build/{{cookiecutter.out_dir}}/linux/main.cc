#include "my_application.h"

#include <dlfcn.h>

// Python's multiprocessing spawn/forkserver paths, including the resource
// tracker, create child processes by re-executing sys.executable with a
// CPython-style command line. In a flet-built Linux app, sys.executable is this
// app binary. Detect that argv shape before GTK/Flutter initialization and run
// the embedded interpreter headlessly instead of starting another GUI app.
// See: https://github.com/flet-dev/flet/issues/4283
//
// These optional entry points live in libdart_bridge.so. Load the bridge early
// and resolve them dynamically so apps built with older dart_bridge versions
// still launch; they just won't have multiprocessing child interception.
//
// Returns true when this process was handled as a multiprocessing child. In
// that case, exit_code receives the interpreter process exit code.
static bool maybe_run_python_child(int argc, char** argv, int& exit_code) {
  typedef int (*sp_argv_fn)(int, char**);

  // The shared library, and its Python dependency, would be loaded moments
  // later by the plugin anyway, so eagerly loading it here does not add
  // meaningful cost to the normal startup path.
  void* bridge = dlopen("libdart_bridge.so", RTLD_NOW);
  if (!bridge) {
    return false;
  }

  auto is_mp_invocation = reinterpret_cast<sp_argv_fn>(
      dlsym(bridge, "serious_python_is_mp_invocation"));
  auto run_python_main =
      reinterpret_cast<sp_argv_fn>(dlsym(bridge, "serious_python_main"));

  if (is_mp_invocation && run_python_main &&
      is_mp_invocation(argc, argv) != 0) {
    exit_code = run_python_main(argc, argv);
    return true;
  }

  return false;
}

int main(int argc, char** argv) {
  // Multiprocessing child re-exec? Run it headlessly and exit, instead of starting Flutter GUI.
  int mp_exit_code = 0;
  if (maybe_run_python_child(argc, argv, mp_exit_code)) {
    return mp_exit_code;
  }

  g_autoptr(MyApplication) app = my_application_new();
  return g_application_run(G_APPLICATION(app), argc, argv);
}
