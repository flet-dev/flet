import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:http/http.dart' as http;

import '../actions.dart';
import '../flet_app_services.dart';
import '../flet_server.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/file_picker_result_event.dart';
import '../protocol/file_picker_upload_file.dart';
import '../protocol/file_picker_upload_progress_event.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/desktop.dart';
import '../utils/strings.dart';

class FilePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;

  const FilePickerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild});

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

    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: (context, pageUri) {
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

          resetDialogState() {
            _state = null;
            var fletServices = FletAppServices.of(context);
            List<Map<String, String>> props = [
              {"i": widget.control.id, "state": ""}
            ];
            fletServices.store.dispatch(UpdateControlPropsAction(
                UpdateControlPropsPayload(props: props)));
            fletServices.server.updateControlProps(props: props);
          }

          sendEvent() {
            if (defaultTargetPlatform != TargetPlatform.windows ||
                !isDesktop()) {
              resetDialogState();
            }
            var fletServices = FletAppServices.of(context);
            fletServices.server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "result",
                eventData: json.encode(FilePickerResultEvent(
                    path: _path,
                    files: _files
                        ?.map((f) => FilePickerFile(
                            name: f.name,
                            path: kIsWeb ? null : f.path,
                            size: f.size))
                        .toList())));
          }

          if (_state != state) {
            _path = null;
            _files = null;
            _state = state;

            if (isDesktop() &&
                defaultTargetPlatform == TargetPlatform.windows) {
              resetDialogState();
            }

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
          }

          // upload files
          if (_upload != upload && upload != null && _files != null) {
            _upload = upload;
            uploadFiles(upload, FletAppServices.of(context).server, pageUri!);
          }

          return widget.nextChild ?? const SizedBox.shrink();
        });
  }

  Future uploadFiles(String filesJson, FletServer server, Uri pageUri) async {
    var uj = json.decode(filesJson);
    var uploadFiles = (uj as List).map((u) => FilePickerUploadFile(
        name: u["name"], uploadUrl: u["upload_url"], method: u["method"]));
    for (var uf in uploadFiles) {
      var file = _files!.firstWhereOrNull((f) => f.name == uf.name);
      if (file != null) {
        try {
          await uploadFile(
              file, server, getFullUploadUrl(pageUri, uf.uploadUrl), uf.method);
          _files!.remove(file);
        } catch (e) {
          sendProgress(server, file.name, null, e.toString());
        }
      }
    }
  }

  Future uploadFile(PlatformFile file, FletServer server, String uploadUrl,
      String method) async {
    final fileReadStream = file.readStream;
    if (fileReadStream == null) {
      throw Exception('Cannot read file from null stream');
    }
    debugPrint("Uploading ${file.name}");
    final streamedRequest = http.StreamedRequest(method, Uri.parse(uploadUrl))
      ..headers.addAll({
        //'Cache-Control': 'no-cache',
      });
    streamedRequest.contentLength = file.size;

    // send 0%
    sendProgress(server, file.name, 0, null);

    double lastSent = 0; // send every 10%
    double progress = 0;
    int bytesSent = 0;
    fileReadStream.listen((chunk) async {
      //debugPrint(chunk.length);
      streamedRequest.sink.add(chunk);
      bytesSent += chunk.length;
      progress = bytesSent / file.size;
      if (progress >= lastSent) {
        lastSent += 0.1;
        if (progress != 1.0) {
          sendProgress(server, file.name, progress, null);
        }
      }
    }, onDone: () {
      streamedRequest.sink.close();
    });

    var streamedResponse = await streamedRequest.send();
    var response = await http.Response.fromStream(streamedResponse);
    if (response.statusCode < 200 || response.statusCode > 204) {
      sendProgress(server, file.name, null,
          "Upload endpoint returned code ${response.statusCode}: ${response.body}");
    } else {
      // send 100%
      sendProgress(server, file.name, progress, null);
    }
  }

  void sendProgress(
      FletServer server, String name, double? progress, String? error) {
    server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: "upload",
        eventData: json.encode(FilePickerUploadProgressEvent(
            name: name, progress: progress, error: error)));
  }

  String getFullUploadUrl(Uri pageUri, String uploadUrl) {
    Uri uploadUri = Uri.parse(uploadUrl);
    if (!uploadUri.hasAuthority) {
      return Uri(
              scheme: pageUri.scheme,
              host: pageUri.host,
              port: pageUri.port,
              path: uploadUri.path,
              query: uploadUri.query)
          .toString();
    } else {
      return uploadUrl;
    }
  }
}
