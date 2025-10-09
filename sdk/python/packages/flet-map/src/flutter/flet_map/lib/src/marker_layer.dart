import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map_animations/flutter_map_animations.dart';

import 'utils/map.dart';

class MarkerLayerControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const MarkerLayerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("MarkerLayerControl build: ${control.id}");
    var markers = control
        .children("markers")
        .where((c) => c.type == "Marker")
        .map((marker) {
      return AnimatedMarker(
          point: parseLatLng(marker.get("coordinates"))!,
          rotate: marker.getBool("rotate"),
          height: marker.getDouble("height", 30.0)!,
          width: marker.getDouble("width", 30.0)!,
          alignment: marker.getAlignment("alignment"),
          builder: (BuildContext context, Animation<double> animation) {
            return marker.buildWidget("content") ??
                const ErrorControl("content must be provided and visible");
          });
    }).toList();

    return AnimatedMarkerLayer(
      markers: markers,
      rotate: control.getBool("rotate", false)!,
      alignment: control.getAlignment("alignment", Alignment.center)!,
    );
  }
}
