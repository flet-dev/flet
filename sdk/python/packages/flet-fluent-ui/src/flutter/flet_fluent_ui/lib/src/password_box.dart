import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/fields.dart';
import 'utils/theme.dart';

class FluentPasswordBoxControl extends StatefulWidget {
  final Control control;

  const FluentPasswordBoxControl({super.key, required this.control});

  @override
  State<FluentPasswordBoxControl> createState() =>
      _FluentPasswordBoxControlState();
}

class _FluentPasswordBoxControlState extends State<FluentPasswordBoxControl>
    with FluentTextFieldState {
  @override
  Control get control => widget.control;

  // fluent_ui's PasswordBox disposes the focus node passed to it.
  @override
  bool get ownsFocusNode => false;

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
    debugPrint("FluentPasswordBox build: ${control.id}");

    syncTextValue();

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        PasswordBox(
          controller: textController,
          focusNode: focusNode,
          enabled: !control.disabled,
          placeholder: control.getString("placeholder"),
          revealMode: parseEnum(
            PasswordRevealMode.values,
            control.getString("reveal_mode"),
            PasswordRevealMode.peek,
          )!,
          readOnly: control.getBool("read_only", false)!,
          leadingIcon: buildFieldPrefix(control),
          autofocus: control.getBool("autofocus", false)!,
          onChanged: onTextChanged,
          onSubmitted: (value) => control.triggerEvent("submit", value),
        ),
      ),
    );
  }
}
