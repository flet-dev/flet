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
            padding: EdgeInsets.all(10),
            //decoration: BoxDecoration(color: HexColor.fromHex("#AA0088")),
            child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: control.childIds
                    .map((childId) => createControl(control, childId, disabled))
                    .toList()),
            // child: ListView(
            //     children: control.childIds
            //         .map((childId) => createControl(control, childId, disabled))
            //         .toList()),
          )),
          const ScreenSize()
        ]),
      ),
    );
  }
}
