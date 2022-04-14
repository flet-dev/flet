import 'package:flet_view/utils/colors.dart';

import '../widgets/screen_size.dart';
import 'package:flutter/material.dart';
import 'create_control.dart';
import '../models/control.dart';

class PageControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;

  const PageControl(
      {Key? key, this.parent, required this.control, required this.children})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Page build: ${control.id}");

    bool disabled = control.isDisabled;

    final spacing = control.attrDouble("spacing", 10)!;
    final mainAlignment = parseMainAxisAlignment(control, "verticalAlignment");
    final crossAlignment =
        parseCrossAxisAlignment(control, "horizontalAlignment");

    List<Widget> offstage = [];
    List<Widget> controls = [];
    bool firstControl = true;

    for (var ctrl in children.where((c) => c.isVisible)) {
      // offstage control
      if (ctrl.name == "offstage") {
        offstage.add(createControl(parent, ctrl.id, control.isDisabled));
        continue;
      }

      // spacer between displayed controls
      if (spacing > 0 &&
          !firstControl &&
          mainAlignment != MainAxisAlignment.spaceAround &&
          mainAlignment != MainAxisAlignment.spaceBetween &&
          mainAlignment != MainAxisAlignment.spaceEvenly) {
        controls.add(SizedBox(height: spacing));
      }
      firstControl = false;

      // displayed control
      controls.add(createControl(parent, ctrl.id, disabled));
    }

    // theme
    var theme = parseTheme(control, "theme") ??
        ThemeData(
            colorSchemeSeed: const Color.fromARGB(255, 20, 136, 224),
            brightness: Brightness.light);

    var darkTheme = parseTheme(control, "darkTheme") ??
        ThemeData(
            colorSchemeSeed: const Color.fromARGB(255, 104, 192, 233),
            brightness: Brightness.dark);

    var themeMode = ThemeMode.values.firstWhere(
        (element) => element.name == control.attrString("themeMode"),
        orElse: () => ThemeMode.system);

    debugPrint("Page theme: $themeMode");

    return MaterialApp(
      title: control.attrString("title", "")!,
      theme: theme,
      darkTheme: darkTheme,
      themeMode: themeMode,
      home: Scaffold(
        body: Stack(children: [
          SizedBox.expand(
              child: Container(
            padding: parseEdgeInsets(control, "padding"),
            decoration: BoxDecoration(color: parseColor(control, "bgColor")),
            child: Column(
                mainAxisAlignment: mainAlignment,
                crossAxisAlignment: crossAlignment,
                children: controls),
          )),
          ...offstage,
          const ScreenSize()
        ]),
      ),
    );
  }
}
