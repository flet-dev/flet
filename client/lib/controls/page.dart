import 'package:flet_view/models/control_type.dart';
import 'package:flet_view/utils/desktop.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_children_view_model.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/theme.dart';
import '../widgets/screen_size.dart';
import 'create_control.dart';
import 'scrollable_control.dart';

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
    final mainAlignment = parseMainAxisAlignment(
        control, "verticalAlignment", MainAxisAlignment.start);
    final crossAlignment = parseCrossAxisAlignment(
        control, "horizontalAlignment", CrossAxisAlignment.start);

    ScrollMode scrollMode = ScrollMode.values.firstWhere(
        (m) =>
            m.name.toLowerCase() ==
            control.attrString("scroll", "")!.toLowerCase(),
        orElse: () => ScrollMode.none);

    debugPrint("scrollMode: $scrollMode");

    Control? offstage;
    List<Widget> controls = [];
    bool firstControl = true;

    for (var ctrl in children.where((c) => c.isVisible)) {
      // offstage control
      if (ctrl.type == ControlType.offstage) {
        offstage = ctrl;
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
            colorSchemeSeed: const Color.fromARGB(255, 0, 152, 218),
            brightness: Brightness.light,
            useMaterial3: true,
            visualDensity: VisualDensity.adaptivePlatformDensity);

    var darkTheme = parseTheme(control, "darkTheme") ??
        ThemeData(
            colorSchemeSeed: const Color.fromARGB(255, 104, 192, 233),
            brightness: Brightness.dark,
            useMaterial3: true,
            visualDensity: VisualDensity.adaptivePlatformDensity);

    var themeMode = ThemeMode.values.firstWhere(
        (t) =>
            t.name.toLowerCase() ==
            control.attrString("themeMode", "")!.toLowerCase(),
        orElse: () => ThemeMode.system);

    debugPrint("Page theme: $themeMode");

    String title = control.attrString("title", "")!;
    setWindowTitle(title);

    return StoreConnector<AppState, ControlChildrenViewModel?>(
        distinct: true,
        converter: (store) => offstage != null
            ? ControlChildrenViewModel.fromStore(store, offstage.id,
                dispatch: store.dispatch)
            : null,
        builder: (context, offstageView) {
          debugPrint("Offstage StoreConnector build");

          // offstage
          List<Widget> offstageWidgets = offstageView != null
              ? offstageView.children
                  .where((c) => c.isVisible)
                  .map((c) => createControl(offstage, c.id, disabled))
                  .toList()
              : [];

          var column = Column(
              mainAxisAlignment: mainAlignment,
              crossAxisAlignment: crossAlignment,
              children: controls);

          return MaterialApp(
            title: title,
            theme: theme,
            darkTheme: darkTheme,
            themeMode: themeMode,
            home: Scaffold(
              body: Stack(children: [
                SizedBox.expand(
                    child: Container(
                        padding: parseEdgeInsets(control, "padding") ??
                            const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                            color: HexColor.fromString(
                                context, control.attrString("bgcolor", "")!)),
                        child: scrollMode != ScrollMode.none
                            ? ScrollableControl(
                                child: column,
                                scrollDirection: Axis.vertical,
                                scrollMode: scrollMode,
                              )
                            : column)),
                ...offstageWidgets,
                const ScreenSize()
              ]),
            ),
          );
        });
  }
}
