const errorExitCode = 100;

const pythonScript =
    """
import importlib.util, os, sys, traceback, types

# fix for cryptography package
os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "1"

# fix for: https://github.com/flet-dev/serious-python/issues/85#issuecomment-2065000974
os.environ["OPENBLAS_NUM_THREADS"] = "1"

def initialize_ctypes():
    import ctypes.util
    import os
    import pathlib
    import sys

    android_native_lib_dir = os.getenv("ANDROID_NATIVE_LIBRARY_DIR")

    def find_library_override_imp(name: str):
        if name is None:
            return None
        if pathlib.Path(name).exists():
            return name
        if sys.platform == "ios":
            for lf in [
                f"Frameworks/{name}.framework/{name}",
                f"Frameworks/lib{name}.framework/lib{name}",
            ]:
                lib_path = pathlib.Path(sys.executable).parent.joinpath(lf)
                if lib_path.exists():
                    return str(lib_path)
        elif android_native_lib_dir:
            for lf in [f"lib{name}.so", f"{name}.so", name]:
                lib_path = pathlib.Path(android_native_lib_dir).joinpath(lf)
                if lib_path.exists():
                    return str(lib_path)
        return None

    find_library_original = ctypes.util.find_library

    def find_library_override(name):
        return find_library_override_imp(name) or find_library_original(name)

    ctypes.util.find_library = find_library_override

    CDLL_init_original = ctypes.CDLL.__init__

    def CDLL_init_override(self, name, *args, **kwargs):
        CDLL_init_original(
            self, find_library_override_imp(name) or name, *args, **kwargs
        )

    ctypes.CDLL.__init__ = CDLL_init_override


initialize_ctypes()

out_file = open(
    {outLogFilename},
    "w+", 
    buffering=1, 
    encoding="utf-8",
    errors="backslashreplace",  # prevents encoding failures
)

# libdart_bridge >= 1.3.0 installs native-log file-like wrappers as
# sys.stdout / sys.stderr right after Py_Initialize so prints land in
# logcat (Android) / os_log (iOS) / stderr (desktop). Tee here so the
# error-screen capture file ALSO gets the output — both paths matter.
# On older libdart_bridge (no native install) `_native_*` will be the
# default text streams; the tee still works as a plain duplicate write.
_native_stdout = sys.stdout
_native_stderr = sys.stderr


class _TeeWriter:
    # The file half receives writes raw — preserves byte-for-byte parity
    # with what Python wrote, so the error-screen capture file matches a
    # plain `python` console run.
    #
    # The native (logcat / os_log) half is line-buffered so Python's
    # `print(x)` doesn't produce two log entries — CPython implements
    # `print` as `write(text)` + `write("\\n")`, and the standalone
    # newline write would otherwise show as a blank logcat row after
    # every print. We accumulate until we see "\\n", emit the line
    # without the trailing newline, and skip purely empty lines (so
    # `print()` with no args also stays out of the log).
    def __init__(self, native, file_):
        self._native = native
        self._file = file_
        self._native_buf = ""

    def write(self, text):
        if not text:
            return 0
        try:
            self._native_buf += text
            while True:
                nl = self._native_buf.find("\\n")
                if nl < 0:
                    break
                line = self._native_buf[:nl]
                self._native_buf = self._native_buf[nl + 1:]
                if line:
                    self._native.write(line)
        except Exception:
            pass
        return self._file.write(text)

    def flush(self):
        try:
            # Drain any pending partial line (no trailing newline in the
            # source stream — could happen if the user app calls
            # `sys.stdout.flush()` mid-line).
            if self._native_buf:
                self._native.write(self._native_buf)
                self._native_buf = ""
            self._native.flush()
        except Exception:
            pass
        self._file.flush()

    def isatty(self):
        return False

    def fileno(self):
        return self._file.fileno()

sys.stdout = _TeeWriter(_native_stdout, out_file)
sys.stderr = _TeeWriter(_native_stderr, out_file)

# Exit-code transport. The Dart side allocated a dedicated PythonBridge port
# (FLET_DART_BRIDGE_EXIT_PORT) and is listening on it. `flet_exit` posts the
# exit code as raw UTF-8 bytes through that bridge — the Dart side parses,
# then either renders the error screen (code == $errorExitCode) or terminates
# the host process (any other code) using the file we wrote to above.
#
# On Android process reuse (Dart VM restarts while libdart_bridge stays
# loaded), the exit-bridge port number changes. We keep `_exit_port` in a
# one-element list so the session-restart handler below can mutate it in
# place — `flet_exit` always reads the current value.
import dart_bridge  # built-in module provided by libdart_bridge
_exit_port = [int(os.environ["FLET_DART_BRIDGE_EXIT_PORT"])]

def flet_exit(code=0):
    try:
        dart_bridge.send_bytes(_exit_port[0], str(code).encode())
    finally:
        out_file.close()

sys.exit = flet_exit

# Subscribe to new-Dart-VM signals if the running libdart_bridge supports
# them (>= 1.3.0). On process reuse, the new VM's port-map carries the
# fresh exit-bridge port number; rewire so flet_exit talks to the right
# Dart side. Older libdart_bridge doesn't expose the handler — fall
# through silently and the existing single-VM behaviour holds.
_add_restart = getattr(dart_bridge, "add_session_restart_handler", None)
if _add_restart is not None:
    def _on_dart_session_restart(port_map):
        new_exit = port_map.get("exit")
        if new_exit is not None:
            _exit_port[0] = int(new_exit)
    _add_restart(_on_dart_session_restart)


def _sp_run_module_as_main(module_name):
    # Execute with `python -m module_name` semantics, but inside the real
    # sys.modules["__main__"]. `runpy.run_module(..., run_name="__main__")`
    # isn't used here, as it uses a temporary namespace, causing pickle/multiprocessing
    # not to reliably resolve top-level functions from the app module.
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        raise ImportError("module %r not found" % module_name)

    if spec.submodule_search_locations is not None:
        # Package case: `python -m pkg` executes pkg.__main__.
        main_name = module_name + ".__main__"
        spec = importlib.util.find_spec(main_name)
        if spec is None:
            raise ImportError(
                "%r is a package and cannot be directly executed: "
                "no %r module" % (module_name, main_name)
            )

    if spec.loader is None or not hasattr(spec.loader, "get_code"):
        raise ImportError("module %r cannot be executed" % module_name)

    code = spec.loader.get_code(spec.name)
    if code is None:
        raise ImportError("module %r has no executable Python code" % module_name)

    main = types.ModuleType("__main__")
    main.__dict__.update(
        __spec__=spec,
        __file__=spec.origin,
        __cached__=spec.cached,
        __loader__=spec.loader,
        __package__=spec.parent,
        __builtins__=__builtins__,
    )

    sys.modules["__main__"] = main
    sys.modules["__mp_main__"] = main  # Match multiprocessing's spawn alias for the main module.

    # Prevent re-exec'd multiprocessing children from inheriting PYTHONINSPECT, or
    # they may stay open in interactive mode after their command finishes.
    os.environ.pop("PYTHONINSPECT", None)

    exec(code, main.__dict__)


ex = None
try:
    import certifi

    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
    os.environ["SSL_CERT_FILE"] = certifi.where()

    if os.getenv("FLET_PLATFORM") == "android":
        import ssl

        def create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None
        ):
            return ssl.create_default_context(
                purpose=purpose, cafile=certifi.where(), capath=capath, cadata=cadata
            )

        ssl._create_default_https_context = create_default_context

    sys.argv = {argv}

    # multiprocessing spawn/forkserver children re-execute sys.executable. In a
    # packaged Flet app, that must be the host app binary, whose native runner
    # detects multiprocessing argv and runs Python headlessly instead of opening
    # another GUI window. Set it before user code can import multiprocessing,
    # because multiprocessing snapshots the executable during import.
    if _sp_host_exe := {host_executable}:
        sys.executable = _sp_host_exe
        sys._base_executable = _sp_host_exe

    # Execute the configured app module as the real __main__ module.
    _sp_run_module_as_main({module_name})
except Exception as e:
    ex = e
    traceback.print_exception(e)

sys.exit(0 if ex is None else $errorExitCode)
""";
