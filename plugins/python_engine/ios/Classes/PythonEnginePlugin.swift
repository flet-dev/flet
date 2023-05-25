import Flutter
import UIKit
import Python

class MyThread: Thread {
    let appModuleName: String
    init(appModuleName: String) {
        self.appModuleName = appModuleName
    }
    
    // Thread's starting point
    override func main() {
        Py_Initialize();
        
        let file = fopen(self.appModuleName, "r")
        //let dir = URL(fileURLWithPath: self.appModuleName).deletingLastPathComponent().path
        //chdir(dir)
        PyRun_SimpleFileEx(file, self.appModuleName, 1)
        
        Py_Finalize()
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
            let modulesPath = args["modulesPath"] as! String
            let appModuleName = args["appModuleName"] as! String
            
            print("INSIDE runPython() of plugin")
            
            // bundle root path
            guard let resourcePath = Bundle(for: type(of: self)).resourcePath else { return }

            setenv("PYTHONOPTIMIZE", "2", 1)
            setenv("PYTHONDONTWRITEBYTECODE", "1", 1)
            setenv("PYTHONNOUSERSITE", "1", 1)
            setenv("PYTHONUNBUFFERED", "1", 1)
            setenv("LC_CTYPE", "UTF-8", 1)
            
            setenv("FLET_PLATFORM", "iOS", 1)
            setenv("FLET_SERVER_UDS_PATH", "flet.sock", 1)
            
            setenv("PYTHONHOME", resourcePath, 1)
            setenv("PYTHONPATH", "\(modulesPath)/__pypackages__:\(resourcePath):\(resourcePath)/lib/python3.10:\(resourcePath)/lib/python3.10/site-packages", 1)
            
//            let math = PyImport_ImportModule("math")
//            if (math == nil) {
//                result(FlutterError.init(code: "NATIVE_ERR",
//                                         message: "Cannot load math module",
//                                         details: nil))
//            }
            
            // run user pgoram in a thread
            let thread = MyThread(appModuleName: modulesPath + "/" + appModuleName + ".py")
            thread.start()
            
            result("OK")
        default:
            result(FlutterMethodNotImplemented)
        }
    }
}
