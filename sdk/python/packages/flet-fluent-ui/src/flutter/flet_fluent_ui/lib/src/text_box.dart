import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentTextBoxControl extends StatefulWidget {
  final Control control;

  const FluentTextBoxControl({super.key, required this.control});

  @override
  State<FluentTextBoxControl> createState() => _FluentTextBoxControlState();
}

class _FluentTextBoxControlState extends State<FluentTextBoxControl> {
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
    debugPrint("FluentTextBox.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown FluentTextBox method: $name");
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
    debugPrint("FluentTextBox build: ${widget.control.id}");

    final control = widget.control;

    final value = control.getString("value", "")!;
    if (_value != value) {
      _value = value;
      _controller.value = TextEditingValue(
        text: value,
        selection: TextSelection.collapsed(offset: value.length),
      );
    }

    final multiline = control.getBool("multiline", false)!;
    final prefix = control.buildIconOrWidget("prefix");
    final suffix = control.buildIconOrWidget("suffix");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        TextBox(
          controller: _controller,
          focusNode: _focusNode,
          enabled: !control.disabled,
          placeholder: control.getString("placeholder"),
          obscureText: control.getBool("password", false)!,
          readOnly: control.getBool("read_only", false)!,
          maxLength: control.getInt("max_length"),
          minLines: multiline ? control.getInt("min_lines") : null,
          maxLines: multiline ? control.getInt("max_lines") : 1,
          // The multiline keyboard type makes `Enter` insert a new line.
          keyboardType: multiline
              ? TextInputType.multiline
              : control.getTextInputType("keyboard_type", TextInputType.text)!,
          textAlign: control.getTextAlign("text_align", TextAlign.start)!,
          prefix: prefix == null
              ? null
              : Padding(
                  padding: const EdgeInsetsDirectional.only(start: 8),
                  child: prefix,
                ),
          suffix: suffix == null
              ? null
              : Padding(
                  padding: const EdgeInsetsDirectional.only(end: 8),
                  child: suffix,
                ),
          autofocus: control.getBool("autofocus", false)!,
          onChanged: _onChanged,
          onSubmitted: (value) => control.triggerEvent("submit", value),
        ),
      ),
    );
  }
}
