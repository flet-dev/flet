import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:msgpack_dart/msgpack_dart.dart';

class FletMsgpackEncoder extends ExtEncoder {
  final codec = const Utf8Codec();

  @override
  int extTypeForObject(dynamic object) {
    if (object is DateTime) {
      return 1;
    } else if (object is TimeOfDay) {
      return 2;
    } else if (object is Duration) {
      return 3;
    }
    return 0;
  }

  @override
  Uint8List encodeObject(dynamic object) {
    if (object is DateTime) {
      return codec.encode(object.toIso8601String());
    } else if (object is TimeOfDay) {
      return codec.encode("${object.hour}:${object.minute}");
    } else if (object is Duration) {
      return codec.encode(object.inMicroseconds.toString());
    }
    return Uint8List(0);
  }
}
