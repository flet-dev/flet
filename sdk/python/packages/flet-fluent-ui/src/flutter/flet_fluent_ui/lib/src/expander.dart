import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentExpanderControl extends StatefulWidget {
  final Control control;

  const FluentExpanderControl({super.key, required this.control});

  @override
  State<FluentExpanderControl> createState() => _FluentExpanderControlState();
}

class _FluentExpanderControlState extends State<FluentExpanderControl> {
  final _expanderKey = GlobalKey<ExpanderState>();

  // ExpanderState reports programmatic changes through onStateChanged too, so
  // a value set from Python is not echoed back as a change event.
  bool _settingValue = false;

  void _onStateChanged(bool expanded) {
    if (_settingValue) return;
    widget.control.updateProperties({"expanded": expanded});
    widget.control.triggerEvent("change", expanded);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentExpander build: ${widget.control.id}");

    final control = widget.control;
    final expanded = control.getBool("expanded", false)!;

    // Expander only takes an initial value: later changes from Python are
    // applied to its state after this frame.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final state = _expanderKey.currentState;
      if (state != null && state.isExpanded != expanded) {
        _settingValue = true;
        state.isExpanded = expanded;
        _settingValue = false;
      }
    });

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Expander(
          key: _expanderKey,
          header: control.buildTextOrWidget("header", required: true)!,
          content: control.buildWidget("content") ?? const SizedBox.shrink(),
          leading: control.buildIconOrWidget("leading"),
          trailing: control.buildWidget("trailing"),
          initiallyExpanded: expanded,
          enabled: !control.disabled,
          direction: parseEnum(
            ExpanderDirection.values,
            control.getString("direction"),
            ExpanderDirection.down,
          )!,
          contentPadding: control.getPadding(
            "content_padding",
            const EdgeInsets.all(16),
          )!,
          onStateChanged: _onStateChanged,
        ),
      ),
    );
  }
}
