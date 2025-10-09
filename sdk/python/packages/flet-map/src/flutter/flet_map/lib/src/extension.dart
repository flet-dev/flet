import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';

import 'circle_layer.dart';
import 'map.dart';
import 'marker_layer.dart';
import 'polygon_layer.dart';
import 'polyline_layer.dart';
import 'rich_attribution.dart';
import 'simple_attribution.dart';
import 'tile_layer.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "Map":
        return MapControl(key: key, control: control);
      case "RichAttribution":
        return RichAttributionControl(key: key, control: control);
      case "SimpleAttribution":
        return SimpleAttributionControl(key: key, control: control);
      case "TileLayer":
        return TileLayerControl(key: key, control: control);
      case "MarkerLayer":
        return MarkerLayerControl(key: key, control: control);
      case "CircleLayer":
        return CircleLayerControl(key: key, control: control);
      case "PolygonLayer":
        return PolygonLayerControl(key: key, control: control);
      case "PolylineLayer":
        return PolylineLayerControl(key: key, control: control);
      default:
        return null;
    }
  }
}
