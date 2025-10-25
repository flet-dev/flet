import 'package:flet/src/utils/animations.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/theme.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ExpansionTileControl extends StatefulWidget {
  final Control control;

  const ExpansionTileControl({super.key, required this.control});

  @override
  State<ExpansionTileControl> createState() => _ExpansionTileControlState();
}

class _ExpansionTileControlState extends State<ExpansionTileControl> {
  late final ExpansibleController _controller;
  bool _expanded = false;

  @override
  void initState() {
    super.initState();
    _controller = ExpansibleController();
    _expanded = widget.control.getBool("expanded", false)!;
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  // Schedules an update to the controller after the current frame.
  // This ensures the expansion/collapse animation is triggered safely.
  void _scheduleControllerUpdate(bool expanded) {
    SchedulerBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return; // Prevents updates if the widget is disposed.

      if (expanded) {
        _controller.expand();
      } else {
        _controller.collapse();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionTile build: ${widget.control.id}");

    final title = widget.control.buildTextOrWidget("title");
    if (title == null) {
      return const ErrorControl(
          "ExpansionTile.title must be provided and visible");
    }

    var expanded = widget.control.getBool("expanded", false)!;
    if (_expanded != expanded) {
      _expanded = expanded;
      _scheduleControllerUpdate(expanded);
    }

    var expandedCrossAxisAlignment = widget.control.getCrossAxisAlignment(
        "expanded_cross_axis_alignment", CrossAxisAlignment.center)!;
    if (expandedCrossAxisAlignment == CrossAxisAlignment.baseline) {
      return const ErrorControl(
          'CrossAxisAlignment.BASELINE is not supported since the expanded '
          'controls are aligned in a column, not a row. '
          'Try aligning the controls differently.');
    }

    final tile = ExpansionTile(
      controller: _controller,
      controlAffinity: widget.control.getListTileControlAffinity("affinity"),
      childrenPadding: widget.control.getPadding("controls_padding"),
      tilePadding: widget.control.getEdgeInsets("tile_padding"),
      expandedAlignment: widget.control.getAlignment("expanded_alignment"),
      expandedCrossAxisAlignment: expandedCrossAxisAlignment,
      backgroundColor: widget.control.getColor("bgcolor", context),
      iconColor: widget.control.getColor("icon_color", context),
      textColor: widget.control.getColor("text_color", context),
      collapsedBackgroundColor:
          widget.control.getColor("collapsed_bgcolor", context),
      collapsedIconColor:
          widget.control.getColor("collapsed_icon_color", context),
      collapsedTextColor:
          widget.control.getColor("collapsed_text_color", context),
      maintainState: widget.control.getBool("maintain_state", false)!,
      initiallyExpanded: expanded,
      clipBehavior: widget.control.getClipBehavior("clip_behavior"),
      shape: widget.control.getShape("shape", Theme.of(context)),
      collapsedShape:
          widget.control.getShape("collapsed_shape", Theme.of(context)),
      onExpansionChanged: (bool expanded) {
        _expanded = expanded;
        widget.control.updateProperties({"expanded": expanded});
        widget.control.triggerEvent("change", expanded);
      },
      visualDensity: widget.control.getVisualDensity("visual_density"),
      enableFeedback: widget.control.getBool("enable_feedback"),
      showTrailingIcon: widget.control.getBool("show_trailing_icon", true)!,
      enabled: !widget.control.disabled,
      minTileHeight: widget.control.getDouble("min_tile_height"),
      dense: widget.control.getBool("dense"),
      expansionAnimationStyle:
          widget.control.getAnimationStyle("animation_style"),
      leading: widget.control.buildIconOrWidget("leading"),
      title: title,
      subtitle: widget.control.buildTextOrWidget("subtitle"),
      trailing: widget.control.buildIconOrWidget("trailing"),
      children: widget.control.buildWidgets("controls"),
    );

    return LayoutControl(control: widget.control, child: tile);
  }
}
