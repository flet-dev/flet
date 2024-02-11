// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';

class AnimatedTransitionPage<T> extends Page<T> {
  final bool fadeTransition;
  final Widget child;
  final Duration duration;
  final bool fullscreenDialog;

  const AnimatedTransitionPage({
    super.key,
    required this.child,
    this.fadeTransition = false,
    this.fullscreenDialog = false,
    this.duration = const Duration(milliseconds: 300),
  });

  @override
  Route<T> createRoute(BuildContext context) =>
      PageBasedAnimatedTransitionRoute<T>(this, fullscreenDialog);
}

class PageBasedAnimatedTransitionRoute<T> extends PageRoute<T> {
  final AnimatedTransitionPage<T> _page;

  PageBasedAnimatedTransitionRoute(this._page, bool fullscreenDialog)
      : super(settings: _page, fullscreenDialog: fullscreenDialog);

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
    final Widget child = (settings as AnimatedTransitionPage).child;

    if (_page.fadeTransition && _page.duration != Duration.zero) {
      // initial page
      var curveTween = CurveTween(curve: Curves.easeIn);
      return FadeTransition(
        opacity: animation.drive(curveTween),
        child: (settings as AnimatedTransitionPage).child,
      );
    } else {
      // use standard animation
      return Semantics(
        scopesRoute: true,
        explicitChildNodes: true,
        child: child,
      );
    }
  }

  @override
  Widget buildTransitions(BuildContext context, Animation<double> animation,
          Animation<double> secondaryAnimation, Widget child) =>
      _page.fadeTransition || _page.duration == Duration.zero
          ? child
          : Theme.of(context).pageTransitionsTheme.buildTransitions<T>(
              this, context, animation, secondaryAnimation, child);
}
