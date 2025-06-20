class AssetSource {
  final String path;
  final bool isFile;

  const AssetSource({required this.path, required this.isFile});

  @override
  String toString() {
    return 'AssetSource(path: $path, isFile: $isFile)';
  }
}
