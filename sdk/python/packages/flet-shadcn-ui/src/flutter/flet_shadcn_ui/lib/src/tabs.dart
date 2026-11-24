import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/icons.dart';
import 'utils/theme.dart';

class ShadTabsControl extends StatefulWidget {
  final Control control;

  const ShadTabsControl({super.key, required this.control});

  @override
  State<ShadTabsControl> createState() => _ShadTabsControlState();
}

class _ShadTabsControlState extends State<ShadTabsControl> {
  ShadTabsController<String>? _controller;

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  void _onChanged(String value) {
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadTabs build: ${widget.control.id}");

    final control = widget.control;
    final tabs = control.children("tabs");
    if (tabs.isEmpty) return const SizedBox.shrink();

    final value =
        control.getString("value") ?? tabs.first.getString("value", "")!;
    if (_controller == null) {
      _controller = ShadTabsController<String>(value: value);
    } else if (_controller!.selected != value) {
      _controller!.select(value);
    }

    // ShadTabs needs typed ShadTab<String> children, so each tab is built from
    // its control's properties instead of being rendered as a control.
    final shadTabs = ShadTabs<String>(
      controller: _controller,
      gap: control.getDouble("gap"),
      onChanged: _onChanged,
      tabs: [
        for (final tab in tabs)
          ShadTab<String>(
            value: tab.getString("value", "")!,
            enabled: !tab.disabled,
            leading: buildShadIconOrWidget(tab, "icon"),
            content: tab.buildWidget("content"),
            child: tab.buildTextOrWidget("label", required: true)!,
          ),
      ],
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, shadTabs),
    );
  }
}
