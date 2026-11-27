import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentBreadcrumbBarControl extends StatelessWidget {
  final Control control;

  const FluentBreadcrumbBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentBreadcrumbBar build: ${control.id}");

    // Item controls are not rendered: BreadcrumbBar takes BreadcrumbItem
    // objects, whose value is the item control.
    final items = control.children("items").map((item) {
      item.notifyParent = true;
      return BreadcrumbItem<Control>(
        label: item.buildTextOrWidget("content", required: true)!,
        value: item,
      );
    }).toList();

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        BreadcrumbBar<Control>(
          items: items,
          onItemPressed: (item) => item.value.triggerEvent("click"),
        ),
      ),
    );
  }
}
