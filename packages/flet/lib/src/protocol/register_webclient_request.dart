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
  final String? isWeb;
  final String? isDebug;
  final String? platform;
  final String? platformBrightness;
  final String? media;
  final String? sessionId;
  final String? cookie;

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
      this.isWeb,
      this.isDebug,
      this.platform,
      this.platformBrightness,
      this.media,
      this.sessionId,
      this.cookie});

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
        'isWeb': isWeb,
        'isDebug': isDebug,
        'platform': platform,
        'platformBrightness': platformBrightness,
        'media': media,
        'sessionId': sessionId,
        'cookie': cookie
      };
}
