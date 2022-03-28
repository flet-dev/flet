class UpdateControlPropsRequest {
  final List<Map<String, String>> props;

  UpdateControlPropsRequest({required this.props});

  Map<String, dynamic> toJson() => <String, dynamic>{'props': props};
}
