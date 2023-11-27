import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/buttons.dart';
import 'create_control.dart';
import 'error.dart';

class SegmentedButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const SegmentedButtonControl({
    Key? key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.dispatch,
  }) : super(key: key);

  @override
  State<SegmentedButtonControl> createState() => _SegmentedButtonControlState();
}

class _SegmentedButtonControlState extends State<SegmentedButtonControl> {
  void onChange(Set<String> selection) {
    var s = jsonEncode(selection.toList());
    debugPrint("onChange selection: $s");

    List<Map<String, String>> props = [
      {
        "i": widget.control.id,
        "selected": s,
      }
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));

    final server = FletAppServices.of(context).server;
    server.updateControlProps(props: props);
    server.sendPageEvent(
        eventTarget: widget.control.id, eventName: "change", eventData: s);
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
    debugPrint("selected: $selected");

    List<Control> segments =
        widget.children.where((c) => c.name == "segment").toList();
    debugPrint("segments: $segments");

    if (selected.isEmpty && !allowEmptySelection) {
      return const ErrorControl(
          "Selected property must contain at least one value.");
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
    debugPrint(
        "SegmentedButtonControl StoreConnector build: ${widget.control.id}");

    var sb = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) =>
            ControlsViewModel.fromStore(store, segments.map((s) => s.id)),
        builder: (content, segmentViews) {
          return SegmentedButton<String>(
              emptySelectionAllowed: allowEmptySelection,
              multiSelectionEnabled: allowMultipleSelection,
              selected: selected.isNotEmpty ? selected : {},
              showSelectedIcon: showSelectedIcon,
              style: style,
              selectedIcon: selectedIcon.isNotEmpty
                  ? createControl(
                      widget.control, selectedIcon.first.id, disabled)
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
                return ButtonSegment(
                    value: segmentView.control.attrString("value")!,
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
