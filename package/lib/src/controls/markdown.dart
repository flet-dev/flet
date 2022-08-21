import '../utils/uri.dart';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:markdown/markdown.dart' as md;

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

class MarkdownControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const MarkdownControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Markdown build: ${control.id}");

    final ws = FletAppServices.of(context).ws;

    var value = control.attrString("value", "")!;
    md.ExtensionSet extensionSet = md.ExtensionSet.none;
    switch (control.attrString("extensionSet", "")!.toLowerCase()) {
      case "commonmark":
        extensionSet = md.ExtensionSet.commonMark;
        break;
      case "githubweb":
        extensionSet = md.ExtensionSet.gitHubWeb;
        break;
      case "githubflavored":
        extensionSet = md.ExtensionSet.gitHubFlavored;
        break;
    }

    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: (context, pageUri) {
          Widget markdown = Markdown(
              data: value,
              selectable: control.attrBool("selectable", false)!,
              imageDirectory: getBaseUri(pageUri!).toString(),
              extensionSet: extensionSet,
              onTapLink: (String text, String? href, String title) {
                debugPrint("Markdown link tapped ${control.id} clicked: $href");
                ws.pageEventFromWeb(
                    eventTarget: control.id,
                    eventName: "tap_link",
                    eventData: href?.toString() ?? "");
              },
              padding: parseEdgeInsets(control, "padding") ??
                  const EdgeInsets.all(0));

          return constrainedControl(markdown, parent, control);
        });
  }
}
