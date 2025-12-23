import 'package:flutter/widgets.dart';

/// Normalizes external URIs (e.g. `flet://flet-host/aaa`) into the path-based
/// form used by Flet routing (e.g. `/aaa`).
class FletRouteInformationProvider extends PlatformRouteInformationProvider {
  FletRouteInformationProvider({
    required super.initialRouteInformation,
  });

  static RouteInformation normalize(RouteInformation routeInformation) {
    final uri = routeInformation.uri;
    return RouteInformation(
      uri: Uri(
        path: uri.path.isEmpty ? '/' : uri.path,
        query: uri.query,
        fragment: uri.fragment,
      ),
      state: routeInformation.state,
    );
  }

  @override
  Future<bool> didPushRouteInformation(RouteInformation routeInformation) {
    final normalized = normalize(routeInformation);
    debugPrint(
        "FletRouteInformationProvider.didPushRouteInformation: ${routeInformation.uri} -> ${normalized.uri}");
    return super.didPushRouteInformation(normalized);
  }
}
