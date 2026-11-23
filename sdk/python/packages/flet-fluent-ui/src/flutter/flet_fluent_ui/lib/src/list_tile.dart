import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/intrinsics.dart';
import 'utils/theme.dart';

class FluentListTileControl extends StatelessWidget {
  final Control control;

  const FluentListTileControl({super.key, required this.control});

  void _onSelectionChange(bool selected) {
    control.updateProperties({"selected": selected}, notify: true);
    control.triggerEvent("selection_change", selected);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentListTile build: ${control.id}");

    final selectionMode = parseEnum(
      ListTileSelectionMode.values,
      control.getString("selection_mode"),
      ListTileSelectionMode.none,
    )!;
    final enabled = !control.disabled;
    final onPressed = enabled && control.hasEventHandler("click")
        ? () => control.triggerEvent("click")
        : null;
    final title = control.buildTextOrWidget("title");
    // fluent_ui asserts that a subtitle has a title.
    final subtitle = title == null ? null : control.buildTextOrWidget("subtitle");
    final leading = control.buildIconOrWidget("leading");
    final trailing = control.buildWidget("trailing");
    final autofocus = control.getBool("autofocus", false)!;

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        // ListTile lays out with a LayoutBuilder, which can't report an
        // intrinsic size.
        MeasuredIntrinsics(
          estimate: const Size(200, 40),
          child: selectionMode == ListTileSelectionMode.none
            ? ListTile(
                title: title,
                subtitle: subtitle,
                leading: leading,
                trailing: trailing,
                autofocus: autofocus,
                onPressed: onPressed,
              )
            : ListTile.selectable(
                title: title,
                subtitle: subtitle,
                leading: leading,
                trailing: trailing,
                autofocus: autofocus,
                onPressed: onPressed,
                selectionMode: selectionMode,
                selected: control.getBool("selected", false)!,
                onSelectionChange: enabled ? _onSelectionChange : null,
              ),
        ),
      ),
    );
  }
}
