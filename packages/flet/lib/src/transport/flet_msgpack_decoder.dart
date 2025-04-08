import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:msgpack_dart/msgpack_dart.dart';

class FletMsgpackDecoder extends ExtDecoder {
  final codec = const Utf8Codec();

  @override
  dynamic decodeObject(int extType, Uint8List data) {
    if (extType == 1) {
      var isoDate = codec.decode(data);
      return DateTime.parse(isoDate);
    } else if (extType == 2) {
      var parts =
          codec.decode(data).split(":").map((s) => int.parse(s)).toList();
      return TimeOfDay(hour: parts[0], minute: parts[1]);
    }
    return null;
  }
}
