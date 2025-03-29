import 'package:equatable/equatable.dart';

class PageArgsModel extends Equatable {
  final Uri? pageUri;
  final String assetsDir;

  const PageArgsModel({required this.pageUri, required this.assetsDir});

  @override
  List<Object?> get props => [pageUri, assetsDir];
}
