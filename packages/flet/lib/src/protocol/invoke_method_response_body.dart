class InvokeMethodResponseBody {
  final int id;
  final String name;
  final dynamic result;
  final String? error;

  InvokeMethodResponseBody(
      {required this.id, required this.name, this.result, this.error});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'id': id,
        'name': name,
        'result': result,
        'error': error
      };
}
