// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';

class NoAnimationPage<T> extends Page<T> {
  final Widget child;
  final Duration duration;

  const NoAnimationPage({
    LocalKey? key,
    required this.child,
    this.duration = const Duration(milliseconds: 0),
  }) : super(key: key);

  @override
  Route<T> createRoute(BuildContext context) => NoAnimationPageRoute<T>(this);
}

class NoAnimationPageRoute<T> extends PageRoute<T> {
  final NoAnimationPage<T> _page;

  NoAnimationPageRoute(this._page) : super(settings: _page);

  @override
  Color? get barrierColor => null;

  @override
  String? get barrierLabel => null;

  @override
  Duration get transitionDuration => _page.duration;

  @override
  bool get maintainState => true;

  @override
  Widget buildPage(BuildContext context, Animation<double> animation,
      Animation<double> secondaryAnimation) {
    return (settings as NoAnimationPage).child;
  }

  @override
  Widget buildTransitions(BuildContext context, Animation<double> animation,
          Animation<double> secondaryAnimation, Widget child) =>
      child;
}
