const errorExitCode = 100;

const pythonScript = """
import os, runpy, socket, sys, traceback

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

callback_socket_addr = os.getenv("FLET_PYTHON_CALLBACK_SOCKET_ADDR")
if ":" in callback_socket_addr:
    addr, port = callback_socket_addr.split(":")
    callback_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    callback_socket.connect((addr, int(port)))
else:
    callback_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    callback_socket.connect(callback_socket_addr)

sys.stdout = sys.stderr = out_file

def flet_exit(code=0):
    callback_socket.sendall(str(code).encode())
    out_file.close()
    callback_socket.close()

sys.exit = flet_exit

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
