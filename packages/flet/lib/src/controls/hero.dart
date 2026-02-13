import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class HeroControl extends StatelessWidget {
  final Control control;

  const HeroControl({super.key, required this.control});

  Widget _buildFlightShuttle(
    BuildContext flightContext,
    Animation<double> animation,
    HeroFlightDirection flightDirection,
    BuildContext fromHeroContext,
    BuildContext toHeroContext,
  ) {
    final toHero = toHeroContext.widget as Hero;
    return Material(
      type: MaterialType.transparency,
      child: DefaultTextStyle(
        style: DefaultTextStyle.of(toHeroContext).style,
        child: toHero.child,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Hero build: ${control.id}");

    final content = control.buildWidget("content");
    if (content == null) {
      return const ErrorControl("Hero.content must be provided and visible");
    }

    final tag = control.get("tag");
    if (tag == null) {
      return const ErrorControl("Hero.tag must be provided");
    }

    return LayoutControl(
      control: control,
      child: Hero(
        tag: tag,
        flightShuttleBuilder: _buildFlightShuttle,
        transitionOnUserGestures: control.getBool(
          "transition_on_user_gestures",
          false,
        )!,
        child: content,
      ),
    );
  }
}
