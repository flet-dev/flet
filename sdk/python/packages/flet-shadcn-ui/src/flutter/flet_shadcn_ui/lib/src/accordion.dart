import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadAccordionControl extends StatefulWidget {
  final Control control;

  const ShadAccordionControl({super.key, required this.control});

  @override
  State<ShadAccordionControl> createState() => _ShadAccordionControlState();
}

class _ShadAccordionControlState extends State<ShadAccordionControl> {
  ShadAccordionController<String>? _controller;
  bool? _multiple;

  // ShadAccordion has no change callback, so changes are read from the
  // controller; a value set from Python must not be echoed back.
  bool _settingValue = false;

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  void _onControllerChanged() {
    if (_settingValue) return;
    final value = List<String>.of(_controller!.value);
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadAccordion build: ${widget.control.id}");

    final control = widget.control;
    final multiple = control.getBool("multiple", false)!;
    final value =
        control.get<List>("value")?.map((v) => v.toString()).toList() ?? [];

    if (_controller == null || _multiple != multiple) {
      _controller?.dispose();
      _controller = multiple
          ? ShadAccordionController<String>.multiple(value)
          : ShadAccordionController<String>(value.firstOrNull);
      _controller!.addListener(_onControllerChanged);
      _multiple = multiple;
    } else if (!_sameItems(_controller!.value, value)) {
      _settingValue = true;
      _controller!.value = multiple ? value : value.take(1).toList();
      _settingValue = false;
    }

    final items = control.buildWidgets("items");
    final accordion = multiple
        ? ShadAccordion<String>.multiple(
            key: const ValueKey("multiple"),
            controller: _controller,
            children: items,
          )
        : ShadAccordion<String>(
            key: const ValueKey("single"),
            controller: _controller,
            children: items,
          );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, accordion),
    );
  }
}

bool _sameItems(List<String> a, List<String> b) =>
    a.length == b.length && a.toSet().containsAll(b);

/// A `flet_shadcn_ui.AccordionItem`; must be inside a `ShadAccordionControl`.
class ShadAccordionItemControl extends StatelessWidget {
  final Control control;

  const ShadAccordionItemControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    return ShadAccordionItem<String>(
      value: control.getString("value", "")!,
      title: control.buildTextOrWidget("title", required: true)!,
      child: control.buildWidget("content") ?? const SizedBox.shrink(),
    );
  }
}
