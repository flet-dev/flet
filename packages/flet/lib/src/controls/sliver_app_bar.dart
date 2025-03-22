import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

enum SliverAppBarMode {
  medium,
  large,
}

class SliverAppBarControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;
  final FletControlBackend backend;

  const SliverAppBarControl({
    super.key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("SliverAppBar build: ${control.id}");

    bool? adaptive = control.isAdaptive ?? parentAdaptive;
    bool disabled = control.isDisabled || parentDisabled;
    const double kToolbarHeight = 56.0;

    var leadingCtrl =
        children.where((c) => c.name == "leading" && c.isVisible).firstOrNull;
    var leading = leadingCtrl != null
        ? createControl(control, leadingCtrl.id, disabled,
            parentAdaptive: adaptive)
        : null;
    var titleCtrl =
        children.where((c) => c.name == "title" && c.isVisible).firstOrNull;
    var title = titleCtrl != null
        ? createControl(control, titleCtrl.id, disabled,
            parentAdaptive: adaptive)
        : null;
    var flexibleSpaceCtrl = children
        .where((c) => c.name == "flexibleSpace" && c.isVisible)
        .firstOrNull;
    var flexibleSpace = flexibleSpaceCtrl != null
        ? createControl(control, flexibleSpaceCtrl.id, disabled,
            parentAdaptive: adaptive)
        : null;
    var actionCtrls = children.where((c) => c.name == "action" && c.isVisible);
    var actions = createControls(control, actionCtrls, disabled,
        parentAdaptive: adaptive);
    var leadingWidth = control.attrDouble("leadingWidth");
    var automaticallyImplyLeading =
        control.attrBool("automaticallyImplyLeading", true)!;
    var centerTitle = control.attrBool("centerTitle", false)!;
    var toolbarHeight = control.attrDouble("toolbarHeight", kToolbarHeight)!;
    var foregroundColor = control.attrColor("color", context);
    var backgroundColor = control.attrColor("bgcolor", context);
    var elevation = control.attrDouble("elevation");
    var systemOverlayStyle = Theme.of(context)
        .extension<SystemUiOverlayStyleTheme>()
        ?.systemUiOverlayStyle;
    var shadowColor = control.attrColor("shadowColor", context);
    var surfaceTintColor = control.attrColor("surfaceTintColor", context);
    var scrolledUnderElevation = control.attrDouble("elevationOnScroll");
    var forceMaterialTransparency =
        control.attrBool("forceMaterialTransparency", false)!;
    var primary = control.attrBool("primary", true)!;
    var titleSpacing = control.attrDouble("titleSpacing");
    var excludeHeaderSemantics =
        control.attrBool("excludeHeaderSemantics", false)!;
    var clipBehavior = parseClip(control.attrString("clipBehavior"));
    var titleTextStyle =
        parseTextStyle(Theme.of(context), control, "titleTextStyle");
    var shape = parseOutlinedBorder(control, "shape");
    var toolbarTextStyle =
        parseTextStyle(Theme.of(context), control, "toolbarTextStyle");
    var actionsPadding = parseEdgeInsets(control, "actionsPadding");
    var collapsedHeight = control.attrDouble("collapsedHeight");
    var pinned = control.attrBool("pinned", false)!;
    var snap = control.attrBool("snap", false)!;
    var floating = control.attrBool("floating", false)!;
    var stretch = control.attrBool("stretch", false)!;
    var expandedHeight = control.attrDouble("expandedHeight");
    var forceElevated = control.attrBool("forceElevated", false)!;
    var stretchTriggerOffset =
        control.attrDouble("stretchTriggerOffset", 100.0)!;
    Future<void> onStretchTrigger() async {
      backend.triggerControlEvent(control.id, "stretch");
    }

    var type = SliverAppBarMode.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() == control.attrString("type")?.toLowerCase());

    var appBar = type == SliverAppBarMode.large
        ? SliverAppBar.large(
            leading: leading,
            leadingWidth: leadingWidth,
            automaticallyImplyLeading: automaticallyImplyLeading,
            title: title,
            centerTitle: centerTitle,
            toolbarHeight: toolbarHeight,
            foregroundColor: foregroundColor,
            backgroundColor: backgroundColor,
            elevation: elevation,
            actions: actions,
            systemOverlayStyle: systemOverlayStyle,
            shadowColor: shadowColor,
            surfaceTintColor: surfaceTintColor,
            scrolledUnderElevation: scrolledUnderElevation,
            forceMaterialTransparency: forceMaterialTransparency,
            primary: primary,
            titleSpacing: titleSpacing,
            excludeHeaderSemantics: excludeHeaderSemantics,
            clipBehavior: clipBehavior,
            titleTextStyle: titleTextStyle,
            shape: shape,
            toolbarTextStyle: toolbarTextStyle,
            actionsPadding: actionsPadding,
            collapsedHeight: collapsedHeight,
            pinned: pinned,
            snap: snap,
            floating: floating,
            stretch: stretch,
            expandedHeight: expandedHeight,
            forceElevated: forceElevated,
            stretchTriggerOffset: stretchTriggerOffset,
            flexibleSpace: flexibleSpace,
            onStretchTrigger: onStretchTrigger,
          )
        : type == SliverAppBarMode.medium
            ? SliverAppBar.medium(
                leading: leading,
                leadingWidth: leadingWidth,
                automaticallyImplyLeading: automaticallyImplyLeading,
                title: title,
                centerTitle: centerTitle,
                toolbarHeight: toolbarHeight,
                foregroundColor: foregroundColor,
                backgroundColor: backgroundColor,
                elevation: elevation,
                actions: actions,
                systemOverlayStyle: systemOverlayStyle,
                shadowColor: shadowColor,
                surfaceTintColor: surfaceTintColor,
                scrolledUnderElevation: scrolledUnderElevation,
                forceMaterialTransparency: forceMaterialTransparency,
                primary: primary,
                titleSpacing: titleSpacing,
                excludeHeaderSemantics: excludeHeaderSemantics,
                clipBehavior: clipBehavior,
                titleTextStyle: titleTextStyle,
                shape: shape,
                toolbarTextStyle: toolbarTextStyle,
                actionsPadding: actionsPadding,
                collapsedHeight: collapsedHeight,
                pinned: pinned,
                snap: snap,
                floating: floating,
                stretch: stretch,
                expandedHeight: expandedHeight,
                forceElevated: forceElevated,
                stretchTriggerOffset: stretchTriggerOffset,
                flexibleSpace: flexibleSpace,
                onStretchTrigger: onStretchTrigger,
              )
            : SliverAppBar(
                leading: leading,
                leadingWidth: leadingWidth,
                automaticallyImplyLeading: automaticallyImplyLeading,
                title: title,
                centerTitle: centerTitle,
                toolbarHeight: toolbarHeight,
                foregroundColor: foregroundColor,
                backgroundColor: backgroundColor,
                elevation: elevation,
                actions: actions,
                systemOverlayStyle: systemOverlayStyle,
                shadowColor: shadowColor,
                surfaceTintColor: surfaceTintColor,
                scrolledUnderElevation: scrolledUnderElevation,
                forceMaterialTransparency: forceMaterialTransparency,
                primary: primary,
                titleSpacing: titleSpacing,
                excludeHeaderSemantics: excludeHeaderSemantics,
                clipBehavior: clipBehavior,
                titleTextStyle: titleTextStyle,
                shape: shape,
                toolbarTextStyle: toolbarTextStyle,
                actionsPadding: actionsPadding,
                collapsedHeight: collapsedHeight,
                pinned: pinned,
                snap: snap,
                floating: floating,
                stretch: stretch,
                expandedHeight: expandedHeight,
                forceElevated: forceElevated,
                stretchTriggerOffset: stretchTriggerOffset,
                flexibleSpace: flexibleSpace,
                onStretchTrigger: onStretchTrigger,
              );
    return baseControl(context, appBar, parent, control);
  }
}
