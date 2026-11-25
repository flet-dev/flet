import 'dart:math' as math;

import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';
import 'package:flutter/rendering.dart';

/// Builds an input field with the control's `error_text` below it.
///
/// [builder] receives the color for the field's underline: red while
/// `error_text` is set, otherwise `null` for the default colors. The error
/// text is styled like fluent_ui's `FormRow`, which its `TextFormBox` uses.
///
/// Call it with a context below the Fluent theme. The layout is
/// [_FieldLayout] (as in flet-shadcn-ui), not `FormRow`'s Column: the field
/// keeps the constraints it would get without the error (a Column loosens a
/// fixed width, shrinking button-like fields such as ComboBox), and it is
/// always wrapped the same way, so its state and focus survive an error
/// appearing or clearing.
Widget buildFluentField(
  BuildContext context,
  Control control,
  Widget Function(Color? errorColor) builder,
) {
  final theme = FluentTheme.of(context);
  final errorText = control.getString("error_text");
  final hasError = errorText != null && errorText.isNotEmpty;
  final errorColor = Colors.red.defaultBrushFor(theme.brightness);

  return _FieldLayout(
    fieldIndex: 0,
    children: [
      KeyedSubtree(
        key: const ValueKey("field"),
        child: builder(hasError ? errorColor : null),
      ),
      if (hasError)
        Padding(
          key: const ValueKey("error"),
          padding: const EdgeInsetsDirectional.only(top: 2),
          child: Text(
            errorText,
            style: TextStyle(color: errorColor, fontWeight: FontWeight.w500),
          ),
        ),
    ],
  );
}

/// Stacks a field with texts above and below it.
///
/// The field (the child at [fieldIndex]) is laid out with the incoming width
/// constraints. The layout is as wide as the field unless a text is wider,
/// and texts wrap at the incoming maximum width. With no texts, the field is
/// laid out exactly as if it were not wrapped.
class _FieldLayout extends MultiChildRenderObjectWidget {
  final int fieldIndex;

  const _FieldLayout({required this.fieldIndex, required super.children});

  @override
  RenderObject createRenderObject(BuildContext context) =>
      _RenderFieldLayout(fieldIndex);

  @override
  void updateRenderObject(
    BuildContext context,
    _RenderFieldLayout renderObject,
  ) {
    renderObject.fieldIndex = fieldIndex;
  }
}

class _FieldLayoutParentData extends ContainerBoxParentData<RenderBox> {}

class _RenderFieldLayout extends RenderBox
    with
        ContainerRenderObjectMixin<RenderBox, _FieldLayoutParentData>,
        RenderBoxContainerDefaultsMixin<RenderBox, _FieldLayoutParentData> {
  _RenderFieldLayout(this._fieldIndex);

  int _fieldIndex;
  set fieldIndex(int value) {
    if (value == _fieldIndex) return;
    _fieldIndex = value;
    markNeedsLayout();
  }

  @override
  void setupParentData(RenderBox child) {
    if (child.parentData is! _FieldLayoutParentData) {
      child.parentData = _FieldLayoutParentData();
    }
  }

  List<RenderBox> get _children => getChildrenAsList();

  /// The height to ask children's intrinsic widths at: the given one when the
  /// field is alone (so the wrapper is transparent), otherwise unbounded,
  /// since the height is shared between the field and its texts.
  double _childHeight(double height) =>
      childCount == 1 ? height : double.infinity;

  @override
  double computeMinIntrinsicWidth(double height) => _children
      .map((c) => c.getMinIntrinsicWidth(_childHeight(height)))
      .fold(0.0, math.max);

  @override
  double computeMaxIntrinsicWidth(double height) => _children
      .map((c) => c.getMaxIntrinsicWidth(_childHeight(height)))
      .fold(0.0, math.max);

  @override
  double computeMinIntrinsicHeight(double width) => _children
      .map((c) => c.getMinIntrinsicHeight(width))
      .fold(0.0, (a, b) => a + b);

  @override
  double computeMaxIntrinsicHeight(double width) => _children
      .map((c) => c.getMaxIntrinsicHeight(width))
      .fold(0.0, (a, b) => a + b);

  @override
  Size computeDryLayout(BoxConstraints constraints) =>
      _layout(constraints, (child, c) => child.getDryLayout(c), null);

  @override
  void performLayout() {
    size = _layout(
      constraints,
      (child, c) {
        child.layout(c, parentUsesSize: true);
        return child.size;
      },
      (child, offset) =>
          (child.parentData as _FieldLayoutParentData).offset = offset,
    );
  }

  Size _layout(
    BoxConstraints constraints,
    Size Function(RenderBox child, BoxConstraints c) layoutChild,
    void Function(RenderBox child, Offset offset)? position,
  ) {
    final children = _children;
    if (children.length == 1) {
      position?.call(children.first, Offset.zero);
      return layoutChild(children.first, constraints);
    }

    final field = children[_fieldIndex];
    final fieldSize = layoutChild(
      field,
      constraints.copyWith(minHeight: 0, maxHeight: double.infinity),
    );

    var width = fieldSize.width;
    for (final child in children) {
      if (child == field) continue;
      width = math.max(
        width,
        math.min(
          child.getMaxIntrinsicWidth(double.infinity),
          constraints.maxWidth,
        ),
      );
    }
    width = constraints.constrainWidth(width);

    var y = 0.0;
    for (final child in children) {
      final childSize = child == field
          ? fieldSize
          : layoutChild(child, BoxConstraints(maxWidth: width));
      position?.call(child, Offset(0, y));
      y += childSize.height;
    }
    return constraints.constrain(Size(width, y));
  }

  @override
  bool hitTestChildren(BoxHitTestResult result, {required Offset position}) =>
      defaultHitTestChildren(result, position: position);

  @override
  void paint(PaintingContext context, Offset offset) =>
      defaultPaint(context, offset);
}
