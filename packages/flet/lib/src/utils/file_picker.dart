import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'enums.dart';

import '../models/control.dart';

class FilePickerResultEvent {
  final String? path;
  final List<FilePickerFile>? files;

  FilePickerResultEvent({required this.path, required this.files});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'path': path,
        'files': files?.map((FilePickerFile f) => f.toMap()).toList()
      };
}

class FilePickerFile {
  final int id;
  final String name;
  final String? path;
  final int size;
  final Uint8List? bytes;

  FilePickerFile(
      {required this.id,
      required this.name,
      required this.path,
      required this.size,
      required this.bytes});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'id': id,
        'name': name,
        'path': path,
        'size': size,
        'bytes': bytes
      };
}

class FilePickerUploadFile {
  final int? id;
  final String? name;
  final String uploadUrl;
  final String method;

  FilePickerUploadFile(
      {required this.id,
      required this.name,
      required this.uploadUrl,
      required this.method});
}

class FilePickerUploadProgressEvent {
  final String name;
  final double? progress;
  final String? error;

  FilePickerUploadProgressEvent(
      {required this.name, required this.progress, required this.error});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'file_name': name,
        'progress': progress,
        'error': error
      };
}

FileType? parseFileType(String? value, [FileType? defaultValue]) {
  return parseEnum(FileType.values, value, defaultValue);
}

extension FilePickerParsers on Control {
  FileType? getFileType(String propertyName, [FileType? defaultValue]) {
    return parseFileType(get(propertyName), defaultValue);
  }
}
