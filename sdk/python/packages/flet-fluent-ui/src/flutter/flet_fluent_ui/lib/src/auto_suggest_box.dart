import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/fields.dart';
import 'utils/theme.dart';

class FluentAutoSuggestBoxControl extends StatefulWidget {
  final Control control;

  const FluentAutoSuggestBoxControl({super.key, required this.control});

  @override
  State<FluentAutoSuggestBoxControl> createState() =>
      _FluentAutoSuggestBoxControlState();
}

class _FluentAutoSuggestBoxControlState
    extends State<FluentAutoSuggestBoxControl> with FluentTextFieldState {
  @override
  Control get control => widget.control;

  @override
  void initState() {
    super.initState();
    initTextField();
  }

  @override
  void dispose() {
    disposeTextField();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentAutoSuggestBox build: ${control.id}");

    syncTextValue();

    // Item controls are not rendered directly: AutoSuggestBox needs typed
    // AutoSuggestBoxItem<String> entries, built from each item's properties.
    final items = [
      for (final item in control.children("items"))
        AutoSuggestBoxItem<String>(
          value: item.getString("value", "")!,
          label: item.getString("label") ?? item.getString("value", "")!,
          child: item.buildWidget("content"),
        ),
    ];

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        AutoSuggestBox<String>(
          items: items,
          controller: textController,
          focusNode: focusNode,
          enabled: !control.disabled,
          placeholder: control.getString("placeholder"),
          leadingIcon: buildFieldPrefix(control),
          clearButtonEnabled: control.getBool("clear_button", true)!,
          maxPopupHeight: control.getDouble("max_popup_height", 380)!,
          autofocus: control.getBool("autofocus", false)!,
          onChanged: (text, reason) => onTextChanged(text),
          onSelected: (item) => control.triggerEvent("select", item.value),
        ),
      ),
    );
  }
}
