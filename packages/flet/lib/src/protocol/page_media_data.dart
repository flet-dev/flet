import 'package:equatable/equatable.dart';
import 'package:flutter/widgets.dart';

class PageMediaData extends Equatable {
  final PaddingData padding;
  final PaddingData viewPadding;
  final PaddingData viewInsets;
  final double devicePixelRatio;
  final Orientation orientation;

  const PageMediaData({
    required this.padding,
    required this.viewPadding,
    required this.viewInsets,
    required this.devicePixelRatio,
    required this.orientation,
  });

  Map<String, dynamic> toMap() => <String, dynamic>{
        'padding': padding.toMap(),
        'view_padding': viewPadding.toMap(),
        'view_insets': viewInsets.toMap(),
        'device_pixel_ratio': devicePixelRatio,
        'orientation': orientation.name,
      };

  @override
  List<Object?> get props =>
      [padding, viewPadding, viewInsets, devicePixelRatio, orientation];
}

class PaddingData extends Equatable {
  final double top;
  final double right;
  final double bottom;
  final double left;

  PaddingData(EdgeInsets insets)
      : top = insets.top,
        right = insets.right,
        bottom = insets.bottom,
        left = insets.left;

  Map<String, dynamic> toMap() => <String, dynamic>{
        'top': top,
        'right': right,
        'bottom': bottom,
        'left': left,
      };

  @override
  List<Object?> get props => [top, right, bottom, left];
}
