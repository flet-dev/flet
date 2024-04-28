import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class MarkerLayerControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const MarkerLayerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("MarkerLayerControl build: ${control.id} (${control.hashCode})");

    return withControls(control.childIds, (context, markersView) {
      debugPrint("MarkerLayerControlState build: ${control.id}");

      var markers = markersView.controlViews
          .where((c) => c.control.type == "mapmarker" && c.control.isVisible)
          .map((marker) {
        return Marker(
            point: parseLatLng(marker.control, "point")!,
            rotate: marker.control.attrBool("rotate"),
            height: marker.control.attrDouble("height", 30)!,
            width: marker.control.attrDouble("width", 30)!,
            alignment: parseAlignment(marker.control, "alignment"),
            child: createControl(
                control, marker.control.childIds.first, parentDisabled));
      }).toList();

      Widget layer = MarkerLayer(
        markers: markers,
        rotate: control.attrBool("rotate", false)!,
        alignment: parseAlignment(control, "alignment", Alignment.center)!,
      );

      return constrainedControl(context, layer, parent, control);
    });
  }
}
