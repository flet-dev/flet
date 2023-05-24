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
        let dir = URL(fileURLWithPath: self.appModuleName).deletingLastPathComponent().path
        chdir(dir)
        let gilCheck = PyGILState_Check()
        print("GIL CHECK: \(gilCheck)")
        PyRun_SimpleFile(file, self.appModuleName)
        fclose(file)
        
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

            print("INSIDE runPython() of plugin")
            
            guard let resourcePath = Bundle(for: type(of: self)).resourcePath else { return }
            let modulesPath = args["modulesPath"] as! String
            let appModuleName = args["appModuleName"] as! String

            setenv("PYTHONOPTIMIZE", "2", 1);
            setenv("PYTHONDONTWRITEBYTECODE", "1", 1);
            setenv("PYTHONNOUSERSITE", "1", 1);
            setenv("PYTHONUNBUFFERED", "1", 1);
            setenv("LC_CTYPE", "UTF-8", 1);
            
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
