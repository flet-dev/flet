import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/theme.dart';
import '../widgets/screen_size.dart';
import 'create_control.dart';

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

    debugPrint(Theme.of(context).colorScheme.primary.toString());

    bool disabled = control.isDisabled;

    final spacing = control.attrDouble("spacing", 10)!;
    final mainAlignment = parseMainAxisAlignment(
        control, "verticalAlignment", MainAxisAlignment.start);
    final crossAlignment = parseCrossAxisAlignment(
        control, "horizontalAlignment", CrossAxisAlignment.start);

    List<Widget> offstage = [];
    List<Widget> controls = [];
    bool firstControl = true;

    for (var ctrl in children.where((c) => c.isVisible)) {
      // offstage control
      if (ctrl.name == "offstage") {
        offstage.add(createControl(control, ctrl.id, control.isDisabled));
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
      controls.add(createControl(control, ctrl.id, disabled));
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
        (t) =>
            t.name.toLowerCase() ==
            control.attrString("themeMode", "")!.toLowerCase(),
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
            padding:
                parseEdgeInsets(control, "padding") ?? const EdgeInsets.all(10),
            decoration: BoxDecoration(
                color: HexColor.fromString(
                    context, control.attrString("bgcolor", "")!)),
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
