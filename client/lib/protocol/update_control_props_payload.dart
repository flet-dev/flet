class UpdateControlPropsPayload {
  final List<Map<String, String>> props;

  UpdateControlPropsPayload({required this.props});

  factory UpdateControlPropsPayload.fromJson(Map<String, dynamic> json) {
    var propsJson = json['props'] as List;
    var props = propsJson
        .map((propJson) => Map<String, String>.from(propJson))
        .toList();
    return UpdateControlPropsPayload(props: props);
  }
}
