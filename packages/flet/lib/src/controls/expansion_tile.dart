import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
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

    var leading = control.child("leading");
    var title = control.child("title");
    var subtitle = control.child("subtitle");
    var trailing = control.child("trailing");

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

    var affinity = parseListTileControlAffinity(
        control.getString("affinity"), ListTileControlAffinity.platform)!;
    var clipBehavior =
        parseClip(control.getString("clip_behavior"), Clip.none)!;

    var expandedCrossAxisAlignment = parseCrossAxisAlignment(
        control.getString("expanded_cross_axis_alignment"),
        CrossAxisAlignment.center)!;

    if (expandedCrossAxisAlignment == CrossAxisAlignment.baseline) {
      return const ErrorControl(
          'CrossAxisAlignment.baseline is not supported since the expanded '
          'controls are aligned in a column, not a row. '
          'Try aligning the controls differently.');
    }

    Function(bool)? onChange = !control.disabled
        ? (expanded) {
            debugPrint(
                "ExpansionTile ${control.id} was ${expanded ? "expanded" : "collapsed"}");
            FletBackend.of(context)
                .triggerControlEvent(control, "change", "$expanded");
          }
        : null;

    Widget tile = ExpansionTile(
      controlAffinity: affinity,
      childrenPadding: parseEdgeInsets(control, "controls_padding"),
      tilePadding: parseEdgeInsets(control, "tile_padding"),
      expandedAlignment: parseAlignment(control, "expanded_alignment"),
      expandedCrossAxisAlignment: parseCrossAxisAlignment(
          control.getString("expanded_cross_axis_alignment")),
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
      collapsedShape: parseOutlinedBorder(control, "collapsed_shape"),
      onExpansionChanged: onChange,
      visualDensity: parseVisualDensity(control.getString("visual_density")),
      enableFeedback: control.getBool("enable_feedback"),
      showTrailingIcon: control.getBool("show_trailing_icon", true)!,
      enabled: !control.disabled,
      minTileHeight: control.getDouble("min_tile_height"),
      dense: control.getBool("dense"),
      leading: leading is Control ? ControlWidget(control: leading) : null,
      title: ControlWidget(control: title),
      subtitle: subtitle is Control ? ControlWidget(control: subtitle) : null,
      trailing: trailing is Control ? ControlWidget(control: trailing) : null,
      children: controls,
    );

    return ConstrainedControl(control: control, child: tile);
  }
}
