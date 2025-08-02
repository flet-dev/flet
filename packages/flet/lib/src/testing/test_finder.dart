abstract class TestFinder {
  static int _nextId = 0;

  final int id = _nextId++;

  Object get raw;
  int get count;

  Map<String, dynamic> toMap() => {
        "id": id,
        "count": count,
      };
}
