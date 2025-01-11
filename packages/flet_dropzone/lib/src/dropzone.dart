import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:desktop_drop/desktop_drop.dart';

class DropZoneControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const DropZoneControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<DropZoneControl> createState() => _DropZoneControlState();
}

class _DropZoneControlState extends State<DropZoneControl> with FletStoreMixin {
  
  bool _dragging = false;
  List<dynamic> _allowedFileTypes = [];

  List<dynamic> _droppedFiles = [];


  @override
  void initState() {
    super.initState();
    _allowedFileTypes = widget.control.attrList("allowedFileTypes") ?? [];
  }

  void onDragDone() {
    widget.backend.triggerControlEvent(
      widget.control.id,
      "dropped",
      jsonEncode({
        "files": _droppedFiles
      }),
    );
  }

  void onDragEntered() {
    widget.backend.triggerControlEvent(
      widget.control.id,
      "entered",
      ""
    );
  }

  void onDragExited() {
    widget.backend.triggerControlEvent(
      widget.control.id,
      "exited",
      ""
    );
  }




  @override
  Widget build(BuildContext context) {
    debugPrint("DropZone build: ${widget.control.id} (${widget.control.hashCode})");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);

    Widget child = contentCtrls.isNotEmpty
        ? createControl(widget.control, contentCtrls.first.id, disabled)
        : Container();
    

    return withPageArgs((context, pageArgs) {
          Widget? dropZone;
          
          dropZone = DropTarget(
          onDragEntered: (details) {
            setState(() {
              _dragging = true;
            });
            onDragEntered();

          },
          onDragExited: (details) {
            setState(() {
              _dragging = false;
            });
            onDragExited();

          },
          onDragDone: (details) {
            setState(() {
              _droppedFiles = details.files
                    .map((file) => file.path)
                    .where((filePath) {
                      if (_allowedFileTypes.isEmpty) return true;

                      final extension = filePath.split('.').last.toLowerCase();
                      return _allowedFileTypes.contains(extension);
                    })
                    .toList();
              _dragging = false;
            });
            if (_droppedFiles.isNotEmpty){
              onDragDone();
            }
            

          },
          enable: !disabled,
          child: child,
          );
     
      return constrainedControl(context, dropZone, widget.parent, widget.control);
    });
  }
}
