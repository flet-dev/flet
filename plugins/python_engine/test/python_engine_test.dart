import 'package:flutter_test/flutter_test.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'package:python_engine/python_engine.dart';
import 'package:python_engine/python_engine_method_channel.dart';
import 'package:python_engine/python_engine_platform_interface.dart';

class MockPythonEnginePlatform
    with MockPlatformInterfaceMixin
    implements PythonEnginePlatform {
  @override
  Future<String?> getPlatformVersion() => Future.value('42');

  @override
  Future<String?> runPython(String modulesPath, String appModuleName) {
    // TODO: implement runPython
    throw UnimplementedError();
  }
}

void main() {
  final PythonEnginePlatform initialPlatform = PythonEnginePlatform.instance;

  test('$MethodChannelPythonEngine is the default instance', () {
    expect(initialPlatform, isInstanceOf<MethodChannelPythonEngine>());
  });

  test('getPlatformVersion', () async {
    PythonEngine pythonEnginePlugin = PythonEngine();
    MockPythonEnginePlatform fakePlatform = MockPythonEnginePlatform();
    PythonEnginePlatform.instance = fakePlatform;

    expect(await pythonEnginePlugin.getPlatformVersion(), '42');
  });
}
