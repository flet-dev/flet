class PythonOutputBody {
  final String text;
  final bool isStderr;

  PythonOutputBody({required this.text, required this.isStderr});

  factory PythonOutputBody.fromJson(Map<dynamic, dynamic> json) =>
      PythonOutputBody(
        text: json['text'] as String,
        isStderr: json['is_stderr'] as bool? ?? false,
      );
}
