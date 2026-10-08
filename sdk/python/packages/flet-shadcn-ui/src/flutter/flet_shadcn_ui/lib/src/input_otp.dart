import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/field.dart';
import 'utils/icons.dart';

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
    List<Widget> slots(BuildContext context, ShadDecoration? decoration) {
      final children = <Widget>[];
      var slot = 0;
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
            children: List.generate(
              size,
              (_) => ShadInputOTPSlot(
                decoration: _slotErrorDecoration(
                  context,
                  decoration,
                  slot++,
                  length / groups.length,
                ),
              ),
            ),
          ),
        );
      }

      return children;
    }

    Widget input(ShadDecoration? decoration) => Builder(
      builder: (context) => ShadInputOTP(
        key: ValueKey(_generation),
        maxLength: length,
        initialValue: value,
        enabled: !control.disabled,
        keyboardType: control.getTextInputType(
          "keyboard_type",
          TextInputType.number,
        ),
        onChanged: _onChanged,
        children: slots(context, decoration),
      ),
    );

    return LayoutControl(
      control: control,
      child: buildShadField(context, control, input),
    );
  }
}

/// The error decoration for the slot at [index].
///
/// ShadInputOTPSlot merges its own `border` (with a grey left side on the
/// first slot of a group) over the given decoration, so a red `border` would
/// leave sides of mixed colors. The error goes into `errorBorder` instead,
/// with the sides and corners shadcn_ui gives the slot.
ShadDecoration? _slotErrorDecoration(
  BuildContext context,
  ShadDecoration? decoration,
  int index,
  double groupSize,
) {
  final color = decoration?.border?.top?.color;
  if (color == null) return null;
  final radius = ShadTheme.of(context).radius;
  final first = index % groupSize == 0;
  final last = (index + 1) % groupSize == 0;
  final side = ShadBorderSide(color: color, width: 1);
  return ShadDecoration(
    hasError: true,
    errorBorder: ShadBorder(
      top: side,
      bottom: side,
      right: side,
      left: first ? side : ShadBorderSide.none,
      padding: const EdgeInsets.all(1),
      radius: BorderRadius.only(
        topLeft: first ? radius.topLeft : Radius.zero,
        bottomLeft: first ? radius.bottomLeft : Radius.zero,
        topRight: last ? radius.topRight : Radius.zero,
        bottomRight: last ? radius.bottomRight : Radius.zero,
      ),
    ),
  );
}
