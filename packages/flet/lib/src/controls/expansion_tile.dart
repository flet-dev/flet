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

    var ctrls = children.where((c) => c.name == "controls" && c.isVisible);
    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);
    var titleCtrls = children.where((c) => c.name == "title" && c.isVisible);
    var subtitleCtrls =
        children.where((c) => c.name == "subtitle" && c.isVisible);
    var trailingCtrls =
        children.where((c) => c.name == "trailing" && c.isVisible);

    if (titleCtrls.isEmpty) {
      return const ErrorControl(
          "ExpansionTile.title must be provided and visible");
    }

    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;
    bool onchange = control.attrBool("onchange", false)!;
    bool maintainState = control.attrBool("maintainState", false)!;
    bool initiallyExpanded = control.attrBool("initiallyExpanded", false)!;

    var iconColor = control.attrColor("iconColor", context);
    var textColor = control.attrColor("textColor", context);
    var bgColor = control.attrColor("bgColor", context);
    var collapsedBgColor = control.attrColor("collapsedBgColor", context);
    var collapsedIconColor = control.attrColor("collapsedIconColor", context);
    var collapsedTextColor = control.attrColor("collapsedTextColor", context);

    var affinity = parseListTileControlAffinity(
        control.attrString("affinity"), ListTileControlAffinity.platform)!;
    var clipBehavior =
        parseClip(control.attrString("clipBehavior"), Clip.none)!;

    var expandedCrossAxisAlignment = parseCrossAxisAlignment(
        control.attrString("crossAxisAlignment"), CrossAxisAlignment.center)!;

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
          parseCrossAxisAlignment(control.attrString("crossAxisAlignment")),
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
      visualDensity: parseVisualDensity(control.attrString("visualDensity")),
      enableFeedback: control.attrBool("enableFeedback"),
      showTrailingIcon: control.attrBool("showTrailingIcon", true)!,
      enabled: !disabled,
      minTileHeight: control.attrDouble("minTileHeight"),
      dense: control.attrBool("dense"),
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
