import Flutter
import UIKit
import Python

class MyThread: Thread {
    let appModuleName: String
    init(appModuleName: String) {
        self.appModuleName = appModuleName
    }
    override func main() { // Thread's starting point
        //var appModule = PyImport_ImportModule(self.appModuleName)
        let file = fopen(self.appModuleName, "r")
        Py_Initialize()
        let dir = URL(fileURLWithPath: self.appModuleName).deletingLastPathComponent().path
        chdir(dir)
        PyRun_SimpleFile(file, self.appModuleName)
        Py_Finalize()
        fclose(file)
    }
}

public class PythonEnginePlugin: NSObject, FlutterPlugin {
    
    public static func register(with registrar: FlutterPluginRegistrar) {
        let channel = FlutterMethodChannel(name: "python_engine", binaryMessenger: registrar.messenger())
        let instance = PythonEnginePlugin()
        registrar.addMethodCallDelegate(instance, channel: channel)
    }
    
    public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
        switch call.method {
        case "getPlatformVersion":
            result("iOS 1.0.0")
        case "runPython":
            let args: [String: Any] = call.arguments as? [String: Any] ?? [:]
            
            guard let stdLibPath = Bundle(for: type(of: self)).path(forResource: "python-stdlib", ofType: nil) else { return }
            guard let libDynloadPath = Bundle(for: type(of: self)).path(forResource: "python-stdlib/lib-dynload", ofType: nil) else { return }
            let modulesPath = args["modulesPath"] as! String
            let appModuleName = args["appModuleName"] as! String
            
            setenv("PYTHONHOME", stdLibPath, 1)
            setenv("PYTHONPATH", "\(modulesPath):\(stdLibPath):\(libDynloadPath)", 1)
            
            var preconfig: PyPreConfig = PyPreConfig()
            var config: PyConfig = PyConfig()
            
            PyPreConfig_InitIsolatedConfig(&preconfig)
            PyConfig_InitIsolatedConfig(&config)
            
            Py_Initialize()
            
            let ws = Py_DecodeLocale("Test", nil)
            PyMem_RawFree(ws)
            
            let math = PyImport_ImportModule("math")
            if (math == nil) {
                result(FlutterError.init(code: "NATIVE_ERR",
                                         message: "Cannot load math module",
                                         details: nil))
            }
            
            // run user pgoram in a thread
            let thread = MyThread(appModuleName: modulesPath + "/" + appModuleName + ".py")
            thread.start()
            
            result("OK")
        default:
            result(FlutterMethodNotImplemented)
        }
    }
}
