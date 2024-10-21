import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/desktop.dart';
import '../utils/strings.dart';
import 'flet_store_mixin.dart';

class FilePickerResultEvent {
  final String? path;
  final List<FilePickerFile>? files;

  FilePickerResultEvent({required this.path, required this.files});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'path': path,
        'files': files?.map((f) => f.toJson()).toList()
      };
}

class FilePickerFile {
  final String name;
  final String? path;
  final int size;

  FilePickerFile({required this.name, required this.path, required this.size});

  Map<String, dynamic> toJson() =>
      <String, dynamic>{'name': name, 'path': path, 'size': size};
}

class FilePickerUploadFile {
  final String name;
  final String uploadUrl;
  final String method;

  FilePickerUploadFile(
      {required this.name, required this.uploadUrl, required this.method});
}

class FilePickerUploadProgressEvent {
  final String name;
  final double? progress;
  final String? error;

  FilePickerUploadProgressEvent(
      {required this.name, required this.progress, required this.error});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'file_name': name,
        'progress': progress,
        'error': error
      };
}

class FilePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const FilePickerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  State<FilePickerControl> createState() => _FilePickerControlState();
}

List<PlatformFile> files = [];

class _FilePickerControlState extends State<FilePickerControl>
    with FletStoreMixin {
  String? _state;
  String? _path;

  @override
  Widget build(BuildContext context) {
    debugPrint("FilePicker build: ${widget.control.id}");

    return withPageArgs((context, pageArgs) {
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
      debugPrint("FilePicker _path: $_path");
      debugPrint("FilePicker _files: $files");

      sendEvent() {
        if (defaultTargetPlatform != TargetPlatform.windows || !isDesktop()) {
          resetDialogState();
        }
        widget.backend.triggerControlEvent(
            widget.control.id,
            "result",
            json.encode(FilePickerResultEvent(
                path: _path,
                files: files
                    .map((f) => FilePickerFile(
                        name: f.name,
                        path: kIsWeb ? null : f.path,
                        size: f.size))
                    .toList())));
      }

      if (_state != state) {
        _path = null;
        // _files = null;
        _state = state;
        if (isDesktop() && defaultTargetPlatform == TargetPlatform.windows) {
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

              if (result != null) {
                files = result.files;
              }
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
        } else if (state?.toLowerCase() == "uploadfiles" &&
            upload != null &&
            files.isNotEmpty) {
          uploadFiles(upload, files, pageArgs.pageUri!);
        }
      }
      return widget.nextChild ?? const SizedBox.shrink();
    });
  }

  Future uploadFiles(
      String filesJson, List<PlatformFile> files, Uri pageUri) async {
    var uj = json.decode(filesJson);
    var uploadFiles = (uj as List).map((u) => FilePickerUploadFile(
        name: u["name"], uploadUrl: u["upload_url"], method: u["method"]));
    List<String> uploadedFiles = [];
    for (var uf in uploadFiles) {
      var file = files.firstWhereOrNull((f) => f.name == uf.name);
      if (file != null) {
        try {
          await uploadFile(
              file, getFullUploadUrl(pageUri, uf.uploadUrl), uf.method);
          uploadedFiles.add(file.name);
        } catch (e) {
          sendProgress(file.name, null, e.toString());
        }
      }
    }
    sendUploadFinishEvent(uploadedFiles);
    resetDialogState();
  }

  Future uploadFile(PlatformFile file, String uploadUrl, String method) async {
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
    sendProgress(file.name, 0, null);

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
          sendProgress(file.name, progress, null);
        }
      }
    }, onDone: () {
      streamedRequest.sink.close();
    });

    var streamedResponse = await streamedRequest.send();
    var response = await http.Response.fromStream(streamedResponse);
    if (response.statusCode < 200 || response.statusCode > 204) {
      sendProgress(file.name, null,
          "Upload endpoint returned code ${response.statusCode}: ${response.body}");
    } else {
      // send 100%
      sendProgress(file.name, progress, null);
    }
  }

  resetDialogState() {
    _state = null;
    widget.backend.updateControlState(widget.control.id, {"state": ""});
  }

  void sendProgress(String name, double? progress, String? error) {
    widget.backend.triggerControlEvent(
        widget.control.id,
        "upload",
        json.encode(FilePickerUploadProgressEvent(
            name: name, progress: progress, error: error)));
  }

  void sendUploadFinishEvent(List<String> files) {
    widget.backend.triggerControlEvent(
        widget.control.id, "upload_finished", json.encode(files));
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
