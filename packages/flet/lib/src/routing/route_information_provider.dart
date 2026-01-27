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
        query: uri.hasQuery ? uri.query : null,
        fragment: uri.hasFragment ? uri.fragment : null,
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

class FletLocalRouteInformationProvider extends RouteInformationProvider
    with ChangeNotifier {
  RouteInformation _value;

  FletLocalRouteInformationProvider({
    required RouteInformation initialRouteInformation,
  }) : _value = FletRouteInformationProvider.normalize(
            initialRouteInformation,
          );

  @override
  RouteInformation get value => _value;

  @override
  void routerReportsNewRouteInformation(
    RouteInformation routeInformation, {
    RouteInformationReportingType type = RouteInformationReportingType.none,
  }) {
    _setValue(routeInformation);
  }

  @override
  Future<bool> didPushRouteInformation(RouteInformation routeInformation) async {
    _setValue(routeInformation);
    return true;
  }

  void _setValue(RouteInformation routeInformation) {
    final normalized = FletRouteInformationProvider.normalize(routeInformation);
    if (_value.uri == normalized.uri && _value.state == normalized.state) {
      return;
    }
    _value = normalized;
    notifyListeners();
  }
}
