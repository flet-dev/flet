double parseDouble(dynamic v, [double defValue = 0]) {
  if (v is double) {
    return v;
  } else if (v == null) {
    return 0;
  } else {
    return double.tryParse(v.toString()) ?? defValue;
  }
}
