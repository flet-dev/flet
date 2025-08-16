import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/error.dart';

class BannerControl extends StatefulWidget {
  final Control control;

  BannerControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<BannerControl> createState() => _BannerControlState();
}

class _BannerControlState extends State<BannerControl> {
  String? _error;

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

  MaterialBanner _createBanner() {
    return MaterialBanner(
      leading: widget.control.buildIconOrWidget("leading"),
      leadingPadding: widget.control.getPadding("leading_padding"),
      content: widget.control.buildTextOrWidget("content")!,
      padding: widget.control.getPadding("content_padding"),
      actions: widget.control.buildWidgets("actions"),
      forceActionsBelow: widget.control.getBool("force_actions_below", false)!,
      backgroundColor: widget.control.getColor("bgcolor", context),
      contentTextStyle:
          widget.control.getTextStyle("content_text_style", Theme.of(context)),
      surfaceTintColor: widget.control.getColor("surface_tint_color", context),
      shadowColor: widget.control.getColor("shadow_color", context),
      dividerColor: widget.control.getColor("divider_color", context),
      elevation: widget.control.getDouble("elevation"),
      minActionBarHeight:
          widget.control.getDouble("min_action_bar_height", 52.0)!,
      margin: widget.control.getMargin("margin"),
      onVisible: () {
        widget.control.triggerEvent("visible");
      },
    );
  }

  void _toggleBanner() {
    var dismissed = widget.control.get("_dismissed");

    debugPrint("Banner build: ${widget.control.id}, _dismissed=$dismissed");

    if (dismissed == true) return;

    final lastOpen = widget.control.getBool("_open", false)!;
    var open = widget.control.getBool("open", false)!;

    if (open && (open != lastOpen)) {
      if (widget.control.get("content") == null) {
        _error = "Banner.content must be provided and visible";
        return;
      } else if (widget.control.children("actions").isEmpty) {
        _error =
            "Banner.actions must be provided and at least one action should be visible";
        return;
      }

      widget.control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).removeCurrentMaterialBanner();
        ScaffoldMessenger.of(context)
            .showMaterialBanner(_createBanner())
            .closed
            .then((reason) {
          debugPrint(
              "Closing Banner(${widget.control.id}) with reason: $reason");
          if (widget.control.get("_dismissed") != true) {
            widget.control
                .updateProperties({"_dismissed": true}, python: false);
            debugPrint(
                "Dismissing Banner(${widget.control.id}) with reason: $reason");
            //_open = false;
            widget.control.updateProperties({"_open": false}, python: false);
            widget.control.updateProperties({"open": false});
            widget.control.triggerEvent("dismiss");
          }
        });
      });
    } else if (!open && lastOpen) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).hideCurrentMaterialBanner();
        widget.control.updateProperties({"_open": false}, python: false);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return _error != null ? ErrorControl(_error!) : const SizedBox.shrink();
  }
}
