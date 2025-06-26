class InvokeMethodRequestBody {
  final int controlId;
  final String callId;
  final String name;
  final dynamic args;
  final Duration timeout;

  InvokeMethodRequestBody(
      {required this.controlId,
      required this.callId,
      required this.name,
      required this.args,
      required this.timeout});

  factory InvokeMethodRequestBody.fromJson(Map<dynamic, dynamic> json) {
    return InvokeMethodRequestBody(
        controlId: json["control_id"],
        callId: json["call_id"],
        name: json['name'],
        args: json['args'],
        timeout: Duration(
            seconds: json.containsKey("timeout") ? json['timeout'] : 10));
  }
}
