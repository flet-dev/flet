import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadPopoverControl extends StatefulWidget {
  final Control control;

  const ShadPopoverControl({super.key, required this.control});

  @override
  State<ShadPopoverControl> createState() => _ShadPopoverControlState();
}

class _ShadPopoverControlState extends State<ShadPopoverControl> {
  late final ShadPopoverController _controller;

  // Only closing by tapping outside is reported; opening and closing from
  // Python is not echoed back.
  bool _settingOpen = false;

  @override
  void initState() {
    super.initState();
    _controller = ShadPopoverController(
      isOpen: widget.control.getBool("open", false)!,
    );
    _controller.addListener(_onControllerChanged);
  }

  @override
  void dispose() {
    _controller.removeListener(_onControllerChanged);
    _controller.dispose();
    super.dispose();
  }

  void _onControllerChanged() {
    if (_settingOpen || _controller.isOpen) return;
    widget.control.updateProperties({"open": false});
    widget.control.triggerEvent("dismiss");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadPopover build: ${widget.control.id}");

    final control = widget.control;

    final open = control.getBool("open", false)!;
    if (_controller.isOpen != open) {
      // The controller notifies listeners, and ShadPopover rebuilds its
      // overlay, from inside this build; defer it to after the frame.
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (!mounted) return;
        _settingOpen = true;
        _controller.setOpen(control.getBool("open", false)!);
        _settingOpen = false;
      });
    }

    final popover = ShadPopover(
      controller: _controller,
      closeOnTapOutside: control.getBool("close_on_tap_outside", true)!,
      popover: (context) =>
          control.buildWidget("popover") ?? const SizedBox.shrink(),
      child: control.buildWidget("content") ?? const SizedBox.shrink(),
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(context, popover),
    );
  }
}
