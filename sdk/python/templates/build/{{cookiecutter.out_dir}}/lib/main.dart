import 'dart:async';
import 'dart:io';
import 'dart:ui';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart' as path_provider;
import 'package:flutter_web_plugins/url_strategy.dart';
import 'package:window_manager/window_manager.dart';

// `dart:ffi` (and therefore `package:serious_python/bridge.dart`,
// `package:serious_python/serious_python.dart`) isn't available on web.
// The conditional import below loads the real PythonBridge-backed runtime
// on platforms where FFI exists; on web it resolves to a stub of the same
// shape that just throws if invoked. `main` guards every use with
// `kIsWeb` so the stub is never actually called.
import 'native_runtime_stub.dart'
    if (dart.library.ffi) 'native_runtime.dart' as nrt;

// All build-time (cookiecutter / jinja) declarations — extension imports and
// list, python module name, boot screen config — live in this generated file
// so that main.dart stays plain, editable Dart.
import 'flet_generated.dart';

const bool isRelease = bool.fromEnvironment('dart.vm.product');

// Drives the boot screen before any FletBackend exists. Seeded to `startingUp`
// so the "preparing" stage never flashes on platforms/launches that don't
// unpack the app bundle. Only Android's first launch after install/update
// actually unpacks (see `_boot`), and only then is it switched to `preparing`.
final ValueNotifier<BootStatus> _bootStatus =
    ValueNotifier<BootStatus>(const BootStatus(BootStage.startingUp));

String outLogFilename = "";

// global vars
List<String> _args = [];
String pageUrl = "";
String assetsDir = "";
String appDir = "";
Map<String, String> environmentVariables = Map.from(Platform.environment);

void main(List<String> args) async {
  // On web the URL strategy must be selected before ANYTHING reads the initial
  // location: FletDeepLinkingBootstrap.install() (below) calls
  // WidgetsFlutterBinding.ensureInitialized() and starts observing route pushes,
  // and the first runApp() wires up the router. Whatever strategy is active at
  // that point latches how the cold-start URL maps to a route — under Flutter's
  // default hash strategy a hard refresh of `/apps/x` reads an empty fragment
  // (route "/"), so the deep link is lost and the app rewrites the URL to "/".
  // Applying the strategy that `flet build` baked into window.flet here, as the
  // very first statement, keeps both the running URLs (no `/#/`) and cold-start
  // deep links on the path strategy.
  if (kIsWeb && getFletRouteUrlStrategy() == "path") {
    usePathUrlStrategy();
  }

  FletDeepLinkingBootstrap.install();

  _args = List<String>.from(args);

  var devPageUrl = const String.fromEnvironment("FLET_PAGE_URL");
  if (devPageUrl != "") {
    _args.addAll([devPageUrl, "--debug"]);
  }

  for (var ext in extensions) {
    ext.ensureInitialized();
  }

  if (const bool.fromEnvironment("FLET_TEST")) {
    // Under integration test (`flet test`), `BootHost` (a StatefulWidget whose
    // initState awaits prepareApp() then setState()s) deadlocks the
    // WidgetTester: `tester.pump()` blocks waiting for a frame that never
    // arrives during this boot. Use the simpler FutureBuilder boot path (no
    // animated boot-screen overlay), which the tester drives cleanly. The app
    // itself — embedded Python over dart_bridge, FletApp — is identical.
    runApp(FutureBuilder(
      future: prepareApp(),
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const SizedBox.shrink();
        }
        if (kIsWeb || (isDesktopPlatform() && _args.isNotEmpty)) {
          return FletApp(
            pageUrl: pageUrl,
            assetsDir: assetsDir,
            bootScreenName: bootScreenName,
            bootScreenOptions: bootScreenOptions,
            bootStatus: _bootStatus,
            extensions: extensions,
          );
        }
        return _ProdApp(args: args);
      },
    ));
    return;
  }

  runApp(BootHost(args: args));
}

/// Hosts the app together with a persistent boot screen overlay.
///
/// The boot screen is rendered once, at a fixed position above the app tree, so
/// its animation runs continuously across both boot phases (preparing → starting
/// up) instead of restarting when `prepareApp()` completes and the app tree is
/// built underneath. The overlay fades out once the app reports it is ready.
class BootHost extends StatefulWidget {
  final List<String> args;

  const BootHost({super.key, required this.args});

  @override
  State<BootHost> createState() => _BootHostState();
}

class _BootHostState extends State<BootHost> {
  bool _prepared = false;

  @override
  void initState() {
    super.initState();
    _boot();
  }

  Future<void> _boot() async {
    // The "preparing" stage is only meaningful while the app bundle is being
    // unpacked, which happens on Android's first launch after install/update.
    // Everywhere else prepareApp() is fast, so staying in `startingUp` avoids
    // flashing "Preparing…" every launch. Only switch to `preparing` if
    // prepareApp is actually slow on Android (i.e. it's unpacking).
    Timer? preparingTimer;
    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      preparingTimer = Timer(const Duration(milliseconds: 400), () {
        _bootStatus.value = const BootStatus(BootStage.preparing);
      });
    }
    try {
      await prepareApp();
    } catch (e) {
      preparingTimer?.cancel();
      _bootStatus.value = BootStatus(BootStage.preparing, error: e.toString());
      return;
    }
    preparingTimer?.cancel();
    // Unpacking (if any) is done — hand off to the starting-up stage.
    _bootStatus.value = const BootStatus(BootStage.startingUp);
    if (!mounted) return;
    setState(() => _prepared = true);
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.ltr,
      child: Stack(
        children: [
          // The app builds underneath the overlay; while preparing it is just
          // an empty placeholder (the opaque overlay covers it anyway).
          _prepared ? _buildApp() : const SizedBox.shrink(),
          _BootOverlay(status: _bootStatus),
        ],
      ),
    );
  }

  Widget _buildApp() {
    // In web + dev modes FletApp connects over its URL-scheme transport
    // (websocket / TCP / UDS). In production prepareApp() created the native
    // FFI bridges and we additionally run the embedded Python program.
    if (kIsWeb || (isDesktopPlatform() && _args.isNotEmpty)) {
      return FletApp(
        pageUrl: pageUrl,
        assetsDir: assetsDir,
        bootScreenName: bootScreenName,
        bootScreenOptions: bootScreenOptions,
        bootStatus: _bootStatus,
        extensions: extensions,
      );
    }
    return _ProdApp(args: widget.args);
  }
}

/// Production host: runs the embedded Python program alongside [FletApp] over
/// the in-process PythonBridge FFI transport. If the program exits or errors,
/// the failure is surfaced on the boot screen via [_bootStatus].
class _ProdApp extends StatefulWidget {
  final List<String> args;

  const _ProdApp({required this.args});

  @override
  State<_ProdApp> createState() => _ProdAppState();
}

class _ProdAppState extends State<_ProdApp> {
  @override
  void initState() {
    super.initState();
    // A completed future means the Python program returned/exited prematurely
    // (it normally runs the event loop until the app quits). On process reuse
    // runPythonApp() returns a never-completing future, so this never fires.
    runPythonApp(widget.args).then((result) {
      if (!mounted) return;
      _bootStatus.value = BootStatus(BootStage.startingUp,
          error: result ?? "The app exited unexpectedly.");
    }).catchError((Object e) {
      if (!mounted) return;
      _bootStatus.value = BootStatus(BootStage.startingUp, error: e.toString());
    });
  }

  @override
  Widget build(BuildContext context) {
    return FletApp(
      pageUrl: pageUrl,
      assetsDir: assetsDir,
      bootScreenName: bootScreenName,
      bootScreenOptions: bootScreenOptions,
      bootStatus: _bootStatus,
      // PythonBridge-backed protocol channel + dedicated byte channels.
      channelBuilder: nrt.channelBuilder,
      dataChannelFactory: nrt.dataChannelFactory,
      extensions: extensions,
    );
  }
}

/// Persistent boot screen overlay. Renders the boot screen once (so its
/// animation never remounts across boot phases), then fades out when [status]
/// reports `done`. Once dismissed it stays gone — later reconnects are handled
/// by the app's own loading UI.
class _BootOverlay extends StatefulWidget {
  final ValueNotifier<BootStatus> status;

  const _BootOverlay({required this.status});

  @override
  State<_BootOverlay> createState() => _BootOverlayState();
}

class _BootOverlayState extends State<_BootOverlay> {
  bool _fadingOut = false;
  bool _removed = false;

  @override
  void initState() {
    super.initState();
    widget.status.addListener(_onStatus);
    _onStatus();
  }

  void _onStatus() {
    if (_fadingOut || !widget.status.value.done) return;
    // With a zero fade duration the AnimatedOpacity below completes
    // synchronously, firing onEnd (and its setState) in the middle of this
    // widget's own rebuild, which trips the framework's `!_dirty` assert in
    // debug mode. Skip the animation and remove the overlay in one step.
    final fadeMs = parseInt(bootScreenOptions["fade_out_duration"], 0)!;
    setState(() {
      _fadingOut = true;
      if (fadeMs == 0) _removed = true;
    });
  }

  @override
  void dispose() {
    widget.status.removeListener(_onStatus);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_removed) return const SizedBox.shrink();
    // Fade-out duration (ms) when the app becomes ready; 0 (default) = instant.
    final fadeMs = parseInt(bootScreenOptions["fade_out_duration"], 0)!;
    return IgnorePointer(
      ignoring: _fadingOut,
      child: AnimatedOpacity(
        opacity: _fadingOut ? 0.0 : 1.0,
        duration: Duration(milliseconds: fadeMs),
        onEnd: () {
          if (_fadingOut && !_removed) setState(() => _removed = true);
        },
        // resolveBootScreen is built once here (status changes update the
        // message via the screen's own ValueListenableBuilder), so the spinner
        // keeps animating across preparing → starting up.
        // Use `builder:` rather than `home:` so this MaterialApp creates NO
        // Navigator. A MaterialApp with `home` builds a Navigator with
        // `reportsRouteUpdateToEngine: true`, which pushes the home route "/"
        // to the browser URL on mount — clobbering a cold-start deep link
        // (e.g. `/gallery`) before FletApp's real router reads it. The boot
        // overlay never navigates, so it doesn't need a Navigator; this keeps
        // theme/Directionality while leaving the URL untouched.
        child: MaterialApp(
          debugShowCheckedModeBanner: false,
          builder: (context, _) => resolveBootScreen(
            name: bootScreenName,
            options: bootScreenOptions,
            extensions: extensions,
            status: widget.status,
          ),
        ),
      ),
    );
  }
}

Future prepareApp() async {
  if (!_args.contains("--debug") && isRelease) {
    // ignore: avoid_returning_null_for_void
    debugPrint = (String? message, {int? wrapWidth}) => null;
  } else {
    _args.remove("--debug");
  }

  // Linux desktop integration tests run under xvfb; waiting for the native
  // ready-to-show callback can keep WidgetTester from reaching the remote
  // tester connection.
  await setupDesktop(
    hideWindowOnStart: hideWindowOnStart,
    waitUntilReadyToShow:
        !(const bool.fromEnvironment("FLET_TEST") &&
            defaultTargetPlatform == TargetPlatform.linux),
  );

  if (kIsWeb) {
    // web mode - connect via HTTP. The URL strategy is applied in main() before
    // runApp(); doing it here would be too late (see the note there).
    pageUrl = Uri.base.toString();
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
    // resolve the app dir from the bundle (Android unpacks app.zip on first launch)
    appDir = await nrt.getAppDir();

    assetsDir = path.join(appDir, "assets");

    // configure the app's storage directories
    WidgetsFlutterBinding.ensureInitialized();

    // FLET_APP_STORAGE_DATA — durable, app-private; also the cwd. Lives under
    // the OS application-support dir (NOT the app bundle, which is read-only),
    // so relative file writes / SQLite work and persist across app updates.
    var appDataPath = path.join(
        (await path_provider.getApplicationSupportDirectory()).path, "data");
    if (!await Directory(appDataPath).exists()) {
      await Directory(appDataPath).create(recursive: true);
    }
    Directory.current = appDataPath;

    // FLET_APP_STORAGE_CACHE — regenerable; the OS may purge it.
    var appCachePath = (await path_provider.getApplicationCacheDirectory()).path;
    // FLET_APP_STORAGE_TEMP — volatile OS temp; may vanish between launches.
    var appTempPath = (await path_provider.getTemporaryDirectory()).path;

    environmentVariables.putIfAbsent("FLET_APP_STORAGE_DATA", () => appDataPath);
    environmentVariables.putIfAbsent(
        "FLET_APP_STORAGE_CACHE", () => appCachePath);
    environmentVariables.putIfAbsent("FLET_APP_STORAGE_TEMP", () => appTempPath);

    outLogFilename = path.join(appCachePath, "console.log");
    environmentVariables.putIfAbsent("FLET_APP_CONSOLE", () => outLogFilename);

    environmentVariables.putIfAbsent(
        "FLET_PLATFORM", () => defaultTargetPlatform.name.toLowerCase());

    // In production we use the in-process dart_bridge FFI transport (no UDS,
    // no TCP — Python and Flutter share the process). Two bridges, both
    // owned by `native_runtime.dart`:
    //   protocol bridge — the Flet MsgPack channel (Dart ↔ Python).
    //   exit bridge     — Python-only outbound channel carrying the exit
    //                     code when `sys.exit(code)` is called inside the
    //                     embedded interpreter. Replaces the legacy
    //                     stdout-callback socket.
    pageUrl = nrt.initBridges(environmentVariables);
  }

  if (!kIsWeb && assetsDir.isNotEmpty) {
    environmentVariables.putIfAbsent("FLET_ASSETS_DIR", () => assetsDir);
  }

  return "";
}

Future<String?> runPythonApp(List<String> args) async {
  // Process-reuse path: Android may keep the OS process alive across a
  // back-button quit and restart only the Dart VM. libdart_bridge stays
  // loaded, Python is still up. `initBridges()` already fired
  // `dart_bridge_signal_dart_session` with the new ports — Python's
  // session-restart handlers have rewired by now. Don't call into
  // `SeriousPython.runProgram` again (it would no-op-return immediately
  // anyway, but the never-completing-future park here keeps the
  // FletApp's existing FutureBuilder rendering until the OS tears us
  // down for real).
  if (nrt.pythonAlreadyRunning) {
    debugPrint(
        "Python already initialized (process reuse) — skipping SeriousPython.runProgram");
    return Completer<String>().future;
  }
  return nrt.runPython(
    moduleName: pythonModuleName,
    appDir: appDir,
    outLogFilename: outLogFilename,
    environmentVariables: environmentVariables,
    args: args,
  );
}
