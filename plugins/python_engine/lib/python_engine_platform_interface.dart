import 'package:plugin_platform_interface/plugin_platform_interface.dart';

import 'python_engine_method_channel.dart';

abstract class PythonEnginePlatform extends PlatformInterface {
  /// Constructs a PythonEnginePlatform.
  PythonEnginePlatform() : super(token: _token);

  static final Object _token = Object();

  static PythonEnginePlatform _instance = MethodChannelPythonEngine();

  /// The default instance of [PythonEnginePlatform] to use.
  ///
  /// Defaults to [MethodChannelPythonEngine].
  static PythonEnginePlatform get instance => _instance;

  /// Platform-specific implementations should set this with their own
  /// platform-specific class that extends [PythonEnginePlatform] when
  /// they register themselves.
  static set instance(PythonEnginePlatform instance) {
    PlatformInterface.verifyToken(instance, _token);
    _instance = instance;
  }

  Future<String?> getPlatformVersion() {
    throw UnimplementedError('platformVersion() has not been implemented.');
  }

  Future<String?> runPython(String modulesPath, String appModuleName) {
    throw UnimplementedError('runPython() has not been implemented.');
  }
}
