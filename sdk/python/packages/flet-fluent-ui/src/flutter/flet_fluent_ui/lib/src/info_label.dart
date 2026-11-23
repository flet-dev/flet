import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentInfoLabelControl extends StatelessWidget {
  final Control control;

  const FluentInfoLabelControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentInfoLabel build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        InfoLabel(
          label: control.getString("label", "")!,
          isHeader: !control.getBool("horizontal", false)!,
          child: control.buildWidget("content"),
        ),
      ),
    );
  }
}
