import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'error.dart';

class BannerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const BannerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.nextChild,
      required this.backend});

  @override
  State<BannerControl> createState() => _BannerControlState();
}

class _BannerControlState extends State<BannerControl> {
  bool _open = false;

  Widget _createBanner() {
    bool disabled = widget.control.disabled || widget.parentDisabled;
    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.visible);
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.visible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.visible);

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Banner.content must be provided and visible");
    } else if (actionCtrls.isEmpty) {
      return const ErrorControl(
          "Banner.actions must be provided and at least one action should be visible");
    }

    return MaterialBanner(
      leading: leadingCtrls.isNotEmpty
          ? createControl(widget.control, leadingCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      leadingPadding: parseEdgeInsets(widget.control, "leadingPadding"),
      content: createControl(widget.control, contentCtrls.first.id, disabled,
          parentAdaptive: widget.parentAdaptive),
      padding: parseEdgeInsets(widget.control, "contentPadding"),
      actions: actionCtrls
          .map((c) => createControl(widget.control, c.id, disabled,
              parentAdaptive: widget.parentAdaptive))
          .toList(),
      forceActionsBelow: widget.control.getBool("forceActionsBelow", false)!,
      backgroundColor: widget.control.getColor("bgcolor", context),
      contentTextStyle:
          parseTextStyle(Theme.of(context), widget.control, "contentTextStyle"),
      surfaceTintColor: widget.control.getColor("surfaceTintColor", context),
      shadowColor: widget.control.getColor("shadowColor", context),
      dividerColor: widget.control.getColor("dividerColor", context),
      elevation: widget.control.getDouble("elevation"),
      minActionBarHeight: widget.control.getDouble("minActionBarHeight", 52.0)!,
      margin: parseEdgeInsets(widget.control, "margin"),
      onVisible: () {
        widget.backend.triggerControlEvent(widget.control.id, "visible");
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Banner build: ${widget.control.id}");

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

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
