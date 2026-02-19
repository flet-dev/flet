import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';
import '../utils/enums.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/gradient.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ShimmerControl extends StatelessWidget {
  final Control control;

  const ShimmerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Shimmer build: ${control.id}");

    final content = control.buildWidget("content");
    if (content == null) {
      return const ErrorControl("Shimmer.content must be specified");
    }

    final gradient = control.getGradient("gradient", Theme.of(context));
    final baseColor = control.getColor("base_color", context);
    final highlightColor = control.getColor("highlight_color", context);

    if (gradient == null && (baseColor == null || highlightColor == null)) {
      return const ErrorControl(
          "Shimmer requires either gradient or base/highlight colors");
    }

    final direction = _parseDirection(control.getString("direction"));
    final period =
        control.getDuration("period", const Duration(milliseconds: 1500))!;
    final loop = control.getInt("loop", 0)!;

    final shimmerWidget = gradient != null
        ? Shimmer(
            gradient: gradient,
            direction: direction,
            period: period,
            loop: loop,
            enabled: !control.disabled,
            child: content,
          )
        : Shimmer.fromColors(
            baseColor: baseColor!,
            highlightColor: highlightColor!,
            direction: direction,
            period: period,
            loop: loop,
            enabled: !control.disabled,
            child: content,
          );

    return LayoutControl(control: control, child: shimmerWidget);
  }
}

ShimmerDirection _parseDirection(String? value,
    [ShimmerDirection defaultValue = ShimmerDirection.ltr]) {
  return parseEnum(ShimmerDirection.values, value, defaultValue)!;
}
