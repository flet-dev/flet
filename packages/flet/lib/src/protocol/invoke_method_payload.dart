class InvokeMethodPayload {
  final String methodId;
  final String methodName;
  final String controlId;
  final Map<String, String> args;

  InvokeMethodPayload(
      {required this.methodId,
      required this.methodName,
      required this.controlId,
      required this.args});

  factory InvokeMethodPayload.fromJson(Map<String, dynamic> json) {
    return InvokeMethodPayload(
        methodId: json["methodId"],
        methodName: json['methodName'],
        controlId: json["controlId"],
        args: json['arguments'] != null
            ? Map<String, String>.from(json['arguments'])
            : {});
  }
}
