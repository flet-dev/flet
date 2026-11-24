import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/icons.dart';
import 'utils/theme.dart';

class ShadContextMenuControl extends StatelessWidget {
  final Control control;

  const ShadContextMenuControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadContextMenu build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadContextMenuRegion(
          // null keeps shadcn_ui's platform default (on for Android/iOS only).
          longPressEnabled: control.getBool("open_on_long_press"),
          tapEnabled: control.getBool("open_on_tap"),
          items: control.buildWidgets("items"),
          child: control.buildWidget("content") ?? const SizedBox.shrink(),
        ),
      ),
    );
  }
}

/// A `flet_shadcn_ui.MenuItem`; must be inside a context menu or menubar menu.
class ShadMenuItemControl extends StatelessWidget {
  final Control control;

  const ShadMenuItemControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    // Submenus open when ShadMouseArea reports hover, and it only does so
    // through a ShadMouseAreaSurface above it, which ShadApp provides at the
    // app root. Menus render in an overlay outside this control, so each item
    // gets its own surface.
    final items = control.buildWidgets("items");
    return ShadMouseAreaSurface(
      child: ShadContextMenuItem.raw(
        variant: control.getBool("inset", false)!
            ? ShadContextMenuItemVariant.inset
            : ShadContextMenuItemVariant.primary,
        enabled: !control.disabled,
        leading: buildShadIconOrWidget(control, "leading"),
        trailing: _buildTrailing(context, items),
        items: items,
        closeOnTap: control.getBool("close_on_click", true)!,
        onPressed: () => control.triggerEvent("click"),
        child: control.buildTextOrWidget("content", required: true)!,
      ),
    );
  }
}

class ShadMenubarControl extends StatelessWidget {
  final Control control;

  const ShadMenubarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadMenubar build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadMenubar(
          selectOnHover: control.getBool("select_on_hover", true)!,
          items: control.buildWidgets("items"),
        ),
      ),
    );
  }
}

extension on ShadMenuItemControl {
  /// The item's trailing text, or a chevron for items that open a submenu.
  Widget? _buildTrailing(BuildContext context, List<Widget> items) {
    final trailing = control.buildTextOrWidget("trailing");
    if (trailing == null && items.isNotEmpty) {
      return const Icon(LucideIcons.chevronRight, size: 16);
    }
    // Trailing text uses the colorless `muted` style; see withMutedColor.
    return withMutedColor(context, trailing);
  }
}

/// A `flet_shadcn_ui.MenubarItem`; must be inside a `ShadMenubarControl`.
class ShadMenubarItemControl extends StatelessWidget {
  final Control control;

  const ShadMenubarItemControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    // See ShadMenuItemControl: hover needs a ShadMouseAreaSurface.
    return ShadMouseAreaSurface(
      child: ShadMenubarItem(
        items: control.buildWidgets("items"),
        child: control.buildTextOrWidget("content", required: true)!,
      ),
    );
  }
}
