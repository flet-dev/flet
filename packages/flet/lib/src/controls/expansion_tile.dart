import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import '../utils/theme.dart';
import 'create_control.dart';
import 'error.dart';

class ExpansionTileControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const ExpansionTileControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionTile build: ${control.id}");

    var ctrls = children.where((c) => c.name == "controls" && c.visible);
    var leadingCtrls = children.where((c) => c.name == "leading" && c.visible);
    var titleCtrls = children.where((c) => c.name == "title" && c.visible);
    var subtitleCtrls =
        children.where((c) => c.name == "subtitle" && c.visible);
    var trailingCtrls =
        children.where((c) => c.name == "trailing" && c.visible);

    if (titleCtrls.isEmpty) {
      return const ErrorControl(
          "ExpansionTile.title must be provided and visible");
    }

    bool disabled = control.disabled || parentDisabled;
    bool? adaptive = control.getBool("adaptive") ?? parentAdaptive;
    bool onchange = control.getBool("onchange", false)!;
    bool maintainState = control.getBool("maintainState", false)!;
    bool initiallyExpanded = control.getBool("initiallyExpanded", false)!;

    var iconColor = control.getColor("iconColor", context);
    var textColor = control.getColor("textColor", context);
    var bgColor = control.getColor("bgColor", context);
    var collapsedBgColor = control.getColor("collapsedBgColor", context);
    var collapsedIconColor = control.getColor("collapsedIconColor", context);
    var collapsedTextColor = control.getColor("collapsedTextColor", context);

    var affinity = parseListTileControlAffinity(
        control.getString("affinity"), ListTileControlAffinity.platform)!;
    var clipBehavior = parseClip(control.getString("clipBehavior"), Clip.none)!;

    var expandedCrossAxisAlignment = parseCrossAxisAlignment(
        control.getString("crossAxisAlignment"), CrossAxisAlignment.center)!;

    if (expandedCrossAxisAlignment == CrossAxisAlignment.baseline) {
      return const ErrorControl(
          'CrossAxisAlignment.baseline is not supported since the expanded '
          'controls are aligned in a column, not a row. '
          'Try aligning the controls differently.');
    }

    Function(bool)? onChange = (onchange) && !disabled
        ? (expanded) {
            debugPrint(
                "ExpansionTile ${control.id} was ${expanded ? "expanded" : "collapsed"}");
            backend.triggerControlEvent(control.id, "change", "$expanded");
          }
        : null;

    Widget tile = ExpansionTile(
      controlAffinity: affinity,
      childrenPadding: parseEdgeInsets(control, "controlsPadding"),
      tilePadding: parseEdgeInsets(control, "tilePadding"),
      expandedAlignment: parseAlignment(control, "expandedAlignment"),
      expandedCrossAxisAlignment:
          parseCrossAxisAlignment(control.getString("crossAxisAlignment")),
      backgroundColor: bgColor,
      iconColor: iconColor,
      textColor: textColor,
      collapsedBackgroundColor: collapsedBgColor,
      collapsedIconColor: collapsedIconColor,
      collapsedTextColor: collapsedTextColor,
      maintainState: maintainState,
      initiallyExpanded: initiallyExpanded,
      clipBehavior: clipBehavior,
      shape: parseOutlinedBorder(control, "shape"),
      collapsedShape: parseOutlinedBorder(control, "collapsedShape"),
      onExpansionChanged: onChange,
      visualDensity: parseVisualDensity(control.getString("visualDensity")),
      enableFeedback: control.getBool("enableFeedback"),
      showTrailingIcon: control.getBool("showTrailingIcon", true)!,
      enabled: !disabled,
      minTileHeight: control.getDouble("minTileHeight"),
      dense: control.getBool("dense"),
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, disabled,
              parentAdaptive: adaptive)
          : null,
      title: createControl(control, titleCtrls.first.id, disabled,
          parentAdaptive: adaptive),
      subtitle: subtitleCtrls.isNotEmpty
          ? createControl(control, subtitleCtrls.first.id, disabled,
              parentAdaptive: adaptive)
          : null,
      trailing: trailingCtrls.isNotEmpty
          ? createControl(control, trailingCtrls.first.id, disabled,
              parentAdaptive: adaptive)
          : null,
      children: ctrls
          .map((c) =>
              createControl(control, c.id, disabled, parentAdaptive: adaptive))
          .toList(),
    );

    return constrainedControl(context, tile, parent, control);
  }
}
