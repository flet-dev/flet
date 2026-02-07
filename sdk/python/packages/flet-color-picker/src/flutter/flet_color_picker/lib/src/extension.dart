import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';

import 'color_picker.dart';
import 'hue_ring_picker.dart';
import 'material_picker.dart';
import 'slide_picker.dart';
import 'block_picker.dart';
import 'multiple_choice_block_picker.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "ColorPicker":
        return ColorPickerControl(control: control);
      case "HueRingPicker":
        return HueRingPickerControl(control: control);
      case "SlidePicker":
        return SlidePickerControl(control: control);
      case "MaterialPicker":
        return MaterialPickerControl(control: control);
      case "BlockPicker":
        return BlockPickerControl(control: control);
      case "MultipleChoiceBlockPicker":
        return MultipleChoiceBlockPickerControl(control: control);
      default:
        return null;
    }
  }
}
