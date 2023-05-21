
import 'python_engine_platform_interface.dart';

class PythonEngine {
  Future<String?> getPlatformVersion() {
    return PythonEnginePlatform.instance.getPlatformVersion();
  }
}
