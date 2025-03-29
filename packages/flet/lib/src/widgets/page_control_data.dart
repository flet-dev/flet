import 'package:flutter/material.dart';

import '../models/page_design.dart';

class PageControlData extends InheritedWidget {
  final PageDesign widgetsDesign;
  final ThemeMode? themeMode;
  final Brightness? brightness;

  const PageControlData(
      {required this.themeMode,
      required this.brightness,
      required this.widgetsDesign,
      required super.child,
      super.key});

  @override
  bool updateShouldNotify(covariant PageControlData oldWidget) {
    return themeMode != oldWidget.themeMode ||
        brightness != oldWidget.brightness ||
        widgetsDesign != oldWidget.widgetsDesign;
  }

  static PageControlData? of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<PageControlData>();
}
