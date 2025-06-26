class UpdateControlBody {
  final int id;
  final Map<String, dynamic> props;

  UpdateControlBody({required this.id, required this.props});

  Map<String, dynamic> toMap() => <String, dynamic>{'id': id, 'props': props};
}
