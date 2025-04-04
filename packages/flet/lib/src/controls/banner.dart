import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../widgets/error.dart';

class BannerControl extends StatefulWidget {
  final Control control;

  const BannerControl({super.key, required this.control});

  @override
  State<BannerControl> createState() => _BannerControlState();
}

class _BannerControlState extends State<BannerControl> {
  bool _open = false;

  Widget _createBanner() {
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
      leadingPadding: parseEdgeInsets(widget.control, "leading_padding"),
      content: content,
      padding: parseEdgeInsets(widget.control, "content_padding"),
      actions: actions,
      forceActionsBelow: widget.control.getBool("force_actions_below", false)!,
      backgroundColor: widget.control.getColor("bgcolor", context),
      contentTextStyle: parseTextStyle(
          Theme.of(context), widget.control, "content_text_style"),
      surfaceTintColor: widget.control.getColor("surface_tint_color", context),
      shadowColor: widget.control.getColor("shadow_color", context),
      dividerColor: widget.control.getColor("divider_color", context),
      elevation: widget.control.getDouble("elevation"),
      minActionBarHeight:
          widget.control.getDouble("min_action_bar_height", 52.0)!,
      margin: parseEdgeInsets(widget.control, "margin"),
      onVisible: () {
        FletBackend.of(context).triggerControlEvent(widget.control, "visible");
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Banner build: ${widget.control.id}");

    var open = widget.control.getBool("open", false)!;

    if (open && (open != _open)) {
      var banner = _createBanner();
      if (banner is ErrorControl) {
        return banner;
      }

      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).removeCurrentMaterialBanner();

        ScaffoldMessenger.of(context)
            .showMaterialBanner(banner as MaterialBanner);
      });
    } else if (open != _open && _open) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).removeCurrentMaterialBanner();
      });
    }

    _open = open;

    return const SizedBox.shrink();
  }
}
