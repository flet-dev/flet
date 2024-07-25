from LocalAuthentication import LAContext
from LocalAuthentication import (
    LAPolicyDeviceOwnerAuthentication,
)
import ctypes
import sys

c = ctypes.cdll.LoadLibrary(None)
PY3 = sys.version_info[0] >= 3
if PY3:
    DISPATCH_TIME_FOREVER = sys.maxsize
else:
    DISPATCH_TIME_FOREVER = sys.maxint
kTouchIdPolicy = LAPolicyDeviceOwnerAuthentication
dispatch_semaphore_create = c.dispatch_semaphore_create
dispatch_semaphore_create.restype = ctypes.c_void_p
dispatch_semaphore_create.argtypes = [ctypes.c_int]

dispatch_semaphore_wait = c.dispatch_semaphore_wait
dispatch_semaphore_wait.restype = ctypes.c_long
dispatch_semaphore_wait.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

dispatch_semaphore_signal = c.dispatch_semaphore_signal
dispatch_semaphore_signal.restype = ctypes.c_long
dispatch_semaphore_signal.argtypes = [ctypes.c_void_p]


def is_available() -> bool:
    context = LAContext.new()
    return context.canEvaluatePolicy_error_(kTouchIdPolicy, None)[0]


def authenticate_mac(reason="authenticate via Touch ID") -> bool:
    kTouchIdPolicy = LAPolicyDeviceOwnerAuthentication
    context = LAContext.new()

    sema = dispatch_semaphore_create(0)

    res = {"success": False, "error": None}

    def cb(_success, _error):
        res["success"] = _success
        if _error:
            res["error"] = _error.localizedDescription()
        dispatch_semaphore_signal(sema)

    context.evaluatePolicy_localizedReason_reply_(kTouchIdPolicy, reason, cb)
    dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER)

    # if res["error"]:
    # raise Exception(res["error"])

    return res["success"]
