import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

import 'python_engine_platform_interface.dart';

/// An implementation of [PythonEnginePlatform] that uses method channels.
class MethodChannelPythonEngine extends PythonEnginePlatform {
  /// The method channel used to interact with the native platform.
  @visibleForTesting
  final methodChannel = const MethodChannel('python_engine');

  @override
  Future<String?> getPlatformVersion() async {
    final version =
        await methodChannel.invokeMethod<String>('getPlatformVersion');
    return version;
  }

  @override
  Future<String?> runPython(String appPath,
      {List<String>? modulePaths,
      Map<String, String>? environmentVariables}) async {
    final Map<String, dynamic> arguments = {
      'appPath': appPath,
      'modulePaths': modulePaths,
      'environmentVariables': environmentVariables
    };
    return await methodChannel.invokeMethod<String>('runPython', arguments);
  }
}
