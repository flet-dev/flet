class MacLocalAuth:
    def __init__(self) -> None:
        import ctypes
        import sys
        from LocalAuthentication import LAContext
        from LocalAuthentication import (
            LAPolicyDeviceOwnerAuthentication,
        )

        self.LAContext = LAContext
        self.LAPolicyDeviceOwnerAuthentication = LAPolicyDeviceOwnerAuthentication

        c = ctypes.cdll.LoadLibrary(None)
        PY3 = sys.version_info[0] >= 3
        if PY3:
            self.DISPATCH_TIME_FOREVER = sys.maxsize
        else:
            self.DISPATCH_TIME_FOREVER = sys.maxint
        self.kTouchIdPolicy = LAPolicyDeviceOwnerAuthentication
        self.dispatch_semaphore_create = c.dispatch_semaphore_create
        self.dispatch_semaphore_create.restype = ctypes.c_void_p
        self.dispatch_semaphore_create.argtypes = [ctypes.c_int]

        self.dispatch_semaphore_wait = c.dispatch_semaphore_wait
        self.dispatch_semaphore_wait.restype = ctypes.c_long
        self.dispatch_semaphore_wait.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

        self.dispatch_semaphore_signal = c.dispatch_semaphore_signal
        self.dispatch_semaphore_signal.restype = ctypes.c_long
        self.dispatch_semaphore_signal.argtypes = [ctypes.c_void_p]

    def is_available(self) -> bool:
        context = self.LAContext.new()
        return context.canEvaluatePolicy_error_(self.kTouchIdPolicy, None)[0]

    def authenticate_mac(self, reason="authenticate via Touch ID") -> bool:
        context = self.LAContext.new()

        sema = self.dispatch_semaphore_create(0)

        res = {"success": False, "error": None}

        def cb(_success, _error):
            res["success"] = _success
            if _error:
                res["error"] = _error.localizedDescription()
            self.dispatch_semaphore_signal(sema)

        context.evaluatePolicy_localizedReason_reply_(self.kTouchIdPolicy, reason, cb)
        self.dispatch_semaphore_wait(sema, self.DISPATCH_TIME_FOREVER)

        # if res["error"]:
        # raise Exception(res["error"])
        print('res["success"]:', res["success"])
        return res["success"]
