import 'dart:convert';

import 'package:file_picker/file_picker.dart';
import 'package:flet/src/protocol/file_picker_close_event.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/strings.dart';

class FilePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const FilePickerControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<FilePickerControl> createState() => _FilePickerControlState();
}

class _FilePickerControlState extends State<FilePickerControl> {
  String? _state;
  String? _upload;
  String? _path;
  List<PlatformFile>? _files;

  @override
  Widget build(BuildContext context) {
    debugPrint("FilePicker build: ${widget.control.id}");

    var state = widget.control.attrString("state");
    var upload = widget.control.attrString("upload");
    var dialogTitle = widget.control.attrString("dialogTitle");
    var fileName = widget.control.attrString("fileName");
    var initialDirectory = widget.control.attrString("initialDirectory");
    var allowMultiple = widget.control.attrBool("allowMultiple", false)!;
    var allowedExtensions =
        parseStringList(widget.control, "allowedExtensions");
    FileType fileType = FileType.values.firstWhere(
        (m) =>
            m.name.toLowerCase() ==
            widget.control.attrString("fileType", "")!.toLowerCase(),
        orElse: () => FileType.any);
    if (allowedExtensions != null && allowedExtensions.isNotEmpty) {
      fileType = FileType.custom;
    }

    debugPrint("FilePicker _state: $_state, state: $state");

    sendEvent() {
      _state = null;
      var fletServices = FletAppServices.of(context);
      List<Map<String, String>> props = [
        {"i": widget.control.id, "state": ""}
      ];
      fletServices.store.dispatch(
          UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
      fletServices.ws.updateControlProps(props: props);
      fletServices.ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: "close",
          eventData: json.encode(FilePickerCloseEvent(
              path: _path,
              files: _files
                  ?.map((f) => FilePickerFile(
                      name: f.name, path: kIsWeb ? null : f.path, size: f.size))
                  .toList())));
    }

    if (_state != state) {
      _path = null;
      _files = null;

      // pickFiles
      if (state?.toLowerCase() == "pickfiles") {
        FilePicker.platform
            .pickFiles(
                dialogTitle: dialogTitle,
                initialDirectory: initialDirectory,
                lockParentWindow: true,
                type: fileType,
                allowedExtensions: allowedExtensions,
                allowMultiple: allowMultiple,
                withData: false,
                withReadStream: true)
            .then((result) {
          debugPrint("pickFiles() completed");
          _files = result?.files;
          sendEvent();
        });
      }
      // saveFile
      else if (state?.toLowerCase() == "savefile" && !kIsWeb) {
        FilePicker.platform
            .saveFile(
          dialogTitle: dialogTitle,
          fileName: fileName,
          initialDirectory: initialDirectory,
          lockParentWindow: true,
          type: fileType,
          allowedExtensions: allowedExtensions,
        )
            .then((result) {
          debugPrint("saveFile() completed");
          _path = result;
          sendEvent();
        });
      }
      // saveFile
      else if (state?.toLowerCase() == "getdirectorypath" && !kIsWeb) {
        FilePicker.platform
            .getDirectoryPath(
          dialogTitle: dialogTitle,
          initialDirectory: initialDirectory,
          lockParentWindow: true,
        )
            .then((result) {
          debugPrint("getDirectoryPath() completed");
          _path = result;
          sendEvent();
        });
      }
      _state = state;
    }
    if (_upload != upload) {
      debugPrint("Selected files: ${_files?.length}");
      _upload = upload;
    }

    return const SizedBox.shrink();
  }
}
