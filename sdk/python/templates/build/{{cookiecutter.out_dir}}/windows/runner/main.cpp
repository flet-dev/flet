#include <flutter/dart_project.h>
#include <flutter/flutter_view_controller.h>
#include <shellapi.h>
#include <windows.h>

#include "flutter_window.h"
#include "utils.h"

// Python's multiprocessing spawn path, including the resource tracker, creates
// child processes by re-executing sys.executable with a CPython-style command
// line. In a flet-built Windows app, sys.executable is this app binary. Detect
// that argv shape before Win32 window/COM/Flutter initialization and run the
// embedded interpreter headlessly instead of starting another GUI app.
// See: https://github.com/flet-dev/flet/issues/4283
//
// These optional entry points live in dart_bridge.dll. Load the bridge early
// and resolve them dynamically so apps built with older dart_bridge versions
// still launch; they just won't have multiprocessing child interception.
//
// Returns true when this process was handled as a multiprocessing child. In
// that case, exit_code receives the interpreter process exit code.
static bool MaybeRunPythonChild(int& exit_code) {
  using SpArgvFn = int (*)(int, wchar_t **);

  int argc = 0;
  wchar_t **argv = ::CommandLineToArgvW(::GetCommandLineW(), &argc);
  if (!argv) {
    return false;
  }

  bool handled = false;

  // The DLL, and its python3XX.dll dependency, would be loaded moments later by
  // the plugin anyway, so eagerly loading it here does not add meaningful cost
  // to the normal startup path.
  HMODULE bridge = ::LoadLibraryW(L"dart_bridge.dll");
  if (!bridge) {
    bridge = ::LoadLibraryW(L"dart_bridge_d.dll");
  }

  if (bridge) {
    auto is_mp_invocation = reinterpret_cast<SpArgvFn>(
        ::GetProcAddress(bridge, "serious_python_is_mp_invocation_w"));
    auto run_python_main = reinterpret_cast<SpArgvFn>(
        ::GetProcAddress(bridge, "serious_python_main_w"));

    if (is_mp_invocation && run_python_main &&
        is_mp_invocation(argc, argv) != 0) {
      exit_code = run_python_main(argc, argv);
      handled = true;
    }
  }

  ::LocalFree(argv);
  return handled;
}

int APIENTRY wWinMain(_In_ HINSTANCE instance, _In_opt_ HINSTANCE prev,
                      _In_ wchar_t *command_line, _In_ int show_command) {
  // Multiprocessing child re-exec? Run it headlessly and exit, instead of starting Flutter GUI.
  int mp_exit_code = 0;
  if (MaybeRunPythonChild(mp_exit_code)) {
    return mp_exit_code;
  }

  // Attach to console when present (e.g., 'flutter run') or create a
  // new console when running with a debugger.
  if (!::AttachConsole(ATTACH_PARENT_PROCESS) && ::IsDebuggerPresent()) {
    CreateAndAttachConsole();
  }

  // Initialize COM, so that it is available for use in the library and/or
  // plugins.
  ::CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);

  flutter::DartProject project(L"data");

  std::vector<std::string> command_line_arguments =
      GetCommandLineArguments();

  project.set_dart_entrypoint_arguments(std::move(command_line_arguments));

  FlutterWindow window(project);
  Win32Window::Point origin(10, 10);
  Win32Window::Size size(1280, 720);
  if (!window.Create(L"{{ cookiecutter.product_name }}", origin, size)) {
    return EXIT_FAILURE;
  }
  window.SetQuitOnClose(true);

  ::MSG msg;
  while (::GetMessage(&msg, nullptr, 0, 0)) {
    ::TranslateMessage(&msg);
    ::DispatchMessage(&msg);
  }

  ::CoUninitialize();
  return EXIT_SUCCESS;
}
