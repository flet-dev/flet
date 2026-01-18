import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:msgpack_dart/msgpack_dart.dart';

import '../utils/strings.dart';
import 'js_interop.dart' show JSAny;

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
    } else if (object is JSAny) {
      return 4;
    }
    debugPrint(
        "FletMsgpackEncoder: unknown type: ${object.runtimeType}: $object");
    return 0;
  }

  @override
  Uint8List encodeObject(dynamic object) {
    if (object is DateTime) {
      var iso = object.toUtc().toIso8601String();
      // Z suffix is not supported by Python's `datetime.fromisoformat`
      iso = iso.endsWith('Z') ? "${iso.trimEnd('Z')}+00:00" : iso;
      return codec.encode(iso);
    } else if (object is TimeOfDay) {
      return codec.encode("${object.hour}:${object.minute}");
    } else if (object is Duration) {
      return codec.encode(object.inMicroseconds.toString());
    } else if (object is JSAny) {
      return codec.encode(object.toString());
    }
    return Uint8List(0);
  }
}
