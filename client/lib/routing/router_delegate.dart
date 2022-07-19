import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

import 'route_state.dart';

class SimpleRouterDelegate extends RouterDelegate<String>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<String> {
  final RouteState routeState;
  final WidgetBuilder builder;

  @override
  final GlobalKey<NavigatorState> navigatorKey;

  SimpleRouterDelegate({
    required this.routeState,
    required this.builder,
    required this.navigatorKey,
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
    debugPrint("currentConfiguration");
    return routeState.route;
  }

  @override
  void dispose() {
    routeState.removeListener(notifyListeners);
    routeState.dispose();
    super.dispose();
  }
}
