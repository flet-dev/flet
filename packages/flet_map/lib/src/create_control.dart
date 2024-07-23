import 'package:flet/flet.dart';

import 'circle_layer.dart';
import 'map.dart';
import 'marker_layer.dart';
import 'polygon_layer.dart';
import 'polyline_layer.dart';
import 'rich_attribution.dart';
import 'simple_attribution.dart';
import 'tile_layer.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "map":
      return MapControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        parentDisabled: args.parentDisabled,
        backend: args.backend,
      );
    case "map_rich_attribution":
      return RichAttributionControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        backend: args.backend,
      );
    case "map_simple_attribution":
      return SimpleAttributionControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        backend: args.backend,
      );
    case "map_tile_layer":
      return TileLayerControl(
        parent: args.parent,
        control: args.control,
        backend: args.backend,
      );
    case "map_marker_layer":
      return MarkerLayerControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        parentDisabled: args.parentDisabled,
      );
    case "map_circle_layer":
      return CircleLayerControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
      );
    case "map_polygon_layer":
      return PolygonLayerControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
      );
    case "map_polyline_layer":
      return PolylineLayerControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
      );
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
