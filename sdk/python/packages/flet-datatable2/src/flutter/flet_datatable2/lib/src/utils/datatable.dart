import 'package:collection/collection.dart';
import 'package:data_table_2/data_table_2.dart';

ColumnSize? parseColumnSize(String? size, [ColumnSize? defValue]) {
  if (size == null) {
    return defValue;
  }
  return ColumnSize.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == size.toLowerCase()) ??
      defValue;
}
