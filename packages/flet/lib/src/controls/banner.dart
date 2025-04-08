import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../widgets/error.dart';

class BannerControl extends StatefulWidget {
  final Control control;

  BannerControl({Key? key, required this.control})
      : super(key: ValueKey(control.id));

  @override
  State<BannerControl> createState() => _BannerControlState();
}

class _BannerControlState extends State<BannerControl> {
  Widget? _dialog;

  @override
  void initState() {
    super.initState();
    debugPrint("Banner.initState: ${widget.control.id}");
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    debugPrint("Banner.didChangeDependencies: ${widget.control.id}");
    _toggleBanner();
  }

  @override
  void didUpdateWidget(covariant BannerControl oldWidget) {
    debugPrint("Banner.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
    _toggleBanner();
  }

  Widget _createBanner(FletBackend backend) {
    var leading = widget.control.buildWidget("leading");
    var content = widget.control.buildWidget("content");
    var actions = widget.control.buildWidgets("actions");

    if (content == null) {
      return const ErrorControl("Banner.content must be provided and visible");
    } else if (actions.isEmpty) {
      return const ErrorControl(
          "Banner.actions must be provided and at least one action should be visible");
    }

    return MaterialBanner(
      leading: leading,
      leadingPadding: widget.control.getPadding("leading_padding"),
      content: content,
      padding: widget.control.getPadding("content_padding"),
      actions: actions,
      forceActionsBelow: widget.control.getBool("force_actions_below", false)!,
      backgroundColor: widget.control.getColor("bgcolor", context),
      contentTextStyle: parseTextStyle(
        widget.control.get("content_text_style"),
        Theme.of(context),
      ),
      surfaceTintColor: widget.control.getColor("surface_tint_color", context),
      shadowColor: widget.control.getColor("shadow_color", context),
      dividerColor: widget.control.getColor("divider_color", context),
      elevation: widget.control.getDouble("elevation"),
      minActionBarHeight:
          widget.control.getDouble("min_action_bar_height", 52.0)!,
      margin: widget.control.getMargin("margin"),
      onVisible: () {
        backend.triggerControlEvent(widget.control, "visible");
      },
    );
  }

  void _toggleBanner() {
    var dismissed = widget.control.get("_dismissed");
    final lastOpen = widget.control.getBool("_open", false)!;

    debugPrint("Banner build: ${widget.control.id}, _dismissed=$dismissed");
    debugPrint("STATE: $hashCode");

    if (dismissed == true) return;

    var open = widget.control.getBool("open", false)!;

    var backend = FletBackend.of(context);

    if (open && (open != lastOpen)) {
      _dialog = _createBanner(FletBackend.of(context));

      if (_dialog is ErrorControl) {
        debugPrint(
            "Banner: ErrorControl, not showing dialog: ${(_dialog as ErrorControl).message}");
        return;
      }

      debugPrint(
          "Banner build 2: ${widget.control.id}, _open=$lastOpen, open=$open");

      backend.updateControl(widget.control.id, {"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).removeCurrentMaterialBanner();
        ScaffoldMessenger.of(context)
            .showMaterialBanner(_dialog as MaterialBanner)
            .closed
            .then((reason) {
          debugPrint(
              "Closing Banner(${widget.control.id}) with reason: $reason");
          debugPrint("STATE: $hashCode");
          if (widget.control.get("_dismissed") != true) {
            backend.updateControl(widget.control.id, {"_dismissed": true},
                python: false);
            debugPrint(
                "Dismissing Banner(${widget.control.id}) with reason: $reason");
            //_open = false;
            backend.updateControl(widget.control.id, {"_open": false},
                python: false);
            backend.updateControl(widget.control.id, {"open": false});
            backend.triggerControlEvent(widget.control, "dismiss");
          }
        });
      });
    } else if (!open && lastOpen) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).hideCurrentMaterialBanner();
        backend.updateControl(widget.control.id, {"_open": false},
            python: false);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return _dialog is ErrorControl ? _dialog! : const SizedBox.shrink();
  }
}
