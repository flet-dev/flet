import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/intrinsics.dart';
import 'utils/theme.dart';

class ShadResizablePanelGroupControl extends StatelessWidget {
  final Control control;

  const ShadResizablePanelGroupControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadResizablePanelGroup build: ${control.id}");

    // ShadResizablePanelGroup needs typed ShadResizablePanel children, so each
    // panel is built from its control's properties.
    final group = ShadResizablePanelGroup(
      axis: control.getBool("vertical", false)!
          ? Axis.vertical
          : Axis.horizontal,
      showHandle: control.getBool("show_handle", false)!,
      dividerColor: control.getColor("divider_color", context),
      children: [
        for (final panel in control.children("panels"))
          ShadResizablePanel(
            id: panel.id,
            defaultSize: panel.getDouble("default_size", 0)!,
            minSize: panel.getDouble("min_size", 0)!,
            maxSize: panel.getDouble("max_size", 1)!,
            child: panel.buildWidget("content") ?? const SizedBox.shrink(),
          ),
      ],
    );

    // The group fills the space it is given and has no natural size. While a
    // divider is dragged it sets the mouse cursor through a
    // ShadMouseCursorController, which ShadApp normally provides at the root;
    // Flet apps have none, so the group gets its own.
    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        FixedIntrinsics(
          minWidth: 0,
          maxWidth: 0,
          height: 0,
          child: ShadMouseCursorProvider(child: group),
        ),
      ),
    );
  }
}
