import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map_animations/flutter_map_animations.dart';

import 'utils/map.dart';

class MarkerLayerControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const MarkerLayerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("MarkerLayerControl build: ${control.id}");

    return withControls(control.childIds, (context, markersView) {
      debugPrint("MarkerLayerControlState build: ${control.id}");

      var markers = markersView.controlViews
          .where((c) => c.control.type == "map_marker" && c.control.isVisible)
          .map((marker) {
        return AnimatedMarker(
            point: parseLatLng(marker.control, "coordinates")!,
            rotate: marker.control.attrBool("rotate"),
            height: marker.control.attrDouble("height", 30)!,
            width: marker.control.attrDouble("width", 30)!,
            alignment: parseAlignment(marker.control, "alignment"),
            builder: (BuildContext context, Animation<double> animation) {
              return createControl(
                  control, marker.control.childIds.first, parentDisabled);
            });
      }).toList();

      return AnimatedMarkerLayer(
        markers: markers,
        rotate: control.attrBool("rotate", false)!,
        alignment: parseAlignment(control, "alignment", Alignment.center)!,
      );
    });
  }
}
