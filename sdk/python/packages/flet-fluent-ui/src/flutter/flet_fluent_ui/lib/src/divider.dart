import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentDividerControl extends StatelessWidget {
  final Control control;

  const FluentDividerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentDivider build: ${control.id}");

    final color = control.getColor("color", context);

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Divider(
          direction: control.getBool("vertical", false)!
              ? Axis.vertical
              : Axis.horizontal,
          size: control.getDouble("size"),
          style: DividerThemeData(
            thickness: control.getDouble("thickness"),
            decoration: color == null ? null : BoxDecoration(color: color),
          ),
        ),
      ),
    );
  }
}
