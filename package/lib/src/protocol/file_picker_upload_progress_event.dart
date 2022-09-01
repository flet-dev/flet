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
