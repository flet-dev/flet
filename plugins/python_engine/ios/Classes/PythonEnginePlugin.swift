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
      guard let stdLibPath = Bundle(for: type(of: self)).path(forResource: "python-stdlib", ofType: nil) else { return }
      guard let libDynloadPath = Bundle(for: type(of: self)).path(forResource: "python-stdlib/lib-dynload", ofType: nil) else { return }
      setenv("PYTHONHOME", stdLibPath, 1)
      setenv("PYTHONPATH", "\(stdLibPath):\(libDynloadPath)", 1)

      var preconfig: PyPreConfig = PyPreConfig()
      var config: PyConfig = PyConfig()

      PyPreConfig_InitIsolatedConfig(&preconfig)
      PyConfig_InitIsolatedConfig(&config)

      Py_Initialize()

      let ws = Py_DecodeLocale("Test", nil)

      result("iOS " + stdLibPath)
    default:
      result(FlutterMethodNotImplemented)
    }
  }
}
