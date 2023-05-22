import 'python_engine_platform_interface.dart';

class PythonEngine {
  Future<String?> getPlatformVersion() {
    return PythonEnginePlatform.instance.getPlatformVersion();
  }

  Future<String?> runPython(String modulesPath, String appModuleName) {
    return PythonEnginePlatform.instance.runPython(modulesPath, appModuleName);
  }
}
