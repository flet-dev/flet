import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadRadioGroupControl extends StatefulWidget {
  final Control control;

  const ShadRadioGroupControl({super.key, required this.control});

  @override
  State<ShadRadioGroupControl> createState() => _ShadRadioGroupControlState();
}

class _ShadRadioGroupControlState extends State<ShadRadioGroupControl> {
  late final ShadRadioController<String> _controller;

  // ShadRadioGroup reports every controller change through onChanged, so a
  // value set from Python is not echoed back as a change event.
  bool _settingValue = false;

  @override
  void initState() {
    super.initState();
    _controller = ShadRadioController<String>(
      value: widget.control.getString("value"),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onChanged(String? value) {
    if (_settingValue) return;
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadRadioGroup build: ${widget.control.id}");

    final control = widget.control;

    final value = control.getString("value");
    if (_controller.value != value) {
      _settingValue = true;
      _controller.value = value;
      _settingValue = false;
    }

    final group = ShadRadioGroup<String>(
      controller: _controller,
      enabled: !control.disabled,
      axis: control.getBool("horizontal", false)!
          ? Axis.horizontal
          : Axis.vertical,
      spacing: control.getDouble("spacing"),
      onChanged: _onChanged,
      items: control.buildWidgets("items"),
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, group),
    );
  }
}

/// A `flet_shadcn_ui.Radio`; must be inside a `ShadRadioGroupControl`.
class ShadRadioControl extends StatelessWidget {
  final Control control;

  const ShadRadioControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    return ShadRadio<String>(
      value: control.getString("value", "")!,
      enabled: !control.disabled,
      label: control.buildTextOrWidget("label"),
      // ShadRadio styles the sublabel with the colorless `muted` text style.
      sublabel: withMutedColor(context, control.buildTextOrWidget("sublabel")),
      color: control.getColor("color", context),
    );
  }
}
