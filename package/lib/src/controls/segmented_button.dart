import 'dart:convert';

import 'package:flutter/material.dart';
import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/desktop.dart';
import 'create_control.dart';
import '../utils/buttons.dart';
import '../utils/debouncer.dart';
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
  final _debouncer = Debouncer(milliseconds: isDesktop() ? 10 : 100);
  Set calendarView = {"1"};

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  void onChange(var selections) {
    List s = jsonDecode(selections.toList().toString());
    debugPrint("onChange values: $s");

    List<Map<String, String>> props = [
      {
        "i": widget.control.id,
        "selected": s.toString(),
      }
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));

    _debouncer.run(() {
      final server = FletAppServices.of(context).server;
      server.updateControlProps(props: props);
      server.sendPageEvent(
          eventTarget: widget.control.id,
          eventName: "change",
          eventData: s.toString());
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SegmentedButtonControl build: ${widget.control.id}");
    debugPrint("ATTRS: ${widget.control.attrs}");

    debugPrint("CHILDREN: ${widget.children}");

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

    Set selected = jsonDecode(widget.control.attrString("selected", "[]")!).toSet();
    debugPrint("selected: $selected");

    List<Control?> segments =
        widget.children.where((c) => c.name == "segment").toList();
    debugPrint("segments: $segments");

    if (selected.isEmpty) {
      return const ErrorControl(
          "Selected property must contain at least one value.");
    }

    if (!allowMultipleSelection && selected.length != 1) {
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

    var sb = SegmentedButton(
        emptySelectionAllowed: allowEmptySelection,
        multiSelectionEnabled: allowMultipleSelection,
        selected: selected.isNotEmpty ? selected: {},
        showSelectedIcon: showSelectedIcon,
        style: style,
        selectedIcon: selectedIcon.isNotEmpty
            ? createControl(widget.control, selectedIcon.first.id, disabled)
            : null,
        onSelectionChanged: !disabled
            ? (newSelection) {
                debugPrint("onSelectionChanged: $newSelection");
                onChange(newSelection.toSet());
                setState() {
                  selected = newSelection;
                }
              }
            : null,
        segments: List.generate(segments.length, (int index) {
          return ButtonSegment(
              value: index.toString(), label: Text(index.toString()));
        }));

    return constrainedControl(context, sb, widget.parent, widget.control);
  }
}
