import 'dart:async';
import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as path;
import 'package:serious_python/serious_python.dart';
import 'package:url_strategy/url_strategy.dart';

{% for dep in cookiecutter.flutter.dependencies %}
import 'package:{{ dep }}/{{ dep }}.dart' as {{ dep }};
{% endfor %}

const bool isProduction = bool.fromEnvironment('dart.vm.product');

const assetPath = "app/app.zip";
const pythonModuleName = "{{ cookiecutter.python_module_name }}";
final hideLoadingPage =
    bool.tryParse("{{ cookiecutter.hide_loading_animation }}".toLowerCase()) ??
        true;
const outLogFilename = "out.log";
const errorExitCode = 100;

List<CreateControlFactory> createControlFactories = [
{% for dep in cookiecutter.flutter.dependencies %}
{{ dep }}.createControl,
{% endfor %}
];

const pythonScript = """
import certifi, os, runpy, socket, sys, traceback

os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

# fix for: https://github.com/flet-dev/serious-python/issues/85#issuecomment-2065000974
os.environ["OPENBLAS_NUM_THREADS"] = "1"

if os.getenv("FLET_PLATFORM") == "android":
    import ssl

    def create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None
    ):
        return ssl.create_default_context(
            purpose=purpose, cafile=certifi.where(), capath=capath, cadata=cadata
        )

    ssl._create_default_https_context = create_default_context

out_file = open("$outLogFilename", "w+", buffering=1)

callback_socket_addr = os.environ.get("FLET_PYTHON_CALLBACK_SOCKET_ADDR")
if ":" in callback_socket_addr:
    addr, port = callback_socket_addr.split(":")
    callback_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    callback_socket.connect((addr, int(port)))
else:
    callback_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    callback_socket.connect(callback_socket_addr)

sys.stdout = sys.stderr = out_file

def flet_exit(code=0):
    callback_socket.sendall(str(code).encode())
    out_file.close()
    callback_socket.close()

sys.exit = flet_exit

ex = None
try:
    runpy.run_module("{module_name}", run_name="__main__")
except Exception as e:
    ex = e
    traceback.print_exception(e)

sys.exit(0 if ex is None else $errorExitCode)
""";

// global vars
String pageUrl = "";
String assetsDir = "";
String appDir = "";
Map<String, String> environmentVariables = {};

void main() async {
  if (isProduction) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  }

  {% for dep in cookiecutter.flutter.dependencies %}
  {{ dep }}.ensureInitialized();
  {% endfor %}

  runApp(FutureBuilder(
      future: prepareApp(),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          // OK - start Python program
          return kIsWeb
              ? FletApp(
                  pageUrl: pageUrl,
                  assetsDir: assetsDir,
                  hideLoadingPage: hideLoadingPage,
                  createControlFactories: createControlFactories
                )
              : FutureBuilder(
                  future: runPythonApp(),
                  builder:
                      (BuildContext context, AsyncSnapshot<String?> snapshot) {
                    if (snapshot.hasData || snapshot.hasError) {
                      // error or premature finish
                      return MaterialApp(
                        home: ErrorScreen(
                            title: "Error running app",
                            text: snapshot.data ?? snapshot.error.toString()),
                      );
                    } else {
                      // no result of error
                      return FletApp(
                        pageUrl: pageUrl,
                        assetsDir: assetsDir,
                        hideLoadingPage: hideLoadingPage,
                        createControlFactories: createControlFactories
                      );
                    }
                  });
        } else if (snapshot.hasError) {
          // error
          return MaterialApp(
              home: ErrorScreen(
                  title: "Error starting app",
                  text: snapshot.error.toString()));
        } else {
          // loading
          return const MaterialApp(home: BlankScreen());
        }
      }));
}

Future prepareApp() async {
  if (kIsWeb) {
    // web mode - connect via HTTP
    pageUrl = Uri.base.toString();
    var routeUrlStrategy = getFletRouteUrlStrategy();
    if (routeUrlStrategy == "path") {
      setPathUrlStrategy();
    }
  } else {
    await setupDesktop();

    // extract app from asset
    appDir = await extractAssetZip(assetPath, checkHash: true);

    // set current directory to app path
    Directory.current = appDir;

    assetsDir = path.join(appDir, "assets");

    environmentVariables["FLET_PLATFORM"] =
        defaultTargetPlatform.name.toLowerCase();

    if (defaultTargetPlatform == TargetPlatform.windows) {
      // use TCP on Windows
      var tcpPort = await getUnusedPort();
      pageUrl = "tcp://localhost:$tcpPort";
      environmentVariables["FLET_SERVER_PORT"] = tcpPort.toString();
    } else {
      // use UDS on other platforms
      pageUrl = "flet.sock";
      environmentVariables["FLET_SERVER_UDS_PATH"] = pageUrl;
    }
  }

  return "";
}

Future<String?> runPythonApp() async {
  var script = pythonScript.replaceAll('{module_name}', pythonModuleName);

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
    socketAddr = "stdout.sock";
    if (await File(socketAddr).exists()) {
      await File(socketAddr).delete();
    }
    outSocketServer = await ServerSocket.bind(
        InternetAddress(socketAddr, type: InternetAddressType.unix), 0);
    debugPrint('Python output Socket Server is listening on $socketAddr');
  }

  environmentVariables["FLET_PYTHON_CALLBACK_SOCKET_ADDR"] = socketAddr;

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
