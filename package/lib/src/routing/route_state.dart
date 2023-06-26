// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/widgets.dart';

import 'route_parser.dart';

class RouteState extends ChangeNotifier {
  final RouteParser _parser;
  String _route;

  RouteState(this._parser) : _route = "";

  String get route => _route;

  set route(String route) {
    // Don't notify listeners if the path hasn't changed.
    if (_route == route) return;

    _route = route;
    debugPrint("Route changed to: $route");
    notifyListeners();
  }

  Future<void> go(String route) async {
    this.route =
        await _parser.parseRouteInformation(RouteInformation(location: route));
  }
}
