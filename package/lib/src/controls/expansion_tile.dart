import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateless_mixin.dart';

class ExpansionTileControl extends StatelessWidget
    with FletControlStatelessMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ExpansionTileControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

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
      return const ErrorControl("ExpansionTile requires a title!");
    }

    bool disabled = control.isDisabled || parentDisabled;
    bool onchange = control.attrBool("onchange", false)!;
    bool maintainState = control.attrBool("maintainState", false)!;
    bool initiallyExpanded = control.attrBool("maintainState", false)!;

    var iconColor = HexColor.fromString(
        Theme.of(context), control.attrString("iconColor", "")!);
    var textColor = HexColor.fromString(
        Theme.of(context), control.attrString("textColor", "")!);
    var bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    var collapsedBgColor = HexColor.fromString(
        Theme.of(context), control.attrString("collapsedBgColor", "")!);
    var collapsedIconColor = HexColor.fromString(
        Theme.of(context), control.attrString("collapsedIconColor", "")!);
    var collapsedTextColor = HexColor.fromString(
        Theme.of(context), control.attrString("collapsedTextColor", "")!);

    var affinity = ListTileControlAffinity.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("affinity", "")!.toLowerCase(),
        orElse: () => ListTileControlAffinity.platform);
    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.none);

    var expandedCrossAxisAlignment = parseCrossAxisAlignment(
        control, "crossAxisAlignment", CrossAxisAlignment.center);

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
            sendControlEvent(context, control.id, "change", "$expanded");
          }
        : null;

    Widget tile = ExpansionTile(
      controlAffinity: affinity,
      childrenPadding: parseEdgeInsets(control, "controlsPadding"),
      tilePadding: parseEdgeInsets(control, "tilePadding"),
      expandedAlignment: parseAlignment(control, "expandedAlignment"),
      expandedCrossAxisAlignment: parseCrossAxisAlignment(
          control, "crossAxisAlignment", CrossAxisAlignment.center),
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
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, disabled)
          : null,
      title: createControl(control, titleCtrls.first.id, disabled),
      subtitle: subtitleCtrls.isNotEmpty
          ? createControl(control, subtitleCtrls.first.id, disabled)
          : null,
      trailing: trailingCtrls.isNotEmpty
          ? createControl(control, trailingCtrls.first.id, disabled)
          : null,
      children: ctrls.isNotEmpty
          ? ctrls.map((c) => createControl(control, c.id, disabled)).toList()
          : [],
    );

    return constrainedControl(context, tile, parent, control);
  }
}
