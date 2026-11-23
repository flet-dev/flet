import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentRatingBarControl extends StatelessWidget {
  final Control control;

  const FluentRatingBarControl({super.key, required this.control});

  void _onChanged(double value) {
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentRatingBar build: ${control.id}");

    final amount = control.getInt("max", 5)!;
    final readOnly = control.getBool("read_only", false)!;

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Builder(
          builder: (context) {
            final theme = FluentTheme.of(context);
            return RatingControl(
              // fluent_ui asserts that the rating is within [0, amount].
              rating: control.getDouble("value", 0)!.clamp(0.0, amount.toDouble()),
              amount: amount,
              iconSize: control.getDouble("icon_size", 20)!,
              starSpacing: control.getDouble("spacing", 8)!,
              autofocus: control.getBool("autofocus", false)!,
              onChanged: control.disabled || readOnly ? null : _onChanged,
              // Without onChanged, fluent_ui draws the stars as disabled
              // (grey); a read-only rating keeps the enabled colors.
              ratedIconColor: control.getColor("color", context) ??
                  (readOnly && !control.disabled
                      ? theme.accentColor.defaultBrushFor(theme.brightness)
                      : null),
              unratedIconColor: control.getColor("unrated_color", context),
            );
          },
        ),
      ),
    );
  }
}
