class AppBecomeInactivePayload {
  final String message;

  AppBecomeInactivePayload({required this.message});

  factory AppBecomeInactivePayload.fromJson(Map<String, dynamic> json) =>
      AppBecomeInactivePayload(message: json['message'] as String);
}
