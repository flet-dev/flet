class AppendControlPropsPayload {
  final List<Map<String, String>> props;

  AppendControlPropsPayload({required this.props});

  factory AppendControlPropsPayload.fromJson(Map<String, dynamic> json) {
    var propsJson = json['props'] as List;
    var props = propsJson
        .map((propJson) => Map<String, String>.from(propJson))
        .toList();
    return AppendControlPropsPayload(props: props);
  }
}
