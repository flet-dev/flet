import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class BannerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;

  const BannerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.nextChild});

  @override
  State<BannerControl> createState() => _BannerControlState();
}

class _BannerControlState extends State<BannerControl> {
  bool _open = false;

  Widget _createBanner() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.isVisible);
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.isVisible);

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Banner does not have any content.");
    } else if (actionCtrls.isEmpty) {
      return const ErrorControl("Banner should have at least one action.");
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
      forceActionsBelow: widget.control.attrBool("forceActionsBelow", false)!,
      backgroundColor: widget.control.attrColor("bgcolor", context),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Banner build: ${widget.control.id}");

    debugPrint("Banner build: ${widget.control.id}");

    var open = widget.control.attrBool("open", false)!;

    debugPrint("Current open state: $_open");
    debugPrint("New open state: $open");

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
