import 'package:flutter/material.dart';

import '../models/control.dart';
import 'time.dart';

ImplicitAnimationDetails? parseAnimation(dynamic value,
    [ImplicitAnimationDetails? defaultValue]) {
  if (value == null) {
    return defaultValue;
  } else if (value is bool && value == true) {
    return ImplicitAnimationDetails(
        duration: const Duration(milliseconds: 1000), curve: Curves.linear);
  } else if (value is int) {
    return ImplicitAnimationDetails(
        duration: parseDuration(value, const Duration())!,
        curve: Curves.linear);
  }
  return ImplicitAnimationDetails(
      duration: parseDuration(value["duration"], const Duration())!,
      curve: parseCurve(value["curve"], Curves.linear)!);
}

class ImplicitAnimationDetails {
  final Duration duration;
  final Curve curve;

  ImplicitAnimationDetails({required this.duration, required this.curve});
}

Curve? parseCurve(String? value, [Curve? defaultValue]) {
  if (value == null) return defaultValue;

  const curves = <String, Curve>{
    "bouncein": Curves.bounceIn,
    "bounceinout": Curves.bounceInOut,
    "bounceout": Curves.bounceOut,
    "decelerate": Curves.decelerate,
    "ease": Curves.ease,
    "easein": Curves.easeIn,
    "easeinback": Curves.easeInBack,
    "easeincirc": Curves.easeInCirc,
    "easeincubic": Curves.easeInCubic,
    "easeinexpo": Curves.easeInExpo,
    "easeinout": Curves.easeInOut,
    "easeinoutback": Curves.easeInOutBack,
    "easeinoutcirc": Curves.easeInOutCirc,
    "easeinoutcubic": Curves.easeInOutCubic,
    "easeinoutcubicemphasized": Curves.easeInOutCubicEmphasized,
    "easeinoutexpo": Curves.easeInOutExpo,
    "easeinoutquad": Curves.easeInOutQuad,
    "easeinoutquart": Curves.easeInOutQuart,
    "easeinoutquint": Curves.easeInOutQuint,
    "easeinoutsine": Curves.easeInOutSine,
    "easeinquad": Curves.easeInQuad,
    "easeinquart": Curves.easeInQuart,
    "easeinquint": Curves.easeInQuint,
    "easeinsine": Curves.easeInSine,
    "easeintolinear": Curves.easeInToLinear,
    "easeout": Curves.easeOut,
    "easeoutback": Curves.easeOutBack,
    "easeoutcirc": Curves.easeOutCirc,
    "easeoutcubic": Curves.easeOutCubic,
    "easeoutexpo": Curves.easeOutExpo,
    "easeoutquad": Curves.easeOutQuad,
    "easeoutquart": Curves.easeOutQuart,
    "easeoutquint": Curves.easeOutQuint,
    "easeoutsine": Curves.easeOutSine,
    "elasticin": Curves.elasticIn,
    "elasticinout": Curves.elasticInOut,
    "elasticout": Curves.elasticOut,
    "fastlineartosloweasein": Curves.fastLinearToSlowEaseIn,
    "fastoutslowin": Curves.fastOutSlowIn,
    "lineartoeaseout": Curves.linearToEaseOut,
    "slowmiddle": Curves.slowMiddle,
  };

  return curves[value.toLowerCase()] ?? defaultValue;
}

AnimationStyle? parseAnimationStyle(dynamic value,
    [AnimationStyle? defaultValue]) {
  if (value == null) return defaultValue;

  return AnimationStyle(
      curve: parseCurve(value["curve"]),
      reverseCurve: parseCurve(value["reverse_curve"]),
      duration: parseDuration(value["duration"]),
      reverseDuration: parseDuration(value["reverse_duration"]));
}

extension AnimationParsers on Control {
  ImplicitAnimationDetails? getAnimation(String propertyName,
      [ImplicitAnimationDetails? defaultValue]) {
    return parseAnimation(get(propertyName), defaultValue);
  }

  Curve? getCurve(String propertyName, [Curve? defaultValue]) {
    return parseCurve(get(propertyName), defaultValue);
  }

  AnimationStyle? getAnimationStyle(String propertyName,
      [AnimationStyle? defaultValue]) {
    return parseAnimationStyle(get(propertyName), defaultValue);
  }
}
