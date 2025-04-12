import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flet/src/utils/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../models/control.dart';
import '../utils/numbers.dart';
import '../widgets/flet_store_mixin.dart';

class FilePickerControl extends StatefulWidget {
  final Control control;

  const FilePickerControl({super.key, required this.control});

  @override
  State<FilePickerControl> createState() => _FilePickerControlState();
}

class _FilePickerControlState extends State<FilePickerControl>
    with FletStoreMixin {
  String? _upload;
  String? _path;
  List<PlatformFile>? _files;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("FilePicker.$name($args)");
    var dialogTitle = args["dialog_title"];
    var fileType = parseFileType(args["file_type"], FileType.any)!;
    var initialDirectory = args["initial_directory"];
    var allowedExtensions = (args["allowed_extensions"] as List?)
        ?.map((e) => e.toString())
        .toList();

    if (allowedExtensions != null && allowedExtensions.isNotEmpty) {
      fileType = FileType.custom;
    }
    switch (name) {
      case "upload":
        var upload = args["upload"];
        if (_upload != upload && upload != null && _files != null) {
          _upload = upload;
          debugPrint("Upload: $_upload");
          // TODO
        }
      case "pick_files":
        FilePicker.platform
            .pickFiles(
                dialogTitle: dialogTitle,
                initialDirectory: initialDirectory,
                lockParentWindow: true,
                type: fileType,
                allowedExtensions: allowedExtensions,
                allowMultiple: args["allow_multiple"],
                withData: false,
                withReadStream: true)
            .then((FilePickerResult? result) {
          _files = result?.files;
          sendEvent();
        });
      case "save_file":
        if (!kIsWeb) {
          FilePicker.platform
              .saveFile(
            dialogTitle: dialogTitle,
            fileName: args["file_name"],
            initialDirectory: initialDirectory,
            lockParentWindow: true,
            type: fileType,
            allowedExtensions: allowedExtensions,
            // bytes:
          )
              .then((result) {
            _path = result;
            sendEvent();
          });
        }
      case "get_directory_path":
        if (!kIsWeb) {
          FilePicker.platform
              .getDirectoryPath(
            dialogTitle: dialogTitle,
            initialDirectory: initialDirectory,
            lockParentWindow: true,
          )
              .then((result) {
            _path = result;
            sendEvent();
          });
        }
      default:
        throw Exception("Unknown FilePicker method: $name");
    }
  }

  void sendEvent() {
    var result = FilePickerResultEvent(
            path: _path,
            files: _files?.asMap().entries.map((entry) {
              PlatformFile f = entry.value;
              return FilePickerFile(
                  id: entry.key, // use entry's index as id
                  name: f.name,
                  path: kIsWeb ? null : f.path,
                  size: f.size);
            }).toList())
        .toMap();

    widget.control.triggerEvent("result", result);
    // widget.control.updateProperties({"_result": result});
  }

  Future uploadFiles(String filesJson, Uri pageUri) async {
    var uj = json.decode(filesJson);
    var uploadFiles = (uj as List).map((u) => FilePickerUploadFile(
        id: parseInt(u["id"], -1)!, // -1 = invalid
        name: u["name"],
        uploadUrl: u["upload_url"],
        method: u["method"]));

    for (var uf in uploadFiles) {
      var file = ((uf.id >= 0 && uf.id < _files!.length)
              ? _files![uf.id]
              : null) // by id
          ??
          _files!.firstWhereOrNull((f) => f.name == uf.name); // by name

      if (file != null) {
        try {
          await uploadFile(
              file, getFullUploadUrl(pageUri, uf.uploadUrl), uf.method);
          _files!.remove(file); // Remove the uploaded file
        } catch (e) {
          sendProgress(file.name, null, e.toString());
        }
      } else {
        debugPrint(
            "FilePicker Error: File '${uf.name}' (id: ${uf.id}) not found.");
      }
    }
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

  void sendProgress(String name, double? progress, String? error) {
    widget.control.triggerEvent(
        "upload",
        FilePickerUploadProgressEvent(
                name: name, progress: progress, error: error)
            .toMap());
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

  @override
  Widget build(BuildContext context) {
    debugPrint("FilePicker build: ${widget.control.id}");
    return const SizedBox.shrink();
  }
}
