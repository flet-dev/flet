import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/menu.dart';
import 'utils/theme.dart';

/// A `flet_fluent_ui.Flyout`, or a `flet_fluent_ui.TeachingTip` when
/// [teachingTip] is true: [content] with a popup opened and closed by the
/// `open` property.
class FluentFlyoutControl extends StatefulWidget {
  final Control control;
  final bool teachingTip;

  const FluentFlyoutControl({
    super.key,
    required this.control,
    this.teachingTip = false,
  });

  @override
  State<FluentFlyoutControl> createState() => _FluentFlyoutControlState();
}

class _FluentFlyoutControlState extends State<FluentFlyoutControl> {
  final _controller = FlyoutController();
  // Whether a flyout was requested and not closed yet; the controller only
  // knows once the route is pushed, after the frame.
  bool _showing = false;

  Control get control => widget.control;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _show() async {
    final placement = parseEnum(
      FlyoutPlacementMode.values,
      control.getString("placement"),
      FlyoutPlacementMode.auto,
    )!;
    final dismissible = control.getBool("dismissible", true)!;

    // The popup rebuilds itself when the control changes. fluent_ui gives it
    // the themes around the target, such as a `Theme` control.
    Widget builder(BuildContext context) => ListenableBuilder(
      listenable: control,
      builder: (context, _) =>
          widget.teachingTip ? _buildTeachingTip() : _buildFlyout(),
    );

    // Not fluent_ui's showTeachingTip, which can't change the preferred side
    // of `auto`: it prefers above, and a tip for a control at the top of the
    // page then covers the control.
    await _controller.showFlyout<void>(
      placementMode: placement,
      autoModeConfiguration: FlyoutAutoConfiguration(
        preferredMode: FlyoutPlacementMode.bottomCenter,
      ),
      barrierDismissible: dismissible,
      dismissWithEsc: dismissible,
      dismissOnPointerMoveAway: control.getBool(
        "dismiss_on_pointer_move_away",
        false,
      )!,
      transitionBuilder: widget.teachingTip
          ? TeachingTip.defaultTransitionBuilder
          : null,
      builder: builder,
    );

    _showing = false;
    // Closed by the user, not by Python setting `open` to false.
    if (mounted && control.getBool("open", false)!) {
      control.updateProperties({"open": false});
      control.triggerEvent("dismiss");
    }
  }

  Widget _buildFlyout() {
    return FlyoutContent(
      child: control.buildWidget("flyout") ?? const SizedBox.shrink(),
    );
  }

  Widget _buildTeachingTip() {
    final buttons = control.buildWidgets("buttons");
    return TeachingTip(
      title: control.buildTextOrWidget("title", required: true)!,
      subtitle:
          control.buildTextOrWidget("subtitle") ?? const SizedBox.shrink(),
      leading: control.buildIconOrWidget("leading"),
      buttons: buttons.isEmpty ? null : buttons,
      // fluent_ui asserts that a tip has buttons or media, not both.
      mediaContent: buttons.isEmpty ? control.buildWidget("media") : null,
      onClose: control.getBool("show_close_button", true)!
          ? TeachingTip.defaultCloseCallback
          : null,
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("${control.type} build: ${control.id}");

    final open = control.getBool("open", false)!;

    if (open && !_showing) {
      _showing = true;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) _show();
      });
    } else if (!open && _showing) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_controller.isOpen) _controller.close<void>();
      });
    }

    return LayoutControl(
      control: control,
      // The flyout takes its theme from the FlyoutTarget, below this one.
      child: withFluentTheme(
        context,
        FlyoutTarget(
          controller: _controller,
          child: control.buildWidget("content") ?? const SizedBox.shrink(),
        ),
      ),
    );
  }
}

/// A `flet_fluent_ui.ContextMenu`: a menu opened at the pointer when
/// [content] is right-clicked or long-pressed.
class FluentContextMenuControl extends StatefulWidget {
  final Control control;

  const FluentContextMenuControl({super.key, required this.control});

  @override
  State<FluentContextMenuControl> createState() =>
      _FluentContextMenuControlState();
}

class _FluentContextMenuControlState extends State<FluentContextMenuControl> {
  final _controller = FlyoutController();

  Control get control => widget.control;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _open(BuildContext targetContext, Offset globalPosition) async {
    if (_controller.isOpen || control.disabled) return;
    // The menu is positioned in the navigator's coordinates.
    final navigatorBox =
        Navigator.of(targetContext).context.findRenderObject()! as RenderBox;
    control.triggerEvent("open");
    await _controller.showFlyout<void>(
      position: navigatorBox.globalToLocal(globalPosition),
      barrierColor: Colors.transparent,
      builder: (context) => ListenableBuilder(
        listenable: control,
        builder: (context, _) =>
            MenuFlyout(items: buildMenuFlyoutItems(control, "items")),
      ),
    );
    if (mounted) control.triggerEvent("dismiss");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentContextMenu build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Builder(
          builder: (targetContext) => GestureDetector(
            onSecondaryTapUp: (details) =>
                _open(targetContext, details.globalPosition),
            onLongPressStart: (details) =>
                _open(targetContext, details.globalPosition),
            child: FlyoutTarget(
              controller: _controller,
              child: control.buildWidget("content") ?? const SizedBox.shrink(),
            ),
          ),
        ),
      ),
    );
  }
}
