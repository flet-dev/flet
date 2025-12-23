import 'package:flutter/widgets.dart';

/// Captures cold-start deep links delivered before Flet's `*.router` app is
/// mounted, and replays them as the initial route once the router is ready.
///
/// Usage in a host app (before `runApp()`):
/// `FletDeepLinkingBootstrap.install();`
class FletDeepLinkingBootstrap {
  static final _observer = _FletDeepLinkObserver();
  static bool _installed = false;

  static RouteInformation? _pendingInitialRouteInformation;

  /// Installs a `WidgetsBindingObserver` as early as possible (ideally right
  /// after `WidgetsFlutterBinding.ensureInitialized()`).
  static void install() {
    if (_installed) return;
    WidgetsFlutterBinding.ensureInitialized();
    WidgetsBinding.instance.addObserver(_observer);
    _installed = true;
  }

  /// Called by Flet once its Router (`MaterialApp.router`/`CupertinoApp.router`)
  /// is ready to receive route updates.
  static void markRouterReady() {
    if (!_installed) return;
    WidgetsBinding.instance.removeObserver(_observer);
    _installed = false;
  }

  static RouteInformation? takePendingInitialRouteInformation() {
    final value = _pendingInitialRouteInformation;
    _pendingInitialRouteInformation = null;
    return value;
  }

  static bool _capture(RouteInformation routeInformation) {
    // Only capture the first pending route to avoid swallowing later deep links
    // that the host app might want to handle while Flet isn't mounted yet.
    if (_pendingInitialRouteInformation != null) {
      return false;
    }

    final uri = routeInformation.uri;
    if (uri.toString().isEmpty) {
      return false;
    }

    _pendingInitialRouteInformation = routeInformation;
    return true;
  }
}

class _FletDeepLinkObserver with WidgetsBindingObserver {
  @override
  Future<bool> didPushRouteInformation(
    RouteInformation routeInformation,
  ) async {
    // Returning true prevents iOS from logging:
    // "Failed to handle route information in Flutter."
    return FletDeepLinkingBootstrap._capture(routeInformation);
  }

  @override
  Future<bool> didPushRoute(String route) async {
    final uri = Uri.tryParse(route);
    if (uri == null) {
      return false;
    }
    return FletDeepLinkingBootstrap._capture(RouteInformation(uri: uri));
  }
}
