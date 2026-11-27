import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentInfoBadgeControl extends StatelessWidget {
  final Control control;

  const FluentInfoBadgeControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentInfoBadge build: ${control.id}");

    final content = control.buildTextOrWidget("content");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        InfoBadge(
          // fluent_ui centres the text's line box, whose descender space
          // pushes digits below the middle; a line as tall as the font
          // keeps them centred.
          source: content == null
              ? null
              : Align(
                  widthFactor: 1,
                  heightFactor: 1,
                  child: DefaultTextStyle.merge(
                    style: const TextStyle(
                      height: 1,
                      leadingDistribution: TextLeadingDistribution.even,
                    ),
                    child: content,
                  ),
                ),
          severity: parseEnum(
            InfoBarSeverity.values,
            control.getString("severity"),
            InfoBarSeverity.info,
          )!,
          color: control.getColor("bgcolor", context),
          foregroundColor: control.getColor("color", context),
        ),
      ),
    );
  }
}
