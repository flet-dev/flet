const errorExitCode = 100;

const pythonScript = """
import os, runpy, sys, traceback

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

out_file = open("{outLogFilename}", "w+", buffering=1)

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
# then either renders the error screen (code == 100) or terminates the host
# process (any other code) using the file we wrote to above.
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
    runpy.run_module("{module_name}", run_name="__main__")
except Exception as e:
    ex = e
    traceback.print_exception(e)

sys.exit(0 if ex is None else 100)
""";
