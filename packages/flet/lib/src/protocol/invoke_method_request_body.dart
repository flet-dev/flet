class InvokeMethodRequestBody {
  final int id;
  final String name;
  final dynamic args;
  final Duration timeout;

  InvokeMethodRequestBody(
      {required this.id,
      required this.name,
      required this.args,
      required this.timeout});

  factory InvokeMethodRequestBody.fromJson(Map<dynamic, dynamic> json) {
    return InvokeMethodRequestBody(
        id: json["id"],
        name: json['name'],
        args: json['args'],
        timeout: Duration(
            seconds: json.containsKey("timeout") ? json['timeout'] : 10));
  }
}
