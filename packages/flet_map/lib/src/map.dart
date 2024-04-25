import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class MapControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const MapControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<MapControl> createState() => _MapControlState();
}

class _MapControlState extends State<MapControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("Map build: ${widget.control.id} (${widget.control.hashCode})");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    MapOptions options = parseMapOptions(widget.control, "options", context);
    var ctrls = widget.children
        .where((c) =>
            c.isVisible &&
            (c.type == "richattribution" || c.type == "maptilelayer"))
        .toList();
    debugPrint("Map build: ${ctrls.length} children");
    Widget map = FlutterMap(
      options: options,
      children: ctrls
          .map((c) => createControl(widget.control, c.id, disabled))
          .toList(),
    );

    return constrainedControl(context, map, widget.parent, widget.control);
  }
}

/*
FlutterMap(
    options: MapOptions(
      initialCenter: LatLng(51.509364, -0.128928),
      initialZoom: 9.2,
    ),
    children: [
      TileLayer(
        urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        userAgentPackageName: 'com.example.app',
      ),
      RichAttributionWidget(
        attributions: [
          TextSourceAttribution(
            'OpenStreetMap contributors',
            onTap: () => launchUrl(Uri.parse('https://openstreetmap.org/copyright')),
          ),
        ],
      ),
    ],
  );*/
