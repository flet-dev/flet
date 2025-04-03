import 'package:flutter/material.dart';

import '../flet_backend.dart';
//import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import '../utils/theme.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'control_widget.dart';
// import 'create_control.dart';
// import 'error.dart';

class ExpansionTileControl extends StatelessWidget {
  //final Control? parent;
  final Control control;
  //final List<Control> children;
  //final bool parentDisabled;
  //final bool? parentAdaptive;
  //final FletControlBackend backend;

  const ExpansionTileControl({
    super.key,
    //this.parent,
    required this.control,
    //required this.children,
    //required this.parentDisabled,
    //required this.parentAdaptive,
    //required this.backend,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionTile build: ${control.id}");

    //var ctrls = children.where((c) => c.name == "controls" && c.visible);
    var controls = control
        .children("controls")
        .map((child) => ControlWidget(control: child, key: ValueKey(child.id)))
        .toList();

    //var leadingCtrls = children.where((c) => c.name == "leading" && c.visible);
    var leading = control.child("leading");

    //var titleCtrls = children.where((c) => c.name == "title" && c.visible);
    var title = control.child("title");

    // var subtitleCtrls =
    //     children.where((c) => c.name == "subtitle" && c.visible);
    var subtitle = control.child("subtitle");

    // var trailingCtrls =
    //     children.where((c) => c.name == "trailing" && c.visible);
    var trailing = control.child("trailing");

    if (title == null) {
      return const ErrorControl(
          "ExpansionTile.title must be provided and visible");
    }

    //bool disabled = control.disabled || parentDisabled;
    bool disabled = control.disabled || control.parent!.disabled;
    bool? adaptive = control.adaptive ?? control.parent?.adaptive;
    //bool onchange = control.getBool("onchange", false)!;
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

    Function(bool)? onChange = !disabled
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
      enabled: !disabled,
      minTileHeight: control.getDouble("min_tile_height"),
      dense: control.getBool("dense"),
      // leading: leadingCtrls.isNotEmpty
      //     ? createControl(control, leadingCtrls.first.id, disabled,
      //         parentAdaptive: adaptive)
      //     : null,
      leading: leading is Control ? ControlWidget(control: leading) : null,
      // title: createControl(control, titleCtrls.first.id, disabled,
      //     parentAdaptive: adaptive),
      title: ControlWidget(control: title),
      // subtitle: subtitleCtrls.isNotEmpty
      //     ? createControl(control, subtitleCtrls.first.id, disabled,
      //         parentAdaptive: adaptive)
      //     : null,
      subtitle: subtitle is Control ? ControlWidget(control: subtitle) : null,
      // trailing: trailingCtrls.isNotEmpty
      //     ? createControl(control, trailingCtrls.first.id, disabled,
      //         parentAdaptive: adaptive)
      //     : null,
      trailing: trailing is Control ? ControlWidget(control: trailing) : null,
      // children: ctrls
      //     .map((c) =>
      //         createControl(control, c.id, disabled, parentAdaptive: adaptive))
      //     .toList(),
      children: controls,
    );

    return ConstrainedControl(control: control, child: tile);
  }
}
