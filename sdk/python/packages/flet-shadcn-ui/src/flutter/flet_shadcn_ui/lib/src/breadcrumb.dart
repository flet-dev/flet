import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/icons.dart';
import 'utils/theme.dart';

class ShadBreadcrumbControl extends StatelessWidget {
  final Control control;

  const ShadBreadcrumbControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadBreadcrumb build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadBreadcrumb(
          separator: buildShadIconOrWidget(control, "separator"),
          spacing: control.getDouble("spacing"),
          children: control.buildWidgets("items"),
        ),
      ),
    );
  }
}

/// A `flet_shadcn_ui.BreadcrumbItem`: a link when it has a click handler,
/// plain text otherwise.
class ShadBreadcrumbItemControl extends StatelessWidget {
  final Control control;

  const ShadBreadcrumbItemControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    final content = control.buildTextOrWidget("content", required: true)!;
    if (!control.hasEventHandler("click")) return content;
    return ShadBreadcrumbLink(
      onPressed: () => control.triggerEvent("click"),
      child: content,
    );
  }
}

/// A `flet_shadcn_ui.BreadcrumbEllipsis`.
class ShadBreadcrumbEllipsisControl extends StatelessWidget {
  const ShadBreadcrumbEllipsisControl({super.key});

  @override
  Widget build(BuildContext context) => const ShadBreadcrumbEllipsis();
}
