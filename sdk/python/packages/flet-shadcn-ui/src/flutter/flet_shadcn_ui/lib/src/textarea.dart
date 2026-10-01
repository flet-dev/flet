import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadTextareaControl extends StatefulWidget {
  final Control control;

  const ShadTextareaControl({super.key, required this.control});

  @override
  State<ShadTextareaControl> createState() => _ShadTextareaControlState();
}

class _ShadTextareaControlState extends State<ShadTextareaControl> {
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
    debugPrint("ShadTextarea.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown ShadTextarea method: $name");
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
    debugPrint("ShadTextarea build: ${widget.control.id}");

    final control = widget.control;

    final value = control.getString("value", "")!;
    if (_value != value) {
      _value = value;
      _controller.value = TextEditingValue(
        text: value,
        selection: TextSelection.collapsed(offset: value.length),
      );
    }

    final textarea = ShadTextarea(
      controller: _controller,
      focusNode: _focusNode,
      enabled: !control.disabled,
      placeholder: control.buildTextOrWidget("placeholder"),
      minHeight: control.getDouble("min_height", 80)!,
      maxHeight: control.getDouble("max_height", 500)!,
      resizable: control.getBool("resizable", true)!,
      readOnly: control.getBool("read_only", false)!,
      maxLength: control.getInt("max_length"),
      autofocus: control.getBool("autofocus", false)!,
      onChanged: _onChanged,
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, textarea),
    );
  }
}
