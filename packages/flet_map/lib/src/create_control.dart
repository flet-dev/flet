import 'package:flet/flet.dart';

import 'map.dart';
import 'rich_attribution.dart';
import 'text_source_attribution.dart';
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
    case "richattribution":
      return RichAttributionControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        parentDisabled: args.parentDisabled,
        backend: args.backend,
      );
    case "textsourceattribution":
      return TextSourceAttributionControl(
          parent: args.parent,
          control: args.control,
          nextChild: args.nextChild,
          backend: args.backend);
    case "maptilelayer":
      return TileLayerControl(
        parent: args.parent,
        control: args.control,
        parentDisabled: args.parentDisabled,
        backend: args.backend,
      );
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
