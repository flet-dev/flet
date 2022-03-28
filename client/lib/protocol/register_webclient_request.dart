class RegisterWebClientRequest {
  final String pageName;
  final String? pageHash;
  final String? winWidth;
  final String? winHeight;
  final String? sessionId;

  RegisterWebClientRequest(
      {required this.pageName,
      this.pageHash,
      this.winWidth,
      this.winHeight,
      this.sessionId});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'pageName': pageName,
        'pageHash': pageHash,
        'winWidth': winWidth,
        'winHeight': winHeight,
        'sessionId': sessionId
      };
}
