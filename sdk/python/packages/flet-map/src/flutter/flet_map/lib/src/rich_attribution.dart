import 'package:flet/flet.dart';
import 'package:material_ui/material_ui.dart';
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
          c.notifyParent = true;
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

    var permanentHeight = widget.control.getDouble("permanent_height", 24.0)!;

    return BaseControl(
      control: widget.control,
      child: RichAttributionWidget(
          attributions: attributions,
          permanentHeight: permanentHeight,
          openButton: (context, open) => _openButton(open, permanentHeight),
          closeButton: (context, close) =>
              _closeButton(context, close, permanentHeight),
          popupBackgroundColor: widget.control.getColor(
              "popup_bgcolor", context, Theme.of(context).colorScheme.surface),
          showFlutterMapAttribution:
              widget.control.getBool("show_flutter_map_attribution", true)!,
          alignment: widget.control.getAttributionAlignment(
              "alignment", AttributionAlignment.bottomRight)!,
          popupBorderRadius:
              widget.control.getBorderRadius("popup_border_radius"),
          popupInitialDisplayDuration: widget.control
              .getDuration("popup_initial_display_duration", Duration.zero)!),
    );
  }

  /// The button that opens the attributions popup.
  ///
  /// Same as `RichAttributionWidget`'s default, which flutter_map builds from
  /// the Flutter SDK's Material library rather than `material_ui`.
  Widget _openButton(VoidCallback open, double size) {
    return IconButton(
      onPressed: open,
      tooltip: 'Attributions',
      icon: Icon(Icons.info_outlined, color: Colors.black, size: size),
    );
  }

  /// The button that closes the attributions popup.
  ///
  /// Same as `RichAttributionWidget`'s default, but colored from the app's
  /// theme: the default reads the SDK's Material theme, which apps rendered
  /// with `material_ui` don't provide, so it fell back to a dark icon on dark
  /// popups.
  Widget _closeButton(BuildContext context, VoidCallback close, double size) {
    return IconButton(
      onPressed: close,
      icon: Icon(Icons.cancel_outlined,
          color: Theme.of(context).textTheme.titleSmall?.color ?? Colors.black,
          size: size),
    );
  }
}
