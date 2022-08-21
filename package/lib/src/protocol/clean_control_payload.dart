class CleanControlPayload {
  final List<String> ids;

  CleanControlPayload({required this.ids});

  factory CleanControlPayload.fromJson(Map<String, dynamic> json) =>
      CleanControlPayload(ids: List<String>.from(json['ids']));
}
