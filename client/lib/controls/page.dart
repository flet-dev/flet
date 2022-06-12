import 'package:flet_view/utils/user_fonts.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_type.dart';
import '../models/controls_view_model.dart';
import '../models/page_media_view_model.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/desktop.dart';
import '../utils/edge_insets.dart';
import '../utils/theme.dart';
import '../utils/uri.dart';
import '../widgets/page_media.dart';
import 'app_bar.dart';
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

    final autoScroll = control.attrBool("autoScroll", false)!;

    Control? offstage;
    Control? appBar;
    List<Widget> controls = [];
    bool firstControl = true;

    for (var ctrl in children.where((c) => c.isVisible)) {
      // offstage control
      if (ctrl.type == ControlType.offstage) {
        offstage = ctrl;
        continue;
      } else if (ctrl.type == ControlType.appBar) {
        appBar = ctrl;
        continue;
      }
      // spacer between displayed controls
      else if (spacing > 0 &&
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
    var lightTheme = parseTheme(control, "theme") ??
        ThemeData(
            colorSchemeSeed: Colors.blue,
            brightness: Brightness.light,
            useMaterial3: true,
            // fontFamily: kIsWeb && window.navigator.userAgent.contains('OS 15_')
            //     ? '-apple-system'
            //     : null,
            visualDensity: VisualDensity.adaptivePlatformDensity);

    var darkTheme = parseTheme(control, "darkTheme") ??
        ThemeData(
            colorSchemeSeed: Colors.blue,
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

    List<String> childIds = [];
    if (offstage != null) {
      childIds.add(offstage.id);
    }
    if (appBar != null) {
      childIds.add(appBar.id);
    }

    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: (context, pageUri) {
          // load custom fonts
          parseFonts(control, "fonts").forEach((fontFamily, fontUrl) {
            var fontUri = Uri.parse(fontUrl);
            if (!fontUri.hasAuthority) {
              fontUri = getAssetUri(pageUri!, fontUrl);
            }
            debugPrint("fontUri: $fontUri");
            UserFonts.loadFont(fontFamily, fontUri);
          });

          return StoreConnector<AppState, PageMediaViewModel>(
              distinct: true,
              converter: (store) => PageMediaViewModel.fromStore(store),
              builder: (context, media) {
                var theme = themeMode == ThemeMode.light ||
                        (themeMode == ThemeMode.system &&
                            media.displayBrightness == Brightness.light)
                    ? lightTheme
                    : darkTheme;

                return StoreConnector<AppState, ControlsViewModel>(
                    distinct: true,
                    converter: (store) =>
                        ControlsViewModel.fromStore(store, childIds),
                    builder: (context, childrenViews) {
                      debugPrint("Offstage StoreConnector build");

                      // offstage
                      List<Widget> offstageWidgets = offstage != null
                          ? childrenViews.controlViews.first.children
                              .where((c) =>
                                  c.isVisible &&
                                  c.type != ControlType.floatingActionButton)
                              .map((c) =>
                                  createControl(offstage, c.id, disabled))
                              .toList()
                          : [];

                      List<Control> fab = offstage != null
                          ? childrenViews.controlViews.first.children
                              .where((c) =>
                                  c.isVisible &&
                                  c.type == ControlType.floatingActionButton)
                              .toList()
                          : [];

                      var appBarView = appBar != null
                          ? childrenViews.controlViews.last
                          : null;

                      var column = Column(
                          mainAxisAlignment: mainAlignment,
                          crossAxisAlignment: crossAlignment,
                          children: controls);

                      return MaterialApp(
                        title: title,
                        theme: lightTheme,
                        darkTheme: darkTheme,
                        themeMode: themeMode,
                        home: Scaffold(
                          appBar: appBarView != null
                              ? AppBarControl(
                                  parent: control,
                                  control: appBarView.control,
                                  children: appBarView.children,
                                  parentDisabled: disabled,
                                  height: appBarView.control.attrDouble(
                                      "toolbarHeight", kToolbarHeight)!,
                                  theme: theme)
                              : null,
                          body: Stack(children: [
                            SizedBox.expand(
                                child: Container(
                                    padding:
                                        parseEdgeInsets(control, "padding") ??
                                            const EdgeInsets.all(10),
                                    decoration: BoxDecoration(
                                        color: HexColor.fromString(
                                            theme,
                                            control.attrString(
                                                "bgcolor", "")!)),
                                    child: scrollMode != ScrollMode.none
                                        ? ScrollableControl(
                                            child: column,
                                            scrollDirection: Axis.vertical,
                                            scrollMode: scrollMode,
                                            autoScroll: autoScroll,
                                          )
                                        : column)),
                            ...offstageWidgets,
                            const PageMedia()
                          ]),
                          floatingActionButton: fab.isNotEmpty
                              ? createControl(offstage, fab.first.id, disabled)
                              : null,
                        ),
                      );
                    });
              });
        });
  }
}
