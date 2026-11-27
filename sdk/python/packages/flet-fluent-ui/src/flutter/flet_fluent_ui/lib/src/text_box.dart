import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/fields.dart';
import 'utils/field_layout.dart';
import 'utils/theme.dart';

class FluentTextBoxControl extends StatefulWidget {
  final Control control;

  const FluentTextBoxControl({super.key, required this.control});

  @override
  State<FluentTextBoxControl> createState() => _FluentTextBoxControlState();
}

class _FluentTextBoxControlState extends State<FluentTextBoxControl>
    with FluentTextFieldState {
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
    debugPrint("FluentTextBox build: ${control.id}");

    syncTextValue();

    final multiline = control.getBool("multiline", false)!;
    final suffix = control.buildIconOrWidget("suffix");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Builder(
          // The context below the Fluent theme, which the field reads.
          builder: (context) => buildFluentField(
            context,
            control,
            (errorColor) => TextBox(
              controller: textController,
              focusNode: focusNode,
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
                  : control.getTextInputType(
                      "keyboard_type",
                      TextInputType.text,
                    )!,
              textAlign: control.getTextAlign("text_align", TextAlign.start)!,
              prefix: buildFieldPrefix(control),
              suffix: suffix == null
                  ? null
                  : Padding(
                      padding: const EdgeInsetsDirectional.only(end: 8),
                      child: suffix,
                    ),
              autofocus: control.getBool("autofocus", false)!,
              onChanged: onTextChanged,
              onSubmitted: (value) => control.triggerEvent("submit", value),
              highlightColor: errorColor,
              unfocusedColor: errorColor,
            ),
          ),
        ),
      ),
    );
  }
}
