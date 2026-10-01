import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadSelectControl extends StatefulWidget {
  final Control control;

  const ShadSelectControl({super.key, required this.control});

  @override
  State<ShadSelectControl> createState() => _ShadSelectControlState();
}

class _ShadSelectControlState extends State<ShadSelectControl> {
  late final ShadSelectController<String> _controller;

  @override
  void initState() {
    super.initState();
    _controller = ShadSelectController<String>(
      initialValue: _valueSet(widget.control.getString("value")),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Set<String> _valueSet(String? value) => value == null ? {} : {value};

  void _onChanged(String? value) {
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadSelect build: ${widget.control.id}");

    final control = widget.control;

    final value = control.getString("value");
    if (_controller.value.firstOrNull != value) {
      _controller.value = _valueSet(value);
    }

    // Option controls are not rendered directly: ShadSelect needs typed
    // ShadOption<String> children, so they are built from each option's
    // properties. The closed select shows the option's text.
    final options = control.children("options");
    final textByValue = {
      for (final option in options)
        option.getString("value", "")!:
            option.getString("text") ?? option.getString("value", "")!,
    };

    final select = ShadSelect<String>(
      controller: _controller,
      enabled: !control.disabled,
      placeholder: control.buildTextOrWidget("placeholder"),
      allowDeselection: control.getBool("allow_deselection", false)!,
      minWidth: control.getDouble("min_width"),
      maxHeight: control.getDouble("max_height"),
      onChanged: _onChanged,
      selectedOptionBuilder: (context, value) =>
          Text(textByValue[value] ?? value),
      options: [
        for (final option in options)
          ShadOption<String>(
            value: option.getString("value", "")!,
            child:
                option.buildWidget("content") ??
                Text(textByValue[option.getString("value", "")!]!),
          ),
      ],
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, select),
    );
  }
}
