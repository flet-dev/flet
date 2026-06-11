import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:ui';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;
import 'package:package_info_plus/package_info_plus.dart';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart' as path_provider;
import 'package:serious_python/bridge.dart';
import 'package:serious_python/serious_python.dart';
import 'package:flutter_web_plugins/url_strategy.dart';
import 'package:window_manager/window_manager.dart';

import "python.dart";

{% for dep in cookiecutter.flutter.dependencies %}
import 'package:{{ dep }}/{{ dep }}.dart' as {{ dep }};
{% endfor %}

/*
{% set show_boot_screen = get_pyproject("tool.flet." ~ cookiecutter.options.config_platform ~ ".app.boot_screen.show")
                        or get_pyproject("tool.flet.app.boot_screen.show")
                        or False %}
{% set boot_screen_message = get_pyproject("tool.flet." ~ cookiecutter.options.config_platform ~ ".app.boot_screen.message")
                        or get_pyproject("tool.flet.app.boot_screen.message") %}

{% set show_startup_screen = get_pyproject("tool.flet." ~ cookiecutter.options.config_platform ~ ".app.startup_screen.show")
                        or get_pyproject("tool.flet.app.startup_screen.show")
                        or False %}
{% set startup_screen_message = get_pyproject("tool.flet." ~ cookiecutter.options.config_platform ~ ".app.startup_screen.message")
                        or get_pyproject("tool.flet.app.startup_screen.message") %}

{% set hide_window_on_start = get_pyproject("tool.flet." ~ cookiecutter.options.config_platform ~ ".app.hide_window_on_start")
                        or get_pyproject("tool.flet.app.hide_window_on_start") %}

show_boot_screen: {{ show_boot_screen }}
boot_screen_message: {{ boot_screen_message }}
show_startup_screen: {{ show_startup_screen }}
startup_screen_message: {{ startup_screen_message }}
hide_window_on_start: {{ hide_window_on_start }}
*/

const bool isRelease = bool.fromEnvironment('dart.vm.product');

const assetPath = "app/app.zip";
const pythonModuleName = "{{ cookiecutter.python_module_name }}";
final showAppBootScreen = bool.tryParse("{{ show_boot_screen }}".toLowerCase()) ?? false;
const appBootScreenMessage = '{{ boot_screen_message | default("Preparing the app for its first launch…", true) }}';
final showAppStartupScreen = bool.tryParse("{{ show_startup_screen }}".toLowerCase()) ?? false;
const appStartupScreenMessage = '{{ startup_screen_message | default("Getting things ready…", true) }}';
final hideWindowOnStart = bool.tryParse("{{ hide_window_on_start }}".toLowerCase()) ?? false;

List<FletExtension> extensions = [
{% for dep in cookiecutter.flutter.dependencies %}
{{ dep }}.Extension(),
{% endfor %}
];

String outLogFilename = "";

// global vars
List<String> _args = [];
String pageUrl = "";
String assetsDir = "";
String appDir = "";
Map<String, String> environmentVariables = Map.from(Platform.environment);

// In production (embedded) mode the Flet protocol flows over an in-process
// PythonBridge — no socket file, no TCP. `_exitBridge` is a separate bridge
// dedicated to Python's exit-code transmission (replaces the legacy stdout-
// callback socket). Both are null in web + developer modes where Python is
// either remote or in a separate process.
PythonBridge? _bridge;
PythonBridge? _exitBridge;

void main(List<String> args) async {

  FletDeepLinkingBootstrap.install();

  _args = List<String>.from(args);

  var devPageUrl = const String.fromEnvironment("FLET_PAGE_URL");
  if (devPageUrl != "") {
    _args.addAll([devPageUrl, "--debug"]);
  }

  for (var ext in extensions) {
    ext.ensureInitialized();
  }

  runApp(FutureBuilder(
      future: prepareApp(),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          // In production mode prepareApp() created _bridge; wire a
          // PythonBridge-backed channel so FletApp talks to the embedded
          // Python over the in-process FFI transport. In web + dev modes
          // _bridge is null and FletApp falls back to its URL-scheme factory
          // (websocket / TCP / UDS).
          final channelBuilder = _bridge == null
              ? null
              : ({
                  required FletBackendChannelOnMessageCallback onMessage,
                  required FletBackendChannelOnDisconnectCallback onDisconnect,
                }) =>
                  _DartBridgeBackendChannel(_bridge!,
                      onMessage: onMessage, onDisconnect: onDisconnect);
          // OK - start Python program
          return kIsWeb || (isDesktopPlatform() && _args.isNotEmpty)
              ? FletApp(
                  pageUrl: pageUrl,
                  assetsDir: assetsDir,
                  showAppStartupScreen: showAppStartupScreen,
                  appStartupScreenMessage: appStartupScreenMessage,
                  extensions: extensions)
              : FutureBuilder(
                  future: runPythonApp(args),
                  builder:
                      (BuildContext context, AsyncSnapshot<String?> snapshot) {
                    if (snapshot.hasData || snapshot.hasError) {
                      // error or premature finish
                      return MaterialApp(
                        builder: (context, _) => ErrorScreen(
                            title: "Error running app",
                            text: snapshot.data ?? snapshot.error.toString()),
                      );
                    } else {
                      // no result of error
                      return FletApp(
                          pageUrl: pageUrl,
                          assetsDir: assetsDir,
                          showAppStartupScreen: showAppStartupScreen,
                          appStartupScreenMessage: appStartupScreenMessage,
                          channelBuilder: channelBuilder,
                          extensions: extensions);
                    }
                  });
        } else if (snapshot.hasError) {
          // error
          return MaterialApp(
              builder: (context, _) => ErrorScreen(
                  title: "Error starting app",
                  text: snapshot.error.toString()));
        } else {
          // loading
          return MaterialApp(
              builder: (context, _) => showAppBootScreen ? const BootScreen() : const BlankScreen());
        }
      }));
}

Future prepareApp() async {
  if (!_args.contains("--debug") && isRelease) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  } else {
    _args.remove("--debug");
  }

  await setupDesktop(hideWindowOnStart: hideWindowOnStart);

  if (kIsWeb) {
    // web mode - connect via HTTP
    pageUrl = Uri.base.toString();
    var routeUrlStrategy = getFletRouteUrlStrategy();
    if (routeUrlStrategy == "path") {
      usePathUrlStrategy();
    }
    assetsDir = getAssetsDir();
  } else if (_args.isNotEmpty && isDesktopPlatform()) {
    // developer mode
    debugPrint("Flet app is running in Developer mode");
    pageUrl = _args[0];
    if (_args.length > 1) {
      var pidFilePath = _args[1];
      debugPrint("Args contain a path to PID file: $pidFilePath}");
      var pidFile = await File(pidFilePath).create();
      await pidFile.writeAsString("$pid");
    }
    if (_args.length > 2) {
      assetsDir = _args[2];
      debugPrint("Args contain a path assets directory: $assetsDir}");
    }
  } else {
    // production mode
    // extract app from asset
    appDir = await extractAssetZip(assetPath, checkHash: true);

    // set current directory to app path
    Directory.current = appDir;

    assetsDir = path.join(appDir, "assets");

    // configure apps DATA and TEMP directories
    WidgetsFlutterBinding.ensureInitialized();

    var appTempPath = (await path_provider.getApplicationCacheDirectory()).path;
    var appDataPath =
        (await path_provider.getApplicationDocumentsDirectory()).path;

    if (defaultTargetPlatform != TargetPlatform.iOS &&
        defaultTargetPlatform != TargetPlatform.android) {
      // append app name to the path and create dir
      PackageInfo packageInfo = await PackageInfo.fromPlatform();
      appDataPath = path.join(appDataPath, "flet", packageInfo.packageName);
      if (!await Directory(appDataPath).exists()) {
        await Directory(appDataPath).create(recursive: true);
      }
    }

    environmentVariables.putIfAbsent("FLET_APP_STORAGE_DATA", () => appDataPath);
    environmentVariables.putIfAbsent("FLET_APP_STORAGE_TEMP", () => appTempPath);

    outLogFilename = path.join(appTempPath, "console.log");
    environmentVariables.putIfAbsent("FLET_APP_CONSOLE", () => outLogFilename);

    environmentVariables.putIfAbsent(
        "FLET_PLATFORM", () => defaultTargetPlatform.name.toLowerCase());

    // In production we use the in-process dart_bridge FFI transport (no UDS,
    // no TCP — Python and Flutter share the process). Two bridges:
    //   _bridge      — the Flet MsgPack protocol channel (Dart ↔ Python).
    //   _exitBridge  — Python-only outbound channel carrying the exit code
    //                  when `sys.exit(code)` is called inside the embedded
    //                  interpreter. Replaces the legacy stdout-callback
    //                  socket.
    _bridge = PythonBridge();
    _exitBridge = PythonBridge();
    pageUrl = "dartbridge://${_bridge!.port}";
    environmentVariables.putIfAbsent(
        "FLET_DART_BRIDGE_PORT", () => _bridge!.port.toString());
    environmentVariables.putIfAbsent(
        "FLET_DART_BRIDGE_EXIT_PORT", () => _exitBridge!.port.toString());
  }

  if (!kIsWeb && assetsDir.isNotEmpty) {
    environmentVariables.putIfAbsent("FLET_ASSETS_DIR", () => assetsDir);
  }

  return "";
}

Future<String?> runPythonApp(List<String> args) async {
  var argvItems = args.map((a) => "\"${a.replaceAll('"', '\\"')}\"");
  var argv = "[${argvItems.isNotEmpty ? argvItems.join(',') : '""'}]";
  var script = pythonScript
      .replaceAll("{outLogFilename}", outLogFilename.replaceAll("\\", "\\\\"))
      .replaceAll('{module_name}', pythonModuleName)
      .replaceAll('{argv}', argv);

  var completer = Completer<String>();

  // Subscribe to the exit-code bridge. Python's `sys.exit(code)` is patched
  // (in python.dart) to encode `code` as raw UTF-8 bytes and post them via
  // `dart_bridge.send_bytes(FLET_DART_BRIDGE_EXIT_PORT, ...)`. We don't need
  // a streaming codec here — the channel only ever carries a single short
  // payload, then Python tears down.
  StringBuffer pythonExitBuf = StringBuffer();
  StreamSubscription<Uint8List>? exitSub;

  void onExitSignal() async {
    await exitSub?.cancel();
    int exitCode = int.tryParse(pythonExitBuf.toString().trim()) ?? 0;
    if (exitCode == errorExitCode) {
      var out = "";
      if (await File(outLogFilename).exists()) {
        out = await File(outLogFilename).readAsString();
      }
      completer.complete(out);
    } else {
      exit(exitCode);
    }
  }

  exitSub = _exitBridge!.messages.listen(
    (data) {
      pythonExitBuf.write(String.fromCharCodes(data));
      // One frame is always the full code on this channel — act on it.
      onExitSignal();
    },
    onError: (error) {
      debugPrint('Exit bridge error: $error');
      onExitSignal();
    },
    onDone: onExitSignal,
    cancelOnError: false,
  );

  // run python async
  SeriousPython.runProgram(path.join(appDir, "$pythonModuleName.pyc"),
      script: script, environmentVariables: environmentVariables);

  // wait for Python to signal exit
  return completer.future;
}

/// `FletBackendChannel` implementation backed by a [PythonBridge]. Bytes
/// flow Dart↔Python entirely in-process; no Unix socket, no kernel context
/// switch. The wire format is the same MsgPack-framed protocol the existing
/// socket-based `FletSocketBackendChannel` speaks.
class _DartBridgeBackendChannel implements FletBackendChannel {
  _DartBridgeBackendChannel(this._bridge,
      {required FletBackendChannelOnMessageCallback onMessage,
      required FletBackendChannelOnDisconnectCallback onDisconnect})
      : _onMessage = onMessage,
        _onDisconnect = onDisconnect,
        _deserializer =
            StreamingMsgpackDeserializer(extDecoder: FletMsgpackDecoder());

  final PythonBridge _bridge;
  final FletBackendChannelOnMessageCallback _onMessage;
  final FletBackendChannelOnDisconnectCallback _onDisconnect;
  final StreamingMsgpackDeserializer _deserializer;
  StreamSubscription<Uint8List>? _subscription;

  @override
  Future connect() async {
    _subscription = _bridge.messages.listen(
      _onBytes,
      onError: (error, stack) {
        debugPrint("PythonBridge stream error: $error");
        _onDisconnect();
      },
      onDone: () {
        debugPrint("PythonBridge stream closed.");
        _onDisconnect();
      },
      cancelOnError: false,
    );
  }

  void _onBytes(Uint8List bytes) {
    _deserializer.addChunk(bytes);
    final frames = _deserializer.decodeMessages();
    for (final frame in frames) {
      _onMessage(Message.fromList(frame));
    }
  }

  @override
  void send(Message message) {
    final encoded = Uint8List.fromList(
        msgpack.serialize(message.toList(), extEncoder: FletMsgpackEncoder()));
    // Retry loop covers the brief startup window where Python hasn't yet
    // called `dart_bridge.set_enqueue_handler_func` — bridge.send returns
    // false in that case. Once Flet's app.py registers the handler (which
    // happens before `runpy.run_module` is dispatched), bridge.send returns
    // true synchronously.
    if (_bridge.send(encoded)) return;
    _retrySend(encoded);
  }

  void _retrySend(Uint8List encoded) {
    const interval = Duration(milliseconds: 50);
    const deadline = Duration(seconds: 30);
    final start = DateTime.now();
    Timer.periodic(interval, (timer) {
      if (_bridge.send(encoded)) {
        timer.cancel();
      } else if (DateTime.now().difference(start) > deadline) {
        timer.cancel();
        debugPrint(
            "PythonBridge send timed out: Python handler never registered.");
      }
    });
  }

  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 0;

  @override
  void disconnect() {
    _subscription?.cancel();
    _subscription = null;
  }
}

class ErrorScreen extends StatelessWidget {
  final String title;
  final String text;

  const ErrorScreen({super.key, required this.title, required this.text});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
          child: Container(
        padding: const EdgeInsets.all(8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                TextButton.icon(
                  onPressed: () {
                    Clipboard.setData(ClipboardData(text: text));
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Copied to clipboard')),
                    );
                  },
                  icon: const Icon(
                    Icons.copy,
                    size: 16,
                  ),
                  label: const Text("Copy"),
                )
              ],
            ),
            Expanded(
                child: SingleChildScrollView(
              child: SelectableText(text,
                  style: Theme.of(context).textTheme.bodySmall),
            ))
          ],
        ),
      )),
    );
  }
}

class BootScreen extends StatelessWidget {
  const BootScreen({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(
              width: 30,
              height: 30,
              child: CircularProgressIndicator(strokeWidth: 3),
            ),
            const SizedBox(
              height: 10,
            ),
            Text(appBootScreenMessage, style: Theme.of(context).textTheme.bodySmall,)
          ],
        ),
      ),
    );
  }
}

class BlankScreen extends StatelessWidget {
  const BlankScreen({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: SizedBox.shrink(),
    );
  }
}

