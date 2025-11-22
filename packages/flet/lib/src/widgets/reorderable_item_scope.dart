import 'package:flutter/widgets.dart';

class ReorderableItemScope extends InheritedWidget {
  const ReorderableItemScope({
    super.key,
    required this.index,
    required super.child,
  });

  final int index;

  static ReorderableItemScope? of(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<ReorderableItemScope>();
  }

  @override
  bool updateShouldNotify(ReorderableItemScope oldWidget) =>
      oldWidget.index != index;
}
