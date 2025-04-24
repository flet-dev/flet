class ControlEventBody {
  final int target;
  final String name;
  final dynamic data;
  final Map<String, dynamic>? fields;

  ControlEventBody(
      {required this.target,
      required this.name,
      required this.data,
      this.fields});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'target': target,
        'name': name,
        'data': data,
        'fields': fields
      };
}
