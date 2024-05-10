double? parseDouble(dynamic v, [double? defValue]) {
  if (v is double) {
    return v;
  } else if (v == null) {
    return defValue;
  } else {
    return double.tryParse(v.toString()) ?? defValue;
  }
}

int? parseInt(dynamic v, [int? defValue]) {
  if (v is int) {
    return v;
  } else if (v == null) {
    return defValue;
  } else {
    return int.tryParse(v.toString()) ?? defValue;
  }
}

bool parseBool(dynamic v, [bool defValue = false]) {
  if (v is bool) {
    return v;
  } else if (v == null) {
    return defValue;
  } else {
    return "true" == v.toString().toLowerCase();
  }
}
