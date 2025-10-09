import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/attribution_alignment.dart';

class RichAttributionControl extends StatefulWidget {
  final Control control;

  const RichAttributionControl({super.key, required this.control});

  @override
  State<RichAttributionControl> createState() => _RichAttributionControlState();
}

class _RichAttributionControlState extends State<RichAttributionControl>
    with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("RichAttributionControl build: ${widget.control.id}");

    var attributions = widget.control
        .children("attributions")
        .map((Control c) {
          if (c.type == "TextSourceAttribution") {
            return TextSourceAttribution(
              c.getString("text", "Placeholder Text")!,
              textStyle: c.getTextStyle("text_style", Theme.of(context)),
              onTap: () => c.triggerEvent("click"),
              prependCopyright: c.getBool("prepend_copyright", true)!,
            );
          } else if (c.type == "ImageSourceAttribution") {
            var image = c.buildWidget("image");
            if (image == null) return null;
            return LogoSourceAttribution(
              image,
              height: c.getDouble("height", 24.0)!,
              tooltip: c.getString("tooltip"),
              onTap: () => c.triggerEvent("click"),
            );
          }
        })
        .nonNulls
        .toList();

    return RichAttributionWidget(
        attributions: attributions,
        permanentHeight: widget.control.getDouble("permanent_height", 24.0)!,
        popupBackgroundColor: widget.control.getColor(
            "popup_bgcolor", context, Theme.of(context).colorScheme.surface),
        showFlutterMapAttribution:
            widget.control.getBool("show_flutter_map_attribution", true)!,
        alignment: parseAttributionAlignment(
            widget.control.getString("alignment"),
            AttributionAlignment.bottomRight)!,
        popupBorderRadius:
            widget.control.getBorderRadius("popup_border_radius"),
        popupInitialDisplayDuration: widget.control
            .getDuration("popup_initial_display_duration", Duration.zero)!);
  }
}
