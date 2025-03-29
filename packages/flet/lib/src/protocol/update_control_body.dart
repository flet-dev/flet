class UpdateControlBody {
  final int id;
  final Map<String, dynamic> props;

  UpdateControlBody({required this.id, required this.props});

  Map<String, dynamic> toJson() => <String, dynamic>{'id': id, 'props': props};
}
