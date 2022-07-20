class RegisterWebClientRequest {
  final String pageName;
  final String? pageRoute;
  final String? pageWidth;
  final String? pageHeight;
  final String? windowWidth;
  final String? windowHeight;
  final String? windowTop;
  final String? windowLeft;
  final String? isPWA;
  final String? sessionId;

  RegisterWebClientRequest(
      {required this.pageName,
      this.pageRoute,
      this.pageWidth,
      this.pageHeight,
      this.windowWidth,
      this.windowHeight,
      this.windowTop,
      this.windowLeft,
      this.isPWA,
      this.sessionId});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'pageName': pageName,
        'pageRoute': pageRoute,
        'pageWidth': pageWidth,
        'pageHeight': pageHeight,
        'windowWidth': windowWidth,
        'windowHeight': windowHeight,
        'windowTop': windowTop,
        'windowLeft': windowLeft,
        'isPWA': isPWA,
        'sessionId': sessionId
      };
}
