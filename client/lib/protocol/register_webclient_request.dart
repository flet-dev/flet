class RegisterWebClientRequest {
  final String pageName;
  final String? pageHash;
  final String? pageWidth;
  final String? pageHeight;
  final String? windowWidth;
  final String? windowHeight;
  final String? sessionId;

  RegisterWebClientRequest(
      {required this.pageName,
      this.pageHash,
      this.pageWidth,
      this.pageHeight,
      this.windowWidth,
      this.windowHeight,
      this.sessionId});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'pageName': pageName,
        'pageHash': pageHash,
        'pageWidth': pageWidth,
        'pageHeight': pageHeight,
        'windowWidth': windowWidth,
        'windowHeight': windowHeight,
        'sessionId': sessionId
      };
}
