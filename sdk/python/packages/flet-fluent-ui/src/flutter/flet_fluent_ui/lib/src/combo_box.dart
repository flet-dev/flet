import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/field_layout.dart';
import 'utils/fields.dart';
import 'utils/theme.dart';

/// Builds fluent_ui's typed items from the `ComboBoxItem` controls, which are
/// not rendered themselves.
List<ComboBoxItem<String>> _buildItems(List<Control> items) => [
  for (final item in items)
    ComboBoxItem<String>(
      value: item.getString("value", "")!,
      enabled: !item.disabled,
      child:
          item.buildWidget("content") ??
          Text(item.getString("text") ?? item.getString("value", "")!),
    ),
];

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
        Builder(
          // The context below the Fluent theme, which the field reads.
          builder: (context) => buildFluentField(
            context,
            control,
            (errorColor) => ComboBox<String>(
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
              items: _buildItems(items),
            ),
          ),
        ),
      ),
    );
  }
}

/// A `flet_fluent_ui.EditableComboBox`: a ComboBox whose box is a text field.
///
/// `value` is the text in the box. It is reported when the user picks an
/// item, presses Enter or leaves the box, not on every key press.
class FluentEditableComboBoxControl extends StatefulWidget {
  final Control control;

  const FluentEditableComboBoxControl({super.key, required this.control});

  @override
  State<FluentEditableComboBoxControl> createState() =>
      _FluentEditableComboBoxControlState();
}

class _FluentEditableComboBoxControlState
    extends State<FluentEditableComboBoxControl>
    with FluentTextFieldState {
  @override
  Control get control => widget.control;

  @override
  void initState() {
    super.initState();
    initTextField();
    // fluent_ui fills the box with the item value it is given, as text, when
    // it is created: "null" when the value is not an item. The control's
    // value replaces it.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) textController.text = control.getString("value", "")!;
    });
  }

  @override
  void dispose() {
    disposeTextField();
    super.dispose();
  }

  void _commit(String text) {
    if (text == control.getString("value", "")) return;
    control.updateProperties({"value": text}, notify: true);
    control.triggerEvent("change", text);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentEditableComboBox build: ${control.id}");

    syncTextValue();
    final items = control.children("items");
    final values = {for (final item in items) item.getString("value", "")!};
    final value = control.getString("value");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Builder(
          // The context below the Fluent theme, which the field reads.
          builder: (context) => buildFluentField(
            context,
            control,
            (errorColor) => EditableComboBox<String>(
              // fluent_ui asserts that the value is one of the items; other
              // text is shown through the text controller.
              value: values.contains(value) ? value : null,
              items: _buildItems(items),
              textController: textController,
              focusNode: focusNode,
              autofocus: control.getBool("autofocus", false)!,
              onChanged: control.disabled
                  ? null
                  : (item) {
                      if (item != null) _commit(item);
                    },
              onFieldSubmitted: (text) {
                _commit(text);
                return text;
              },
            ),
          ),
        ),
      ),
    );
  }
}
