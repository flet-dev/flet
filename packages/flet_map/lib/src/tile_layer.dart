import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';

class TileLayerControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const TileLayerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("TileLayerControl build: ${control.id} (${control.hashCode})");

    Widget tile = TileLayer(
      urlTemplate: control.attrString("urlTemplate", "")!,
      fallbackUrl: control.attrString("fallbackUrl", "")!,
      tileSize: control.attrDouble("tileSize", 256)!,
      minNativeZoom: control.attrInt("minNativeZoom", 0)!,
      maxNativeZoom: control.attrInt("maxNativeZoom", 19)!,
      zoomReverse: control.attrBool("zoomReverse", false)!,
      zoomOffset: control.attrDouble("zoomOffset", 0)!,
      // additionalOptions: ,
      // subdomains: ,
      keepBuffer: control.attrInt("keepBuffer", 2)!,
      panBuffer: control.attrInt("panBuffer", 1)!,
      tms: control.attrBool("tms", false)!,
      maxZoom: control.attrDouble("maxZoom", double.infinity)!,
      minZoom: control.attrDouble("minZoom", 0)!,
    );

    return constrainedControl(context, tile, parent, control);
  }
}
