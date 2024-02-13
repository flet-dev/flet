class InvokeMethodResult {
  final String methodId;
  final String? result;
  final String? error;

  InvokeMethodResult({required this.methodId, this.result, this.error});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'method_id': methodId,
        'result': result,
        'error': error
      };
}
