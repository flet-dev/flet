import Flutter
import UIKit
import Python

class MyThread: Thread {
    let appPath: String
    init(appPath: String) {
        self.appPath = appPath
    }
    
    // Thread's starting point
    override func main() {
        Py_Initialize();
        
        // run app
        let file = fopen(self.appPath, "r")
        PyRun_SimpleFileEx(file, self.appPath, 1)
        
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
            result("iOS " + UIDevice.current.systemVersion)
        case "runPython":
            let args: [String: Any] = call.arguments as? [String: Any] ?? [:]
            let appPath = args["appPath"] as! String
            let modulePaths = args["modulePaths"] as? [String] ?? []
            let envVars = args["environmentVariables"] as? [String:String] ?? [:]
            
            print("Swift runPython(appPath: \(appPath), modulePaths: \(modulePaths))")
            
            let appDir = URL(fileURLWithPath: appPath).deletingLastPathComponent().path
            
            // bundle root path
            guard let resourcePath = Bundle(for: type(of: self)).resourcePath else { return }
            
            let pythonPaths: [String] = modulePaths + [
                "\(appDir)/__pypackages__",
                resourcePath,
                "\(resourcePath)/lib/python3.10",
                "\(resourcePath)/lib/python3.10/site-packages"
            ]

            setenv("PYTHONOPTIMIZE", "2", 1)
            setenv("PYTHONDONTWRITEBYTECODE", "1", 1)
            setenv("PYTHONNOUSERSITE", "1", 1)
            setenv("PYTHONUNBUFFERED", "1", 1)
            setenv("LC_CTYPE", "UTF-8", 1)
            
            setenv("PYTHONHOME", resourcePath, 1)
            setenv("PYTHONPATH", pythonPaths.joined(separator: ":"), 1)
            
            // custom env vars
            envVars.forEach {v in
                setenv(v.key, v.value, 1)
            }
            
            // run user pgoram in a thread
            let thread = MyThread(appPath: appPath)
            thread.start()
            
            result(0)
        default:
            result(FlutterMethodNotImplemented)
        }
    }
}
