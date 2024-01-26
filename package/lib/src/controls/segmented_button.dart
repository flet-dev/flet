import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/buttons.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateful_mixin.dart';
import 'flet_store_mixin.dart';

class SegmentedButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SegmentedButtonControl({
    super.key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
  });

  @override
  State<SegmentedButtonControl> createState() => _SegmentedButtonControlState();
}

class _SegmentedButtonControlState extends State<SegmentedButtonControl>
    with FletControlStatefulMixin, FletStoreMixin {
  void onChange(Set<String> selection) {
    var s = jsonEncode(selection.toList());
    updateControlProps(widget.control.id, {"selected": s});
    sendControlEvent(widget.control.id, "change", s);
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
        defaultBorderSide: BorderSide.none,
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

    List<Control> segments =
        widget.children.where((c) => c.name == "segment").toList();

    if (selected.isEmpty && !allowEmptySelection) {
      return const ErrorControl("When allow_empty_selection is False, "
          "the selected property must contain at least one value.");
    }

    if (!allowMultipleSelection &&
        selected.length != 1 &&
        !allowEmptySelection) {
      return const ErrorControl("When allow_multiple_selection is False, "
          "the selected property must contain exactly one value.");
    }

    if (allowMultipleSelection && selected.length > segments.length) {
      return const ErrorControl("The length of the selected property must "
          "be less than or equal to the number of segments.");
    }

    var selectedIcon = widget.children.where((c) => c.name == "selectedIcon");

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
          segments: segmentViews.controlViews.map((segmentView) {
            var iconCtrls = segmentView.children
                .where((c) => c.name == "icon" && c.isVisible);
            var labelCtrls = segmentView.children
                .where((c) => c.name == "label" && c.isVisible);
            var enabled = !segmentView.control.attrBool("disabled", false)!;

            return ButtonSegment(
                value: segmentView.control.attrString("value")!,
                enabled: enabled,
                tooltip: enabled && !disabled
                    ? segmentView.control.attrString("tooltip")
                    : null,
                icon: iconCtrls.isNotEmpty
                    ? createControl(
                        segmentView.control, iconCtrls.first.id, disabled)
                    : null,
                label: labelCtrls.isNotEmpty
                    ? createControl(
                        segmentView.control, labelCtrls.first.id, disabled)
                    : null);
          }).toList());
    });

    return constrainedControl(context, sb, widget.parent, widget.control);
  }
}
