class ControlEventBody {
  final int target;
  final String name;
  final dynamic data;

  ControlEventBody(
      {required this.target, required this.name, required this.data});

  Map<String, dynamic> toJson() =>
      <String, dynamic>{'target': target, 'name': name, 'data': data};
}
