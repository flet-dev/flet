import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

import 'route_state.dart';

class SimpleRouterDelegate extends RouterDelegate<String>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<String> {
  final RouteState routeState;
  final WidgetBuilder builder;
  final Future<bool?> Function()? popRouteHandler;

  @override
  final GlobalKey<NavigatorState> navigatorKey;

  SimpleRouterDelegate({
    required this.routeState,
    required this.builder,
    required this.navigatorKey,
    this.popRouteHandler,
  }) {
    routeState.addListener(notifyListeners);
  }

  @override
  Widget build(BuildContext context) => builder(context);

  @override
  Future<void> setNewRoutePath(String configuration) async {
    routeState.route = configuration;
    return SynchronousFuture(null);
  }

  @override
  String get currentConfiguration {
    return routeState.route;
  }

  @override
  Future<bool> popRoute() async {
    debugPrint("SimpleRouterDelegate.popRoute()");
    final handler = popRouteHandler;
    if (handler != null) {
      final result = await handler();
      if (result != null) {
        return result;
      }
    }
    return super.popRoute();
  }

  @override
  void dispose() {
    routeState.removeListener(notifyListeners);
    routeState.dispose();
    super.dispose();
  }
}
