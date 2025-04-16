import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class SegmentedButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const SegmentedButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<SegmentedButtonControl> createState() => _SegmentedButtonControlState();
}

class _SegmentedButtonControlState extends State<SegmentedButtonControl>
    with FletStoreMixin {
  void onChange(Set<String> selection) {
    var s = jsonEncode(selection.toList());
    widget.backend.updateControlState(widget.control.id, {"selected": s});
    widget.backend.triggerControlEvent(widget.control.id, "change", s);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SegmentedButtonControl build: ${widget.control.id}");

    var theme = Theme.of(context);
    var style = parseButtonStyle(Theme.of(context), widget.control, "style",
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

    bool allowEmptySelection =
        widget.control.attrBool("allowEmptySelection", false)!;

    bool allowMultipleSelection =
        widget.control.attrBool("allowMultipleSelection", false)!;

    Set<String> selected =
        (jsonDecode(widget.control.attrString("selected", "[]")!) as List)
            .map((e) => e.toString())
            .toSet();

    List<Control> segments = widget.children
        .where((c) => c.name == "segment" && c.isVisible)
        .toList();

    if (segments.isEmpty) {
      return const ErrorControl(
          "SegmentedButton.segments must be provided and contain at minimum one visible segment");
    }

    if (selected.isEmpty && !allowEmptySelection) {
      return const ErrorControl(
          "SegmentedButton.selected must be provided and contain at minimum one value because allow_empty_selection=False");
    }

    if (!allowMultipleSelection &&
        selected.length != 1 &&
        !allowEmptySelection) {
      return const ErrorControl(
          "SegmentedButton.selected must be provided and contain exactly one value because allow_multiple_selection=False");
    }

    if (allowMultipleSelection && selected.length > segments.length) {
      return const ErrorControl(
          "The length of SegmentedButton.selected must be less than or equal to the number of visible segments");
    }

    var selectedIcon =
        widget.children.where((c) => c.name == "selectedIcon" && c.isVisible);

    bool showSelectedIcon = widget.control.attrBool("showSelectedIcon", true)!;

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    debugPrint("SegmentedButtonControl build: ${widget.control.id}");

    var sb = withControls(segments.map((s) => s.id), (content, segmentViews) {
      return SegmentedButton<String>(
          emptySelectionAllowed: allowEmptySelection,
          multiSelectionEnabled: allowMultipleSelection,
          selected: selected.isNotEmpty ? selected : {},
          showSelectedIcon: showSelectedIcon,
          style: style,
          selectedIcon: selectedIcon.isNotEmpty
              ? createControl(widget.control, selectedIcon.first.id, disabled)
              : null,
          onSelectionChanged: !disabled
              ? (newSelection) {
                  onChange(newSelection.toSet());
                }
              : null,
          direction: parseAxis(
              widget.control.attrString("direction"), Axis.horizontal)!,
          expandedInsets: parseEdgeInsets(widget.control, "padding"),
          segments: segmentViews.controlViews.map((segmentView) {
            var iconCtrls = segmentView.children
                .where((c) => c.name == "icon" && c.isVisible);
            var labelCtrls = segmentView.children
                .where((c) => c.name == "label" && c.isVisible);
            var segmentDisabled = segmentView.control.isDisabled || disabled;
            var segmentTooltip = segmentView.control.attrString("tooltip");
            return ButtonSegment(
                value: segmentView.control.attrString("value")!,
                enabled: !segmentDisabled,
                tooltip: segmentDisabled ? null : segmentTooltip,
                icon: iconCtrls.isNotEmpty
                    ? createControl(segmentView.control, iconCtrls.first.id,
                        segmentDisabled)
                    : null,
                label: labelCtrls.isNotEmpty
                    ? createControl(segmentView.control, labelCtrls.first.id,
                        segmentDisabled)
                    : null);
          }).toList());
    });

    return constrainedControl(context, sb, widget.parent, widget.control);
  }
}
