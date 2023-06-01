import 'python_engine_platform_interface.dart';

class PythonEngine {
  Future<String?> getPlatformVersion() {
    return PythonEnginePlatform.instance.getPlatformVersion();
  }

  Future<String?> runPython(String appPath,
      {List<String>? modulePaths, Map<String, String>? environmentVariables}) {
    return PythonEnginePlatform.instance.runPython(appPath,
        modulePaths: modulePaths, environmentVariables: environmentVariables);
  }
}
