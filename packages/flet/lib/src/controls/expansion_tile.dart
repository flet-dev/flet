import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
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
import 'control_widget.dart';

class ExpansionTileControl extends StatelessWidget {
  final Control control;

  const ExpansionTileControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionTile build: ${control.id}");

    var controls = control
        .children("controls")
        .map((child) => ControlWidget(control: child, key: ValueKey(child.id)))
        .toList();

    var leading = control.buildWidget("leading");
    var title = control.buildWidget("title");
    var subtitle = control.buildWidget("subtitle");
    var trailing = control.buildWidget("trailing");

    if (title == null) {
      return const ErrorControl(
          "ExpansionTile.title must be provided and visible");
    }

    bool maintainState = control.getBool("maintain_state", false)!;
    bool initiallyExpanded = control.getBool("initially_expanded", false)!;

    var iconColor = control.getColor("icon_color", context);
    var textColor = control.getColor("text_color", context);
    var bgColor = control.getColor("bgcolor", context);
    var collapsedBgColor = control.getColor("collapsed_bgcolor", context);
    var collapsedIconColor = control.getColor("collapsed_icon_color", context);
    var collapsedTextColor = control.getColor("collapsed_text_color", context);

    var affinity = control.getListTileControlAffinity(
        "affinity", ListTileControlAffinity.platform)!;
    var clipBehavior =
        parseClip(control.getString("clip_behavior"), Clip.none)!;

    var expandedCrossAxisAlignment = control.getCrossAxisAlignment(
        "expanded_cross_axis_alignment", CrossAxisAlignment.center)!;

    if (expandedCrossAxisAlignment == CrossAxisAlignment.baseline) {
      return const ErrorControl(
          'CrossAxisAlignment.baseline is not supported since the expanded '
          'controls are aligned in a column, not a row. '
          'Try aligning the controls differently.');
    }

    Function(bool)? onChange = !control.disabled
        ? (expanded) {
           control.triggerEvent("change", "$expanded");
          }
        : null;

    Widget tile = ExpansionTile(
      controlAffinity: affinity,
      childrenPadding: control.getPadding("controls_padding"),
      tilePadding: control.getEdgeInsets("tile_padding"),
      expandedAlignment: control.getAlignment("expanded_alignment"),
      expandedCrossAxisAlignment:
          control.getCrossAxisAlignment("expanded_cross_axis_alignment"),
      backgroundColor: bgColor,
      iconColor: iconColor,
      textColor: textColor,
      collapsedBackgroundColor: collapsedBgColor,
      collapsedIconColor: collapsedIconColor,
      collapsedTextColor: collapsedTextColor,
      maintainState: maintainState,
      initiallyExpanded: initiallyExpanded,
      clipBehavior: clipBehavior,
      shape: control.getShape("shape"),
      collapsedShape: control.getShape("collapsed_shape"),
      onExpansionChanged: onChange,
      visualDensity: control.getVisualDensity("visual_density"),
      enableFeedback: control.getBool("enable_feedback"),
      showTrailingIcon: control.getBool("show_trailing_icon", true)!,
      enabled: !control.disabled,
      minTileHeight: control.getDouble("min_tile_height"),
      dense: control.getBool("dense"),
      leading: leading,
      title: title,
      subtitle: subtitle,
      trailing: trailing,
      children: controls,
    );

    return ConstrainedControl(control: control, child: tile);
  }
}
