import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'numbers.dart';

ImplicitAnimationDetails? parseAnimation(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return animationFromJSON(j1);
}

ImplicitAnimationDetails animationFromJSON(dynamic json) {
  if (json is int) {
    return ImplicitAnimationDetails(
        duration: Duration(milliseconds: parseInt(json)), curve: Curves.linear);
  } else if (json is bool && json == true) {
    return ImplicitAnimationDetails(
        duration: const Duration(milliseconds: 1000), curve: Curves.linear);
  }

  return ImplicitAnimationDetails.fromJson(json);
}

class ImplicitAnimationDetails {
  final Duration duration;
  final Curve curve;

  ImplicitAnimationDetails({required this.duration, required this.curve});

  factory ImplicitAnimationDetails.fromJson(Map<String, dynamic> json) {
    return ImplicitAnimationDetails(
        duration: Duration(milliseconds: json["duration"] as int),
        curve: parseCurve(json["curve"]));
  }
}

Curve parseCurve(String? s) {
  switch (s?.toLowerCase()) {
    case "bouncein":
      return Curves.bounceIn;
    case "bounceinout":
      return Curves.bounceInOut;
    case "bounceout":
      return Curves.bounceOut;
    case "decelerate":
      return Curves.decelerate;
    case "ease":
      return Curves.ease;
    case "easein":
      return Curves.easeIn;
    case "easeinback":
      return Curves.easeInBack;
    case "easeincirc":
      return Curves.easeInCirc;
    case "easeincubic":
      return Curves.easeInCubic;
    case "easeinexpo":
      return Curves.easeInExpo;
    case "easeinout":
      return Curves.easeInOut;
    case "easeinoutback":
      return Curves.easeInOutBack;
    case "easeinoutcirc":
      return Curves.easeInOutCirc;
    case "easeinoutcubic":
      return Curves.easeInOutCubic;
    case "easeinoutcubicemphasized":
      return Curves.easeInOutCubicEmphasized;
    case "easeinoutexpo":
      return Curves.easeInOutExpo;
    case "easeinoutquad":
      return Curves.easeInOutQuad;
    case "easeinoutquart":
      return Curves.easeInOutQuart;
    case "easeinoutquint":
      return Curves.easeInOutQuint;
    case "easeinoutsine":
      return Curves.easeInOutSine;
    case "easeinquad":
      return Curves.easeInQuad;
    case "easeinquart":
      return Curves.easeInQuart;
    case "easeinquint":
      return Curves.easeInQuint;
    case "easeinsine":
      return Curves.easeInSine;
    case "easeintolinear":
      return Curves.easeInToLinear;
    case "easeout":
      return Curves.easeOut;
    case "easeoutback":
      return Curves.easeOutBack;
    case "easeoutcirc":
      return Curves.easeOutCirc;
    case "easeoutcubic":
      return Curves.easeOutCubic;
    case "easeoutexpo":
      return Curves.easeOutExpo;
    case "easeoutquad":
      return Curves.easeOutQuad;
    case "easeoutquart":
      return Curves.easeOutQuart;
    case "easeoutquint":
      return Curves.easeOutQuint;
    case "easeoutsine":
      return Curves.easeOutSine;
    case "elasticin":
      return Curves.elasticIn;
    case "elasticinout":
      return Curves.elasticInOut;
    case "elasticout":
      return Curves.elasticOut;
    case "fastlineartosloweasein":
      return Curves.fastLinearToSlowEaseIn;
    case "fastoutslowin":
      return Curves.fastOutSlowIn;
    case "lineartoeaseout":
      return Curves.linearToEaseOut;
    case "slowmiddle":
      return Curves.slowMiddle;
    default:
      return Curves.linear;
  }
}
