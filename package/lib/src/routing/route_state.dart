// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/widgets.dart';

import 'route_parser.dart';

class RouteState extends ChangeNotifier {
  final RouteParser _parser;
  String _route;
  final List<String> _routesBuffer = [];

  RouteState(this._parser) : _route = "";

  String get route => _route;

  set route(String route) {
    if (_route != route) {
      _route = route;
      notifyListeners();
    }
  }

  // void addPageListener(VoidCallback listener) {
  //   addListener(listener);
  //   for (var route in _routesBuffer) {
  //     _route = route;
  //     notifyListeners();
  //   }
  //   _routesBuffer.clear();
  // }

  Future<void> go(String route) async {
    this.route =
        await _parser.parseRouteInformation(RouteInformation(location: route));
  }
}
