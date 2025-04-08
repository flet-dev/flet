import 'dart:convert';
import 'dart:typed_data';

import 'package:msgpack_dart/msgpack_dart.dart';

class FletMsgpackEncoder extends ExtEncoder {
  final codec = const Utf8Codec();

  @override
  int extTypeForObject(dynamic object) {
    if (object is DateTime) {
      return 42;
    }
    return 0;
  }

  @override
  Uint8List encodeObject(dynamic object) {
    if (object is DateTime) {
      return codec.encode(object.toIso8601String());
    }
    return Uint8List(0);
  }
}
