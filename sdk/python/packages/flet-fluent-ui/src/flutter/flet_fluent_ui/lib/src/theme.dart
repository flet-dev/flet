import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentThemeControl extends StatelessWidget {
  final Control control;

  const FluentThemeControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentTheme build: ${control.id}");

    return LayoutControl(
      control: control,
      // The theme goes inside the fallback wrapper, so localizations are
      // still provided when the page has none.
      child: withFluentTheme(
        context,
        FluentTheme(
          data: parseFluentThemeData(control, context),
          child: control.buildWidget("content") ?? const SizedBox.shrink(),
        ),
      ),
    );
  }
}
