import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

/// Keeps a text field's controller in sync with the control's `value`, and
/// reports typing, focus changes and the `focus()` method, for the Fluent text
/// inputs that take a [TextEditingController].
mixin FluentTextFieldState<T extends StatefulWidget> on State<T> {
  Control get control;

  late final TextEditingController textController;
  late final FocusNode focusNode;
  String _value = "";

  /// Whether this state disposes [focusNode]. fluent_ui's PasswordBox
  /// disposes the focus node it is given (its ownership check is inverted),
  /// so a state that passes it to a PasswordBox must not dispose it again.
  bool get ownsFocusNode => true;

  void initTextField() {
    textController = TextEditingController();
    focusNode = FocusNode();
    focusNode.addListener(_onFocusChange);
    control.addInvokeMethodListener(_invokeMethod);
  }

  void disposeTextField() {
    control.removeInvokeMethodListener(_invokeMethod);
    focusNode.removeListener(_onFocusChange);
    if (ownsFocusNode) focusNode.dispose();
    textController.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("${control.type}.$name($args)");
    switch (name) {
      case "focus":
        focusNode.requestFocus();
      default:
        throw Exception("Unknown ${control.type} method: $name");
    }
  }

  void _onFocusChange() {
    control.triggerEvent(focusNode.hasFocus ? "focus" : "blur");
  }

  /// Puts a `value` set from Python into the field; call it from `build`.
  void syncTextValue() {
    final value = control.getString("value", "")!;
    if (_value != value) {
      _value = value;
      textController.value = TextEditingValue(
        text: value,
        selection: TextSelection.collapsed(offset: value.length),
      );
    }
  }

  /// Reports text typed by the user as the new `value`.
  void onTextChanged(String value) {
    if (value == _value) return;
    _value = value;
    control.updateProperties({"value": value});
    control.triggerEvent("change", value);
  }
}

/// Builds the `prefix` icon or control of a Fluent text input, padded away
/// from the field's edge.
Widget? buildFieldPrefix(Control control) {
  final prefix = control.buildIconOrWidget("prefix");
  return prefix == null
      ? null
      : Padding(
          padding: const EdgeInsetsDirectional.only(start: 8),
          child: prefix,
        );
}
