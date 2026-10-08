import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/field.dart';
import 'utils/icons.dart';

class ShadInputControl extends StatefulWidget {
  final Control control;

  const ShadInputControl({super.key, required this.control});

  @override
  State<ShadInputControl> createState() => _ShadInputControlState();
}

class _ShadInputControlState extends State<ShadInputControl> {
  String _value = "";
  late final TextEditingController _controller;
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    _controller.dispose();
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("ShadInput.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown ShadInput method: $name");
    }
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  void _onChanged(String value) {
    _value = value;
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadInput build: ${widget.control.id}");

    final control = widget.control;

    final value = control.getString("value", "")!;
    if (_value != value) {
      _value = value;
      _controller.value = TextEditingValue(
        text: value,
        selection: TextSelection.collapsed(offset: value.length),
      );
    }

    Widget input(ShadDecoration? decoration) => ShadInput(
      decoration: decoration,
      controller: _controller,
      focusNode: _focusNode,
      enabled: !control.disabled,
      placeholder: control.buildTextOrWidget("placeholder"),
      obscureText: control.getBool("password", false)!,
      obscuringCharacter: control.getString("obscuring_character", "•")!,
      readOnly: control.getBool("read_only", false)!,
      maxLength: control.getInt("max_length"),
      minLines: control.getInt("min_lines"),
      maxLines: control.getInt("max_lines", 1),
      keyboardType: control.getTextInputType(
        "keyboard_type",
        TextInputType.text,
      )!,
      textAlign: control.getTextAlign("text_align", TextAlign.start)!,
      leading: buildShadIconOrWidget(control, "leading"),
      trailing: buildShadIconOrWidget(control, "trailing"),
      autofocus: control.getBool("autofocus", false)!,
      onChanged: _onChanged,
      onSubmitted: (value) => control.triggerEvent("submit", value),
      onPressed: control.hasEventHandler("click")
          ? () => control.triggerEvent("click")
          : null,
    );

    return LayoutControl(
      control: control,
      child: buildShadField(context, control, input),
    );
  }
}
