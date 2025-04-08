import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';

class SegmentedButtonControl extends StatefulWidget {
  final Control control;

  const SegmentedButtonControl({super.key, required this.control});

  @override
  State<SegmentedButtonControl> createState() => _SegmentedButtonControlState();
}

class _SegmentedButtonControlState extends State<SegmentedButtonControl>
    with FletStoreMixin {
  void onChange(Set<String> selection) {
    var s = selection.toList();
    widget.control.updateProperties({"selected": s}, context, notify: true);
    widget.control.triggerEvent("change", context, s);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SegmentedButtonControl build: ${widget.control.id}");

    var theme = Theme.of(context);
    var style = widget.control.getButtonStyle("style", Theme.of(context),
        defaultForegroundColor: theme.colorScheme.primary,
        defaultBackgroundColor: theme.colorScheme.surface,
        defaultOverlayColor: theme.colorScheme.primary.withOpacity(0.08),
        defaultShadowColor: theme.colorScheme.shadow,
        defaultSurfaceTintColor: theme.colorScheme.surfaceTint,
        defaultElevation: 1,
        defaultPadding: const EdgeInsets.symmetric(horizontal: 8),
        defaultShape: theme.useMaterial3
            ? const StadiumBorder()
            : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    var allowEmptySelection =
        widget.control.getBool("allow_empty_selection", false)!;
    var allowMultipleSelection =
        widget.control.getBool("allow_multiple_selection", false)!;
    var selected = widget.control
        .get<List>("selected", [])!
        .map((e) => e.toString())
        .toSet();
    var segments = widget.control.children("segments");

    if (segments.isEmpty) {
      return const ErrorControl(
          "SegmentedButton.segments must be contain at least one visible segment");
    }

    if (selected.isEmpty && !allowEmptySelection) {
      return const ErrorControl(
          "SegmentedButton.selected must contain at least one value because allow_empty_selection=False");
    }

    if (!allowMultipleSelection &&
        selected.length != 1 &&
        !allowEmptySelection) {
      return const ErrorControl(
          "SegmentedButton.selected must contain exactly one value because allow_multiple_selection=False");
    }

    if (allowMultipleSelection && selected.length > segments.length) {
      return const ErrorControl(
          "The length of SegmentedButton.selected must be less than or equal to the number of visible segments");
    }

    var segmentedButton = SegmentedButton<String>(
        emptySelectionAllowed: allowEmptySelection,
        multiSelectionEnabled: allowMultipleSelection,
        selected: selected,
        showSelectedIcon: widget.control.getBool("show_selected_icon", true)!,
        style: style,
        selectedIcon: widget.control.buildWidget("selected_icon"),
        onSelectionChanged: !widget.control.disabled
            ? (newSelection) => onChange(newSelection)
            : null,
        direction: widget.control.getAxis("direction", Axis.horizontal)!,
        expandedInsets: widget.control.getPadding("padding"),
        segments: segments.map((segment) {
          return ButtonSegment(
              value: segment.getString("value")!,
              enabled: !segment.disabled,
              tooltip: segment.disabled ? null : segment.getString("tooltip"),
              icon: segment.buildWidget("icon"),
              label: segment.buildWidget("label"));
        }).toList());

    return ConstrainedControl(control: widget.control, child: segmentedButton);
  }
}
