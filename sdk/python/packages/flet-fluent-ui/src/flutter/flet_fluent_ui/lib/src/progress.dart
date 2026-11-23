import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

/// A `flet_fluent_ui.ProgressBar` or `ProgressRing`, picked by [ring].
class FluentProgressControl extends StatelessWidget {
  final Control control;
  final bool ring;

  const FluentProgressControl({
    super.key,
    required this.control,
    required this.ring,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("${control.type} build: ${control.id}");

    // fluent_ui asserts that the value is within [0, 100].
    final value = control.getDouble("value")?.clamp(0.0, 100.0);
    final strokeWidth = control.getDouble("stroke_width", 4.5)!;
    final activeColor = control.getColor("color", context);
    final backgroundColor = control.getColor("bgcolor", context);

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        ring
            ? ProgressRing(
                value: value,
                strokeWidth: strokeWidth,
                activeColor: activeColor,
                backgroundColor: backgroundColor,
              )
            : ProgressBar(
                value: value,
                strokeWidth: strokeWidth,
                activeColor: activeColor,
                backgroundColor: backgroundColor,
              ),
      ),
    );
  }
}
