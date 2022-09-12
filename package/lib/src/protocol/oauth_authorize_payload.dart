class OAuthAuthorizePayload {
  String authorizationUrl;

  OAuthAuthorizePayload({required this.authorizationUrl});

  factory OAuthAuthorizePayload.fromJson(Map<String, dynamic> json) =>
      OAuthAuthorizePayload(authorizationUrl: json['authorizationUrl']);
}
