class InvokeMethodPayload {
  final String methodId;
  final String methodName;
  final Map<String, String> args;

  InvokeMethodPayload(
      {required this.methodId, required this.methodName, required this.args});

  factory InvokeMethodPayload.fromJson(Map<String, dynamic> json) {
    return InvokeMethodPayload(
        methodId: json["methodId"],
        methodName: json['methodName'],
        args: json['arguments'] != null
            ? Map<String, String>.from(json['arguments'])
            : {});
  }
}
