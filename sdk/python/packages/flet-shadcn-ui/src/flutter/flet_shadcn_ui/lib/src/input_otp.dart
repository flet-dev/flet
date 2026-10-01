import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/icons.dart';
import 'utils/theme.dart';

class ShadInputOTPControl extends StatefulWidget {
  final Control control;

  const ShadInputOTPControl({super.key, required this.control});

  @override
  State<ShadInputOTPControl> createState() => _ShadInputOTPControlState();
}

class _ShadInputOTPControlState extends State<ShadInputOTPControl> {
  String _value = "";
  // ShadInputOTP only reads its value on creation, so a value set from Python
  // rebuilds it under a new key.
  int _generation = 0;

  void _onChanged(String raw) {
    final value = raw.trimRight();
    if (value == _value) return;
    _value = value;
    final control = widget.control;
    control.updateProperties({"value": value});
    control.triggerEvent("change", value);
    if (value.length == control.getInt("length", 6)! && !value.contains(" ")) {
      control.triggerEvent("complete", value);
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadInputOTP build: ${widget.control.id}");

    final control = widget.control;
    final length = control.getInt("length", 6)!;

    final value = control.getString("value", "")!;
    if (value != _value) {
      _value = value;
      _generation++;
    }

    final groups =
        control.get<List>("groups")?.map((g) => g as int).toList() ?? [length];
    final children = <Widget>[];
    for (final (index, size) in groups.indexed) {
      if (index > 0) {
        children.add(
          buildShadIconOrWidget(control, "separator") ??
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 4),
                child: Icon(LucideIcons.dot, size: 16),
              ),
        );
      }
      children.add(
        ShadInputOTPGroup(
          children: List.generate(size, (_) => const ShadInputOTPSlot()),
        ),
      );
    }

    final input = ShadInputOTP(
      key: ValueKey(_generation),
      maxLength: length,
      initialValue: value,
      enabled: !control.disabled,
      keyboardType: control.getTextInputType(
        "keyboard_type",
        TextInputType.number,
      ),
      onChanged: _onChanged,
      children: children,
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, input),
    );
  }
}
