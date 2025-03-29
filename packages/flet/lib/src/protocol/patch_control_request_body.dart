class PatchControlRequestBody {
  final int id;
  final Map<String, dynamic> patch;

  PatchControlRequestBody({
    required this.id,
    required this.patch,
  });

  factory PatchControlRequestBody.fromJson(Map<dynamic, dynamic> json) {
    return PatchControlRequestBody(
      id: json["id"],
      patch: Map<String, dynamic>.from(json['patch']),
    );
  }
}
