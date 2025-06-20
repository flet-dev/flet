class PatchControlRequestBody {
  final int id;
  final List<dynamic> patch;

  PatchControlRequestBody({
    required this.id,
    required this.patch,
  });

  factory PatchControlRequestBody.fromJson(Map<dynamic, dynamic> json) {
    return PatchControlRequestBody(
      id: json["id"],
      patch: List<dynamic>.from(json['patch']),
    );
  }
}
