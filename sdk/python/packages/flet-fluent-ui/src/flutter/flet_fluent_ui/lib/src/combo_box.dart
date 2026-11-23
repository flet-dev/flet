import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentComboBoxControl extends StatelessWidget {
  final Control control;

  const FluentComboBoxControl({super.key, required this.control});

  void _onChanged(String? value) {
    if (value == control.getString("value")) return;
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentComboBox build: ${control.id}");

    // Item controls are not rendered directly: ComboBox needs typed
    // ComboBoxItem<String> entries, so they are built from each item's
    // properties.
    final items = control.children("items");
    final values = {for (final item in items) item.getString("value", "")!};
    final value = control.getString("value");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        ComboBox<String>(
          // fluent_ui asserts that the value is one of the items.
          value: values.contains(value) ? value : null,
          placeholder: control.buildTextOrWidget("placeholder"),
          isExpanded: control.getBool("expand_to_fit", false)!,
          autofocus: control.getBool("autofocus", false)!,
          onChanged: control.disabled ? null : _onChanged,
          onOpen: control.hasEventHandler("open")
              ? () => control.triggerEvent("open")
              : null,
          onClose: control.hasEventHandler("close")
              ? () => control.triggerEvent("close")
              : null,
          items: [
            for (final item in items)
              ComboBoxItem<String>(
                value: item.getString("value", "")!,
                enabled: !item.disabled,
                child:
                    item.buildWidget("content") ??
                    Text(
                      item.getString("text") ?? item.getString("value", "")!,
                    ),
              ),
          ],
        ),
      ),
    );
  }
}
