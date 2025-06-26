import 'dart:convert';
import 'dart:typed_data';

import 'package:msgpack_dart/msgpack_dart.dart';

/// Thrown when a complete MessagePack object cannot be decoded
/// because the data is incomplete.
class IncompleteDataError extends FormatError {
  IncompleteDataError(super.message);
}

class _Deserializer {
  final ExtDecoder? _extDecoder;
  final codec = const Utf8Codec();
  final Uint8List _list;
  final ByteData _data;
  int _offset = 0;

  /// If false, decoded binary data buffers will reference underlying input
  /// buffer and thus may change when the content of input buffer changes.
  /// If true, decoded buffers are copies and the underlying input buffer is
  /// free to change after decoding.
  final bool copyBinaryData;

  /// The current offset after decoding
  int get offset => _offset;

  _Deserializer(
    Uint8List list, {
    ExtDecoder? extDecoder,
    this.copyBinaryData = false,
    int initialOffset = 0,
  })  : _list = list,
        _data =
            ByteData.view(list.buffer, list.offsetInBytes, list.lengthInBytes),
        _extDecoder = extDecoder {
    _offset = initialOffset;
  }

  // Checks that at least [required] bytes are available,
  // or throws an IncompleteDataError.
  void _ensureAvailable(int required) {
    if (_offset + required > _list.length) {
      throw IncompleteDataError(
          "Not enough data: require $required more bytes, available ${_list.length - _offset}");
    }
  }

  dynamic decode() {
    _ensureAvailable(1);
    final u = _list[_offset++];
    if (u <= 127) {
      return u;
    } else if ((u & 0xE0) == 0xE0) {
      // negative small integer
      return u - 256;
    } else if ((u & 0xE0) == 0xA0) {
      return _readString(u & 0x1F);
    } else if ((u & 0xF0) == 0x90) {
      return _readArray(u & 0xF);
    } else if ((u & 0xF0) == 0x80) {
      return _readMap(u & 0xF);
    }
    switch (u) {
      case 0xc0:
        return null;
      case 0xc2:
        return false;
      case 0xc3:
        return true;
      case 0xcc:
        return _readUInt8();
      case 0xcd:
        return _readUInt16();
      case 0xce:
        return _readUInt32();
      case 0xcf:
        return _readUInt64();
      case 0xd0:
        return _readInt8();
      case 0xd1:
        return _readInt16();
      case 0xd2:
        return _readInt32();
      case 0xd3:
        return _readInt64();
      case 0xca:
        return _readFloat();
      case 0xcb:
        return _readDouble();
      case 0xd9:
        return _readString(_readUInt8());
      case 0xda:
        return _readString(_readUInt16());
      case 0xdb:
        return _readString(_readUInt32());
      case 0xc4:
        return _readBuffer(_readUInt8());
      case 0xc5:
        return _readBuffer(_readUInt16());
      case 0xc6:
        return _readBuffer(_readUInt32());
      case 0xdc:
        return _readArray(_readUInt16());
      case 0xdd:
        return _readArray(_readUInt32());
      case 0xde:
        return _readMap(_readUInt16());
      case 0xdf:
        return _readMap(_readUInt32());
      case 0xd4:
        return _readExt(1);
      case 0xd5:
        return _readExt(2);
      case 0xd6:
        return _readExt(4);
      case 0xd7:
        return _readExt(8);
      case 0xd8:
        return _readExt(16);
      case 0xc7:
        return _readExt(_readUInt8());
      case 0xc8:
        return _readExt(_readUInt16());
      case 0xc9:
        return _readExt(_readUInt32());
      default:
        throw FormatError("Invalid MessagePack format");
    }
  }

  int _readInt8() {
    _ensureAvailable(1);
    return _data.getInt8(_offset++);
  }

  int _readUInt8() {
    _ensureAvailable(1);
    return _data.getUint8(_offset++);
  }

  int _readUInt16() {
    _ensureAvailable(2);
    final res = _data.getUint16(_offset);
    _offset += 2;
    return res;
  }

  int _readInt16() {
    _ensureAvailable(2);
    final res = _data.getInt16(_offset);
    _offset += 2;
    return res;
  }

  int _readUInt32() {
    _ensureAvailable(4);
    final res = _data.getUint32(_offset);
    _offset += 4;
    return res;
  }

  int _readInt32() {
    _ensureAvailable(4);
    final res = _data.getInt32(_offset);
    _offset += 4;
    return res;
  }

  int _readUInt64() {
    _ensureAvailable(8);
    final res = _data.getUint64(_offset);
    _offset += 8;
    return res;
  }

  int _readInt64() {
    _ensureAvailable(8);
    final res = _data.getInt64(_offset);
    _offset += 8;
    return res;
  }

  double _readFloat() {
    _ensureAvailable(4);
    final res = _data.getFloat32(_offset);
    _offset += 4;
    return res;
  }

  double _readDouble() {
    _ensureAvailable(8);
    final res = _data.getFloat64(_offset);
    _offset += 8;
    return res;
  }

  Uint8List _readBuffer(int length) {
    _ensureAvailable(length);
    final res =
        Uint8List.view(_list.buffer, _list.offsetInBytes + _offset, length);
    _offset += length;
    return copyBinaryData ? Uint8List.fromList(res) : res;
  }

  String _readString(int length) {
    final list = _readBuffer(length);
    final len = list.length;
    for (int i = 0; i < len; ++i) {
      if (list[i] > 127) {
        return codec.decode(list);
      }
    }
    return String.fromCharCodes(list);
  }

  List _readArray(int length) {
    final res = List<dynamic>.filled(length, null, growable: false);
    for (int i = 0; i < length; ++i) {
      res[i] = decode();
    }
    return res;
  }

  Map _readMap(int length) {
    final res = {};
    while (length > 0) {
      res[decode()] = decode();
      --length;
    }
    return res;
  }

  dynamic _readExt(int length) {
    final extType = _readUInt8();
    final data = _readBuffer(length);
    return _extDecoder?.decodeObject(extType, data);
  }
}

/// A helper to decode MessagePack data as it arrives in chunks.
/// Call [addChunk] for every incoming piece of data,
/// then [decodeMessages] to retrieve complete messages.
class StreamingMsgpackDeserializer {
  final ExtDecoder? _extDecoder;
  final bool copyBinaryData;
  final BytesBuilder _buffer = BytesBuilder();

  StreamingMsgpackDeserializer(
      {ExtDecoder? extDecoder, this.copyBinaryData = false})
      : _extDecoder = extDecoder;

  /// Adds a new chunk of MessagePack data.
  void addChunk(Uint8List chunk) {
    _buffer.add(chunk);
  }

  /// Attempts to decode as many complete messages as possible
  /// from the buffered data. Incomplete trailing data remains in the buffer.
  List<dynamic> decodeMessages() {
    List<dynamic> messages = [];
    Uint8List data = _buffer.takeBytes();
    int offset = 0;
    while (offset < data.length) {
      try {
        // Create a Deserializer using the current offset
        _Deserializer d = _Deserializer(
          data,
          extDecoder: _extDecoder,
          copyBinaryData: copyBinaryData,
          initialOffset: offset,
        );
        dynamic message = d.decode();
        messages.add(message);
        offset = d.offset;
      } on IncompleteDataError {
        // Not enough data to decode a full message; break out of the loop.
        break;
      } on FormatError {
        // For actual format errors (not just incomplete data),
        // rethrow or handle as needed.
        rethrow;
      }
    }
    // If there is any leftover (incomplete) data, put it back into the buffer.
    if (offset < data.length) {
      _buffer.add(data.sublist(offset));
    }
    return messages;
  }
}
