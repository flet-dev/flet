import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import 'create_control.dart';

enum FormFieldInputBorder { outline, underline, none }

TextInputType parseTextInputType(String type) {
  switch (type.toLowerCase()) {
    case "datetime":
      return TextInputType.datetime;
    case "email":
      return TextInputType.emailAddress;
    case "multiline":
      return TextInputType.multiline;
    case "name":
      return TextInputType.name;
    case "none":
      return TextInputType.none;
    case "number":
      return TextInputType.number;
    case "phone":
      return TextInputType.phone;
    case "streetaddress":
      return TextInputType.streetAddress;
    case "text":
      return TextInputType.text;
    case "url":
      return TextInputType.url;
    case "visiblepassword":
      return TextInputType.visiblePassword;
  }
  return TextInputType.text;
}

InputDecoration buildInputDecoration(
    Control control, Control? prefix, Control? suffix, Widget? customSuffix) {
  String? label = control.attrString("label", "")!;
  FormFieldInputBorder inputBorder = FormFieldInputBorder.values.firstWhere(
    ((b) => b.name == control.attrString("border", "")!.toLowerCase()),
    orElse: () => FormFieldInputBorder.outline,
  );
  var icon = getMaterialIcon(control.attrString("icon", "")!);

  var prefixIcon = getMaterialIcon(control.attrString("prefixIcon", "")!);
  var prefixText = control.attrString("prefixText");
  var suffixIcon = getMaterialIcon(control.attrString("suffixIcon", "")!);
  var suffixText = control.attrString("suffixText");

  return InputDecoration(
      contentPadding: parseEdgeInsets(control, "contentPadding"),
      label: label != "" ? Text(label) : null,
      border: inputBorder == FormFieldInputBorder.none
          ? InputBorder.none
          : inputBorder == FormFieldInputBorder.outline
              ? const OutlineInputBorder()
              : const UnderlineInputBorder(),
      icon: icon != null ? Icon(icon) : null,
      filled: control.attrBool("filled", false)!,
      hintText: control.attrString("hintText"),
      helperText: control.attrString("helperText"),
      counterText: control.attrString("counterText"),
      errorText: control.attrString("errorText"),
      prefixIcon: prefixIcon != null ? Icon(prefixIcon) : null,
      prefixText: prefixText,
      prefix: prefix != null
          ? createControl(control, prefix.id, control.isDisabled)
          : null,
      suffix: suffix != null
          ? createControl(control, suffix.id, control.isDisabled)
          : null,
      suffixIcon: suffixIcon != null ? Icon(suffixIcon) : customSuffix,
      suffixText: suffixText);
}
