import 'package:equatable/equatable.dart';
import 'package:flutter/widgets.dart';

class PageMediaData extends Equatable {
  final PaddingData padding;
  final PaddingData viewPadding;
  final PaddingData viewInsets;

  const PageMediaData(
      {required this.padding,
      required this.viewPadding,
      required this.viewInsets});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'padding': padding,
        'view_padding': viewPadding,
        'view_insets': viewInsets,
      };

  @override
  List<Object?> get props => [padding, viewPadding, viewInsets];
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

  Map<String, dynamic> toJson() => <String, dynamic>{
        'top': top,
        'right': right,
        'bottom': bottom,
        'left': left,
      };

  @override
  List<Object?> get props => [top, right, bottom, left];
}
