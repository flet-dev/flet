import 'package:flet/flet.dart';

import 'circle_layer.dart';
import 'map.dart';
import 'marker_layer.dart';
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
    case "maprichattribution":
      return RichAttributionControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        backend: args.backend,
      );
    case "mapsimpleattribution":
      return SimpleAttributionControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        backend: args.backend,
      );
    case "maptilelayer":
      return TileLayerControl(
        parent: args.parent,
        control: args.control,
        backend: args.backend,
      );
    case "mapmarkerlayer":
      return MarkerLayerControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        parentDisabled: args.parentDisabled,
      );
    case "mapcirclelayer":
      return CircleLayerControl(
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
