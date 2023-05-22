import Flutter
import UIKit
import Python

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

      var math = PyImport_ImportModule("math")
      if (math == nil) {
        result(FlutterError.init(code: "NATIVE_ERR",
                                                 message: "Cannot load math module",
                                                 details: nil))
      }

      var appModule = PyImport_ImportModule(appModuleName)
      if (appModule == nil) {
        result(FlutterError.init(code: "NATIVE_ERR",
                                                 message: "Cannot load appModuleName module",
                                                 details: nil))
      }

      print("hi!")
      print("AAA\nBBBB")
      NSLog("Before\nAfter")
      NSLog("\nHello, World!")
      

      result("OK")
    default:
      result(FlutterMethodNotImplemented)
    }
  }
}
