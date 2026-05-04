import 'dart:async';
import 'dart:io';
import 'dart:ui';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart' as path_provider;
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

    if (defaultTargetPlatform == TargetPlatform.windows) {
      // use TCP on Windows
      var tcpPort = await getUnusedPort();
      pageUrl = "tcp://localhost:$tcpPort";
      environmentVariables.putIfAbsent("FLET_SERVER_PORT", () => tcpPort.toString());
    } else {
      // use UDS on other platforms
      pageUrl = "flet_$pid.sock";
      environmentVariables.putIfAbsent("FLET_SERVER_UDS_PATH", () => pageUrl);
    }
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

  ServerSocket outSocketServer;
  String socketAddr = "";
  StringBuffer pythonOut = StringBuffer();

  if (defaultTargetPlatform == TargetPlatform.windows) {
    var tcpAddr = "127.0.0.1";
    outSocketServer = await ServerSocket.bind(tcpAddr, 0);
    debugPrint(
        'Python output TCP Server is listening on port ${outSocketServer.port}');
    socketAddr = "$tcpAddr:${outSocketServer.port}";
  } else {
    socketAddr = "stdout_$pid.sock";
    if (await File(socketAddr).exists()) {
      await File(socketAddr).delete();
    }
    outSocketServer = await ServerSocket.bind(
        InternetAddress(socketAddr, type: InternetAddressType.unix), 0);
    debugPrint('Python output Socket Server is listening on $socketAddr');
  }

  environmentVariables.putIfAbsent("FLET_PYTHON_CALLBACK_SOCKET_ADDR", () => socketAddr);

  void closeOutServer() async {
    outSocketServer.close();

    int exitCode = int.tryParse(pythonOut.toString().trim()) ?? 0;

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

  outSocketServer.listen((client) {
    debugPrint(
        'Connection from: ${client.remoteAddress.address}:${client.remotePort}');
    client.listen((data) {
      var s = String.fromCharCodes(data);
      pythonOut.write(s);
    }, onError: (error) {
      client.close();
      closeOutServer();
    }, onDone: () {
      client.close();
      closeOutServer();
    });
  });

  // run python async
  SeriousPython.runProgram(path.join(appDir, "$pythonModuleName.pyc"),
      script: script, environmentVariables: environmentVariables);

  // wait for client connection to close
  return completer.future;
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

Future<int> getUnusedPort() {
  return ServerSocket.bind("127.0.0.1", 0).then((socket) {
    var port = socket.port;
    socket.close();
    return port;
  });
}
