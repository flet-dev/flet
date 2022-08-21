import 'package:flutter/widgets.dart';

class RouteParser extends RouteInformationParser<String> {
  @override
  Future<String> parseRouteInformation(
      RouteInformation routeInformation) async {
    return routeInformation.location!;
  }

  @override
  RouteInformation restoreRouteInformation(String configuration) =>
      RouteInformation(location: configuration);
}
