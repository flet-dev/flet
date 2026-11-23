import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentCardControl extends StatelessWidget {
  final Control control;

  const FluentCardControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentCard build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Card(
          padding: control.getPadding("padding", const EdgeInsets.all(12))!,
          backgroundColor: control.getColor("bgcolor", context),
          borderColor: control.getColor("border_color", context),
          borderRadius: control.getBorderRadius(
            "border_radius",
            const BorderRadius.all(Radius.circular(4)),
          )!,
          child: control.buildWidget("content") ?? const SizedBox.shrink(),
        ),
      ),
    );
  }
}
