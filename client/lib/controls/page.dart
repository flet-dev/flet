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

    bool disabled = control.attrBool("disabled", false)!;

    var themeMode = ThemeMode.values.firstWhere(
        (element) => element.name == control.attrString("themeMode"),
        orElse: () => ThemeMode.system);

    debugPrint("Page theme: $themeMode");

    final padding = control.attrDouble("padding", 10)!;
    final spacing = control.attrDouble("spacing", 10)!;
    final mainAlignment = MainAxisAlignment.values.firstWhere(
        (e) =>
            e.name.toLowerCase() == control.attrString("verticalAlignment", ""),
        orElse: () => MainAxisAlignment.start);
    final crossAlignment = CrossAxisAlignment.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("horizontalAlignment", ""),
        orElse: () => CrossAxisAlignment.start);

    List<Widget> offstage = [];
    List<Widget> controls = [];
    bool firstControl = true;

    for (var ctrl in children) {
      // offstage control
      if (ctrl.name == "offstage") {
        offstage.add(createControl(parent, ctrl.id, disabled));
        continue;
      }

      // displayed control
      if (spacing > 0 && !firstControl) {
        controls.add(SizedBox(height: spacing));
      }
      controls.add(createControl(parent, ctrl.id, disabled));
      firstControl = false;
    }

    return MaterialApp(
      title: control.attrString("title", "")!,
      theme: ThemeData(
          colorSchemeSeed: Color.fromARGB(255, 20, 136, 224),
          brightness: Brightness.light,
          useMaterial3: true),
      darkTheme: ThemeData(
          colorSchemeSeed: Color.fromARGB(255, 104, 192, 233),
          brightness: Brightness.dark,
          useMaterial3: true),
      themeMode: themeMode,
      home: Scaffold(
        body: Stack(children: [
          SizedBox.expand(
              child: Container(
            padding: EdgeInsets.all(padding),
            //decoration: BoxDecoration(color: HexColor.fromHex("#AA0088")),
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
