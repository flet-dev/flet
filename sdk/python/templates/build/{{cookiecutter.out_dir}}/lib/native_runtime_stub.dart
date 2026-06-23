// Web stub for `native_runtime.dart`. Selected by `main.dart`'s conditional
// import on platforms where `dart:ffi` is NOT available (web).
//
// All callers must guard with `kIsWeb` so the real native_runtime entry
// points are never invoked on web — but the stubs still need to exist for
// the file to compile.

import 'package:flet/flet.dart';

String initBridges(Map<String, String> envVars) =>
    throw UnsupportedError("Native bridges not available on web");

bool get bridgesActive => false;

/// Always false on web — there's no embedded CPython to be "already
/// running". Mirrors `native_runtime.dart`'s getter so `main.dart`'s
/// process-reuse check compiles for the web target.
bool get pythonAlreadyRunning => false;

Future<String> getAppDir() =>
    throw UnsupportedError("App directory not available on web");

FletBackendChannelBuilder? get channelBuilder => null;

DataChannelFactory? get dataChannelFactory => null;

Future<String?> runPython({
  required String moduleName,
  required String appDir,
  required String outLogFilename,
  required Map<String, String> environmentVariables,
  required List<String> args,
}) => throw UnsupportedError("Native runtime not available on web");
