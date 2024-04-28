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

    List<String> acceptedChildrenTypes = [
      "mapcirclelayer",
      "maptilelayer",
      "mapmarkerlayer",
      "maprichattribution",
      "mapsimpleattribution"
    ];
    MapOptions configuration =
        parseMapOptions(widget.control, "configuration", context);
    var ctrls = widget.children
        .where((c) => c.isVisible && (acceptedChildrenTypes.contains(c.type)))
        .toList();

    Widget map = FlutterMap(
      options: configuration,
      children: ctrls
          .map((c) => createControl(widget.control, c.id, disabled))
          .toList(),
    );

    return constrainedControl(context, map, widget.parent, widget.control);
  }
}
