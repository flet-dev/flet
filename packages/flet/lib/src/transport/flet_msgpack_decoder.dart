import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:msgpack_dart/msgpack_dart.dart';

class FletMsgpackDecoder extends ExtDecoder {
  final codec = const Utf8Codec();

  @override
  dynamic decodeObject(int extType, Uint8List data) {
    if (extType == 42) {
      var isoDate = codec.decode(data);
      return DateTime.parse(isoDate);
    }
    return null;
  }
}
