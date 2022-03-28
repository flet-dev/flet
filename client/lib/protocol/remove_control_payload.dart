class RemoveControlPayload {
  final List<String> ids;

  RemoveControlPayload({required this.ids});

  factory RemoveControlPayload.fromJson(Map<String, dynamic> json) =>
      RemoveControlPayload(ids: List<String>.from(json['ids']));
}
