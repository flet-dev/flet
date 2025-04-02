class InvokeMethodResponseBody {
  final int controlId;
  final String callId;
  final dynamic result;
  final String? error;

  InvokeMethodResponseBody(
      {required this.controlId, required this.callId, this.result, this.error});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'control_id': controlId,
        'call_id': callId,
        'result': result,
        'error': error
      };
}
