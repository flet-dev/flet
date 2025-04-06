import 'dart:ui';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/animations.dart';
import '../utils/autofill.dart';
import '../utils/badge.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/dismissible.dart';
import '../utils/drawing.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/gradient.dart';
import '../utils/icons.dart';
import '../utils/images.dart';
import '../utils/locale.dart';
import '../utils/markdown.dart';
import '../utils/menu.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/misc.dart';
import '../utils/overlay_style.dart';
import '../utils/platform.dart';
import '../utils/responsive.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import '../utils/theme.dart';
import '../utils/time.dart';
import '../utils/tooltip.dart';
import '../utils/transforms.dart';
import '../utils/user_fonts.dart';

/// Extension on [Control] to easily convert child or children controls
/// into corresponding [Widget]s using [ControlWidget].
extension WidgetFromControl on Control {
  /// Returns a list of [Widget]s built from the children of this control
  /// under the given [propertyName].
  ///
  /// If [visibleOnly] is `true` (default), only includes children that are visible.
  ///
  /// If [notifyParent] is `true`, sets `notifyParent` on each child control.
  List<Widget> buildWidgets(String propertyName,
      {bool visibleOnly = true, bool notifyParent = false}) {
    return children(propertyName, visibleOnly: visibleOnly).map((child) {
      child.notifyParent = notifyParent;
      return ControlWidget(control: child);
    }).toList();
  }

  /// Returns a single [Widget] built from the child of this control
  /// under the given [propertyName], or `null` if not present or not visible.
  ///
  /// If [visibleOnly] is `true` (default), returns `null` for an invisible child.
  ///
  /// If [notifyParent] is `true`, sets `notifyParent` on the child control.
  ///
  /// If [key] is provided, applies it to the returned [ControlWidget].
  Widget? buildWidget(String propertyName,
      {bool visibleOnly = true, bool notifyParent = false, Key? key}) {
    final c = child(propertyName, visibleOnly: visibleOnly);
    if (c == null) return null;
    c.notifyParent = notifyParent;
    return ControlWidget(key: key, control: c);
  }
}

extension AlignmentParsers on Control {
  MainAxisAlignment? getMainAxisAlignment(String propertyName,
      [MainAxisAlignment? defaultValue]) {
    return parseMainAxisAlignment(get(propertyName), defaultValue);
  }

  CrossAxisAlignment? getCrossAxisAlignment(String propertyName,
      [CrossAxisAlignment? defaultValue]) {
    return parseCrossAxisAlignment(get(propertyName), defaultValue);
  }

  TabAlignment? getTabAlignment(String propertyName,
      [TabAlignment? defaultValue]) {
    return parseTabAlignment(get(propertyName), defaultValue);
  }

  WrapAlignment? getWrapAlignment(String propertyName,
      [WrapAlignment? defaultValue]) {
    return parseWrapAlignment(get(propertyName), defaultValue);
  }

  WrapCrossAlignment? getWrapCrossAlignment(String propertyName,
      [WrapCrossAlignment? defaultValue]) {
    return parseWrapCrossAlignment(get(propertyName), defaultValue);
  }

  Alignment? getAlignment(String propertyName, [Alignment? defaultValue]) {
    return parseAlignment(get(propertyName), defaultValue);
  }
}

extension AnimationParsers on Control {
  ImplicitAnimationDetails? getAnimation(String propertyName,
      [ImplicitAnimationDetails? defaultValue]) {
    return parseAnimation(get(propertyName), defaultValue);
  }

  Curve? getCurve(String propertyName, [Curve? defaultValue]) {
    return parseCurve(get(propertyName), defaultValue);
  }

  AnimationStyle? getAnimationStyle(String propertyName,
      [AnimationStyle? defaultValue]) {
    return parseAnimationStyle(get(propertyName), defaultValue);
  }
}

extension AutofillParsers on Control {
  List<String>? getAutofillHints(String propertyName,
      [List<String>? defaultValue]) {
    return parseAutofillHints(get(propertyName), defaultValue);
  }

  String? getAutofillHint(String propertyName, [String? defaultValue]) {
    return parseAutofillHint(get(propertyName), defaultValue);
  }

  AutofillContextAction? getAutofillContextAction(String propertyName,
      [AutofillContextAction? defaultValue]) {
    return parseAutofillContextAction(get(propertyName), defaultValue);
  }
}

extension BadgeParsers on Control {
  Badge? getBadge(String propertyName, Widget child, ThemeData theme) {
    return parseBadge(get(propertyName), child, theme);
  }
}

extension BorderParsers on Control {
  BorderRadius? getBorderRadius(String propertyName,
      [BorderRadius? defaultValue]) {
    return parseBorderRadius(get(propertyName), defaultValue);
  }

  Radius? getRadius(String propertyName, [Radius? defaultValue]) {
    return parseRadius(get(propertyName), defaultValue);
  }

  Border? getBorder(String propertyName, ThemeData theme,
      {Color? defaultSideColor,
      BorderSide? defaultBorderSide,
      Border? defaultValue}) {
    return parseBorder(get(propertyName), theme,
        defaultSideColor: defaultSideColor,
        defaultBorderSide: defaultBorderSide,
        defaultValue: defaultValue);
  }

  BorderSide? getBorderSide(String propertyName, ThemeData theme,
      {Color? defaultSideColor = Colors.black, BorderSide? defaultValue}) {
    return parseBorderSide(get(propertyName), theme,
        defaultSideColor: defaultSideColor, defaultValue: defaultValue);
  }

  OutlinedBorder? getOutlinedBorder(String propertyName,
      {BorderRadius? defaultBorderRadius = BorderRadius.zero,
      OutlinedBorder? defaultValue}) {
    return parseOutlinedBorder(get(propertyName),
        defaultBorderRadius: defaultBorderRadius, defaultValue: defaultValue);
  }

  WidgetStateBorderSide? getWidgetStateBorderSide(
      String propertyName, ThemeData theme,
      {BorderSide defaultBorderSide = BorderSide.none,
      WidgetStateBorderSide? defaultValue}) {
    return parseWidgetStateBorderSide(get(propertyName), theme,
        defaultBorderSide: defaultBorderSide, defaultValue: defaultValue);
  }

  WidgetStateProperty<OutlinedBorder?>? getWidgetStateOutlinedBorder(
      String propertyName,
      {OutlinedBorder? defaultOutlinedBorder,
      WidgetStateProperty<OutlinedBorder?>? defaultValue}) {
    return parseWidgetStateOutlinedBorder(get(propertyName),
        defaultOutlinedBorder: defaultOutlinedBorder,
        defaultValue: defaultValue);
  }
}

extension BoxDecorationParsers on Control {
  BoxConstraints? getBoxConstraints(String propertyName,
      [BoxConstraints? defaultValue]) {
    return parseBoxConstraints(get(propertyName), defaultValue);
  }

  List<BoxShadow>? getBoxShadows(String propertyName, ThemeData theme,
      [List<BoxShadow>? defaultValue]) {
    return parseBoxShadows(get(propertyName), theme, defaultValue);
  }

  BoxDecoration? getBoxDecoration(String propertyName, BuildContext context,
      [BoxDecoration? defaultValue]) {
    return parseBoxDecoration(get(propertyName), context, defaultValue);
  }

  DecorationImage? getDecorationImage(String propertyName, BuildContext context,
      [DecorationImage? defaultValue]) {
    return parseDecorationImage(get(propertyName), context, defaultValue);
  }
}

extension ButtonParsers on Control {
  ButtonStyle? getButtonStyle(String propertyName, ThemeData theme,
      {Color? defaultForegroundColor,
      Color? defaultBackgroundColor,
      Color? defaultOverlayColor,
      Color? defaultShadowColor,
      Color? defaultSurfaceTintColor,
      double? defaultElevation,
      EdgeInsets? defaultPadding,
      BorderSide? defaultBorderSide,
      OutlinedBorder? defaultShape,
      ButtonStyle? defaultValue}) {
    return parseButtonStyle(get(propertyName), theme,
        defaultForegroundColor: defaultForegroundColor,
        defaultBackgroundColor: defaultBackgroundColor,
        defaultOverlayColor: defaultOverlayColor,
        defaultShadowColor: defaultShadowColor,
        defaultSurfaceTintColor: defaultSurfaceTintColor,
        defaultElevation: defaultElevation,
        defaultPadding: defaultPadding,
        defaultBorderSide: defaultBorderSide,
        defaultShape: defaultShape,
        defaultValue: defaultValue);
  }

  FloatingActionButtonLocation? getFloatingActionButtonLocation(
      String propertyName,
      [FloatingActionButtonLocation? defaultValue]) {
    return parseFloatingActionButtonLocation(get(propertyName), defaultValue);
  }
}

extension ColorParsers on Control {
  Color? getColor(String propertyName, BuildContext? context,
      [Color? defaultValue]) {
    return parseColor(getString(propertyName),
        context != null ? Theme.of(context) : null, defaultValue);
  }

  WidgetStateProperty<Color?>? getWidgetStateColor(
      String propertyName, ThemeData theme,
      {Color? defaultColor, WidgetStateProperty<Color?>? defaultValue}) {
    return parseWidgetStateColor(get(propertyName), theme,
        defaultColor: defaultColor, defaultValue: defaultValue);
  }
}

extension DismissibleParsers on Control {
  DismissDirection? getDismissDirection(String propertyName,
      [DismissDirection? defaultValue]) {
    return parseDismissDirection(get(propertyName), defaultValue);
  }

  Map<DismissDirection, double>? getDismissThresholds(String propertyName,
      [Map<DismissDirection, double>? defaultValue]) {
    return parseDismissThresholds(get(propertyName), defaultValue);
  }
}

extension PaintParsers on Control {
  Paint? getPaint(String propertyName, ThemeData theme, [Paint? defaultValue]) {
    return parsePaint(get(propertyName), theme, defaultValue);
  }

  PaintingStyle? getPaintingStyle(String propertyName,
      [PaintingStyle? defaultValue]) {
    return parsePaintingStyle(get(propertyName), defaultValue);
  }

  List<double>? getPaintStrokeDashPattern(String propertyName,
      [List<double>? defaultValue]) {
    return parsePaintStrokeDashPattern(get(propertyName), defaultValue);
  }
}

extension EdgeInsetsParsers on Control {
  EdgeInsets? getEdgeInsets(String propertyName, [EdgeInsets? defaultValue]) {
    return parseEdgeInsets(get(propertyName), defaultValue);
  }

  EdgeInsets? getMargin(String propertyName, [EdgeInsets? defaultValue]) {
    return parseMargin(get(propertyName), defaultValue);
  }

  EdgeInsets? getPadding(String propertyName, [EdgeInsets? defaultValue]) {
    return parsePadding(get(propertyName), defaultValue);
  }

  EdgeInsetsDirectional? getEdgeInsetsDirectional(String propertyName,
      [EdgeInsetsDirectional? defaultValue]) {
    return parseEdgeInsetsDirectional(get(propertyName), defaultValue);
  }

  WidgetStateProperty<EdgeInsets?>? getWidgetStateEdgeInsets(
      String propertyName,
      {EdgeInsets? defaultEdgeInsets,
      WidgetStateProperty<EdgeInsets?>? defaultValue}) {
    return parseWidgetStateEdgeInsets(get(propertyName),
        defaultEdgeInsets: defaultEdgeInsets, defaultValue: defaultValue);
  }
}

extension InputParsers on Control {
  FormFieldInputBorder? getFormFieldInputBorder(String propertyName,
      [FormFieldInputBorder? defaultValue]) {
    return parseFormFieldInputBorder(get(propertyName), defaultValue);
  }

  TextInputType? getTextInputType(String propertyName,
      [TextInputType? defaultValue]) {
    return parseTextInputType(get(propertyName), defaultValue);
  }

  OverlayVisibilityMode? getOverlayVisibilityMode(String propertyName,
      [OverlayVisibilityMode? defaultValue]) {
    return parseVisibilityMode(get(propertyName), defaultValue);
  }

  StrutStyle? getStrutStyle(String propertyName, [StrutStyle? defaultValue]) {
    return parseStrutStyle(get(propertyName), defaultValue);
  }
}

extension GradientParsers on Control {
  Gradient? getGradient(String propertyName, ThemeData theme) {
    return parseGradient(get(propertyName), theme);
  }

  List<Color> getColors(String propertyName, ThemeData theme) {
    return parseColors(get(propertyName), theme);
  }

  List<double>? getGradientStops(String propertyName,
      [List<double>? defaultValue]) {
    return parseGradientStops(get(propertyName), defaultValue);
  }

  TileMode? getTileMode(String propertyName, [TileMode? defaultValue]) {
    return parseTileMode(get(propertyName), defaultValue);
  }

  GradientRotation? getGradientRotation(String propertyName,
      [GradientRotation? defaultValue]) {
    return parseRotation(get(propertyName), defaultValue);
  }
}

extension IconParsers on Control {
  IconData? getIcon(String propertyName, [IconData? defaultValue]) {
    return parseIcon(get(propertyName), defaultValue);
  }

  WidgetStateProperty<Icon?>? getWidgetStateIcon(
      String propertyName, ThemeData theme,
      {Icon? defaultIcon, WidgetStateProperty<Icon?>? defaultValue}) {
    return parseWidgetStateIcon(get(propertyName), theme,
        defaultIcon: defaultIcon, defaultValue: defaultValue);
  }
}

extension ImageParsers on Control {
  ImageRepeat? getImageRepeat(String propertyName,
      [ImageRepeat? defaultValue]) {
    return parseImageRepeat(get(propertyName), defaultValue);
  }

  BlendMode? getBlendMode(String propertyName, [BlendMode? defaultValue]) {
    return parseBlendMode(get(propertyName), defaultValue);
  }

  BoxFit? getBoxFit(String propertyName, [BoxFit? defaultValue]) {
    return parseBoxFit(get(propertyName), defaultValue);
  }

  ImageFilter? getBlur(String propertyName, [ImageFilter? defaultValue]) {
    return parseBlur(get(propertyName), defaultValue);
  }

  ColorFilter? getColorFilter(String propertyName, ThemeData theme,
      [ColorFilter? defaultValue]) {
    return parseColorFilter(get(propertyName), theme, defaultValue);
  }

  FilterQuality? getFilterQuality(String propertyName,
      [FilterQuality? defaultValue]) {
    return parseFilterQuality(get(propertyName), defaultValue);
  }
}

extension LocaleParsers on Control {
  Map<String, dynamic>? getLocaleConfiguration(String propertyName,
      [Map<String, dynamic>? defaultValue]) {
    return parseLocaleConfiguration(get(propertyName), defaultValue);
  }

  Locale? getLocale(String propertyName, [Locale? defaultValue]) {
    return parseLocale(get(propertyName), defaultValue);
  }
}

extension MarkdownParsers on Control {
  Map<String, TextStyle> getMarkdownCodeTheme(
      String propertyName, ThemeData theme) {
    return parseMarkdownCodeTheme(get(propertyName), theme);
  }
/*
  md.ExtensionSet? getMarkdownExtensionSet(String propertyName,
      [md.ExtensionSet? defaultValue]) {
    return parseMarkdownExtensionSet(get(propertyName), defaultValue);
  }


  MarkdownStyleSheet? getMarkdownStyleSheet(
      String propertyName, BuildContext context,
      [MarkdownStyleSheet? defaultValue]) {
    return parseMarkdownStyleSheet(get(propertyName), context, defaultValue);
  }
  */
}

extension WidgetStatePropertyParsers on Control {
  WidgetStateProperty<T?>? getWidgetStateProperty<T>(
      String propertyName, T Function(dynamic) converterFromJson,
      [T? defaultValue]) {
    return getWidgetStateProperty<T>(
        get(propertyName), converterFromJson, defaultValue);
  }
}

extension MenuParsers on Control {
  MenuStyle? getMenuStyle(String propertyName, ThemeData theme,
      {Color? defaultBackgroundColor,
      Color? defaultShadowColor,
      Color? defaultSurfaceTintColor,
      double? defaultElevation,
      Alignment? defaultAlignment,
      MouseCursor? defaultMouseCursor,
      EdgeInsets? defaultPadding,
      BorderSide? defaultBorderSide,
      OutlinedBorder? defaultShape,
      MenuStyle? defaultValue}) {
    return parseMenuStyle(get(propertyName), theme,
        defaultBackgroundColor: defaultBackgroundColor,
        defaultShadowColor: defaultShadowColor,
        defaultSurfaceTintColor: defaultSurfaceTintColor,
        defaultElevation: defaultElevation,
        defaultAlignment: defaultAlignment,
        defaultMouseCursor: defaultMouseCursor,
        defaultPadding: defaultPadding,
        defaultBorderSide: defaultBorderSide,
        defaultShape: defaultShape,
        defaultValue: defaultValue);
  }
}

extension MouseCursorParsers on Control {
  MouseCursor? getMouseCursor(String propertyName,
      [MouseCursor? defaultMouseCursor]) {
    return parseMouseCursor(get(propertyName), defaultMouseCursor);
  }

  WidgetStateProperty<MouseCursor?>? getWidgetStateMouseCursor(
      String propertyName,
      {MouseCursor? defaultMouseCursor,
      WidgetStateProperty<MouseCursor?>? defaultValue}) {
    return parseWidgetStateMouseCursor(get(propertyName),
        defaultMouseCursor: defaultMouseCursor, defaultValue: defaultValue);
  }
}

extension WidgetStateValueParsers on Control {
  WidgetStateProperty<double?>? getWidgetStateDouble(String propertyName,
      {double? defaultDouble, WidgetStateProperty<double?>? defaultValue}) {
    return parseWidgetStateDouble(get(propertyName),
        defaultDouble: defaultDouble, defaultValue: defaultValue);
  }

  WidgetStateProperty<int?>? getWidgetStateInt(String propertyName,
      {int? defaultInt, WidgetStateProperty<int?>? defaultValue}) {
    return parseWidgetStateInt(get(propertyName),
        defaultInt: defaultInt, defaultValue: defaultValue);
  }

  WidgetStateProperty<bool?>? getWidgetStateBool(String propertyName,
      {bool? defaultBool, WidgetStateProperty<bool?>? defaultValue}) {
    return parseWidgetStateBool(get(propertyName),
        defaultBool: defaultBool, defaultValue: defaultValue);
  }
}

extension MiscParsers on Control {
  Clip? getClip(String propertyName, [Clip? defaultValue]) {
    return parseClip(get(propertyName), defaultValue);
  }

  Orientation? getOrientation(String propertyName,
      [Orientation? defaultValue]) {
    return parseOrientation(get(propertyName), defaultValue);
  }

  StrokeCap? getStrokeCap(String propertyName, [StrokeCap? defaultValue]) {
    return parseStrokeCap(get(propertyName), defaultValue);
  }

  StrokeJoin? getStrokeJoin(String propertyName, [StrokeJoin? defaultValue]) {
    return parseStrokeJoin(get(propertyName), defaultValue);
  }

  BoxShape? getBoxShape(String propertyName, [BoxShape? defaultValue]) {
    return parseBoxShape(get(propertyName), defaultValue);
  }

  NotchedShape? getNotchedShape(String propertyName,
      [NotchedShape? defaultValue]) {
    return parseNotchedShape(get(propertyName), defaultValue);
  }

  SliderInteraction? getSliderInteraction(String propertyName,
      [SliderInteraction? defaultValue]) {
    return parseSliderInteraction(get(propertyName), defaultValue);
  }

  Size? getSize(String propertyName, [Size? defaultValue]) {
    return parseSize(get(propertyName), defaultValue);
  }

  SnackBarBehavior? getSnackBarBehavior(String propertyName,
      [SnackBarBehavior? defaultValue]) {
    return parseSnackBarBehavior(get(propertyName), defaultValue);
  }

  StackFit? getStackFit(String propertyName, [StackFit? defaultValue]) {
    return parseStackFit(get(propertyName), defaultValue);
  }

  DatePickerMode? getDatePickerMode(String propertyName,
      [DatePickerMode? defaultValue]) {
    return parseDatePickerMode(get(propertyName), defaultValue);
  }

  DatePickerEntryMode? getDatePickerEntryMode(String propertyName,
      [DatePickerEntryMode? defaultValue]) {
    return parseDatePickerEntryMode(get(propertyName), defaultValue);
  }

  CardVariant? getCardVariant(String propertyName,
      [CardVariant? defaultValue]) {
    return parseCardVariant(get(propertyName), defaultValue);
  }

  ScrollMode? getScrollMode(String propertyName,
      [ScrollMode? defaultValue = ScrollMode.none]) {
    return parseScrollMode(get(propertyName), defaultValue);
  }

  LabelPosition? getLabelPosition(String propertyName,
      [LabelPosition? defaultValue]) {
    return parseLabelPosition(get(propertyName), defaultValue);
  }

  CupertinoTimerPickerMode? getCupertinoTimerPickerMode(String propertyName,
      [CupertinoTimerPickerMode? defaultValue]) {
    return parseCupertinoTimerPickerMode(get(propertyName), defaultValue);
  }

  ListTileControlAffinity? getListTileControlAffinity(String propertyName,
      [ListTileControlAffinity? defaultValue]) {
    return parseListTileControlAffinity(get(propertyName), defaultValue);
  }

  ListTileStyle? getListTileStyle(String propertyName,
      [ListTileStyle? defaultValue]) {
    return parseListTileStyle(get(propertyName), defaultValue);
  }

  NavigationDestinationLabelBehavior? getNavigationDestinationLabelBehavior(
      String propertyName,
      [NavigationDestinationLabelBehavior? defaultValue]) {
    return parseNavigationDestinationLabelBehavior(
        get(propertyName), defaultValue);
  }

  PopupMenuPosition? getPopupMenuPosition(String propertyName,
      [PopupMenuPosition? defaultValue]) {
    return parsePopupMenuPosition(get(propertyName), defaultValue);
  }

  Assertiveness? getAssertiveness(String propertyName,
      [Assertiveness? defaultValue]) {
    return parseAssertiveness(get(propertyName), defaultValue);
  }

  DatePickerDateOrder? getDatePickerDateOrder(String propertyName,
      [DatePickerDateOrder? defaultValue]) {
    return parseDatePickerDateOrder(get(propertyName), defaultValue);
  }

  CupertinoDatePickerMode? getCupertinoDatePickerMode(String propertyName,
      [CupertinoDatePickerMode? defaultValue]) {
    return parseCupertinoDatePickerMode(get(propertyName), defaultValue);
  }

  ListTileTitleAlignment? getListTileTitleAlignment(String propertyName,
      [ListTileTitleAlignment? defaultValue]) {
    return parseListTileTitleAlignment(get(propertyName), defaultValue);
  }

  TimePickerEntryMode? getTimePickerEntryMode(String propertyName,
      [TimePickerEntryMode? defaultValue]) {
    return parseTimePickerEntryMode(get(propertyName), defaultValue);
  }

  Axis? getAxis(String propertyName, [Axis? defaultValue]) {
    return parseAxis(get(propertyName), defaultValue);
  }

  PointerDeviceKind? getPointerDeviceKind(String propertyName,
      [PointerDeviceKind? defaultValue]) {
    return parsePointerDeviceKind(get(propertyName), defaultValue);
  }

  NavigationRailLabelType? getNavigationRailLabelType(String propertyName,
      [NavigationRailLabelType? defaultValue]) {
    return parseNavigationRailLabelType(get(propertyName), defaultValue);
  }
}

extension SystemUiParsers on Control {
  SystemUiOverlayStyle? getSystemUiOverlayStyle(
      String propertyName, ThemeData? theme, Brightness? brightness,
      [SystemUiOverlayStyle? defaultValue]) {
    return parseSystemUiOverlayStyle(
        get(propertyName), theme, brightness, defaultValue);
  }

  Brightness? getBrightness(String propertyName, [Brightness? defaultValue]) {
    return parseBrightness(get(propertyName), defaultValue);
  }
}

extension PlatformParsers on Control {
  TargetPlatform? getTargetPlatform(String propertyName,
      [TargetPlatform? defaultValue]) {
    return parseTargetPlatform(get(propertyName), defaultValue);
  }
}

extension ResponsiveParsers on Control {
  Map<String, double> getResponsiveNumber(
      String propertyName, double defaultValue) {
    return parseResponsiveNumber(get(propertyName), defaultValue);
  }
}

extension TextParsers on Control {
  TextStyle? getTextStyle(String propertyName, ThemeData theme,
      [TextStyle? defaultValue]) {
    return parseTextStyle(get(propertyName), theme, defaultValue);
  }

  TextAlign? getTextAlign(String propertyName, [TextAlign? defaultValue]) {
    return parseTextAlign(get(propertyName), defaultValue);
  }

  TextOverflow? getTextOverflow(String propertyName,
      [TextOverflow? defaultValue]) {
    return parseTextOverflow(get(propertyName), defaultValue);
  }

  TextDecorationStyle? getTextDecorationStyle(String propertyName,
      [TextDecorationStyle? defaultValue]) {
    return parseTextDecorationStyle(get(propertyName), defaultValue);
  }

  TextCapitalization? getTextCapitalization(String propertyName,
      [TextCapitalization? defaultValue]) {
    return parseTextCapitalization(get(propertyName), defaultValue);
  }

  TextBaseline? getTextBaseline(String propertyName,
      [TextBaseline? defaultValue]) {
    return parseTextBaseline(get(propertyName), defaultValue);
  }

  WidgetStateProperty<TextStyle?>? getWidgetStateTextStyle(
      String propertyName, ThemeData theme,
      {TextStyle? defaultTextStyle,
      WidgetStateProperty<TextStyle?>? defaultValue}) {
    return parseWidgetStateTextStyle(get(propertyName), theme,
        defaultTextStyle: defaultTextStyle, defaultValue: defaultValue);
  }
}

extension InputFormatterParsers on Control {
  FilteringTextInputFormatter? getInputFilter(String propertyName,
      [FilteringTextInputFormatter? defaultValue]) {
    return parseInputFilter(get(propertyName), defaultValue);
  }
}

extension DurationParsers on Control {
  Duration? getDuration(String propertyName, [Duration? defaultValue]) {
    return parseDuration(get(propertyName), defaultValue);
  }
}

extension TooltipParsers on Control {
  TooltipTriggerMode? getTooltipTriggerMode(String propertyName,
      [TooltipTriggerMode? defaultValue]) {
    return parseTooltipTriggerMode(get(propertyName), defaultValue);
  }
}

extension TransformParsers on Control {
  RotationDetails? getRotationDetails(String propertyName,
      [RotationDetails? defaultValue]) {
    return parseRotationDetails(get(propertyName), defaultValue);
  }

  ScaleDetails? getScale(String propertyName, [ScaleDetails? defaultValue]) {
    return parseScale(get(propertyName), defaultValue);
  }

  Offset? getOffset(String propertyName, [Offset? defaultValue]) {
    return parseOffset(get(propertyName), defaultValue);
  }

  List<Offset>? getOffsetList(String propertyName,
      [List<Offset>? defaultValue]) {
    return parseOffsetList(get(propertyName), defaultValue);
  }
}

extension ThemeParsers on Control {
  ThemeData getTheme(
      String propertyName, BuildContext context, Brightness? brightness,
      {ThemeData? parentTheme}) {
    return parseTheme(get(propertyName), context, brightness,
        parentTheme: parentTheme);
  }

  ThemeMode? getThemeMode(String propertyName, [ThemeMode? defaultValue]) {
    return parseThemeMode(get(propertyName), defaultValue);
  }

  CupertinoThemeData? getCupertinoTheme(
      String propertyName, BuildContext context, Brightness? brightness,
      {ThemeData? parentTheme}) {
    return parseCupertinoTheme(get(propertyName), context, brightness,
        parentTheme: parentTheme);
  }

  ColorScheme? getColorScheme(String propertyName, ThemeData theme,
      [ColorScheme? defaultValue]) {
    return parseColorScheme(get(propertyName), theme, defaultValue);
  }

  TextTheme? getTextTheme(
      String propertyName, ThemeData theme, TextTheme textTheme,
      [TextTheme? defaultValue]) {
    return parseTextTheme(get(propertyName), theme, textTheme, defaultValue);
  }

  VisualDensity? getVisualDensity(String propertyName,
      [VisualDensity? defaultValue]) {
    return parseVisualDensity(get(propertyName), defaultValue);
  }

  PageTransitionsTheme? getPageTransitionsTheme(String propertyName,
      [PageTransitionsTheme? defaultValue]) {
    return parsePageTransitions(get(propertyName), defaultValue);
  }

  SystemUiOverlayStyleTheme getSystemUiOverlayStyleTheme(
      String propertyName, ThemeData theme, Brightness? brightness) {
    return SystemUiOverlayStyleTheme(
      get(propertyName) != null
          ? parseSystemUiOverlayStyle(get(propertyName), theme, brightness)
          : null,
    );
  }

  ButtonThemeData? getButtonTheme(String propertyName, ThemeData theme,
      [ButtonThemeData? defaultValue]) {
    return parseButtonTheme(get(propertyName), theme, defaultValue);
  }

  ElevatedButtonThemeData? getElevatedButtonTheme(
      String propertyName, ThemeData theme,
      [ElevatedButtonThemeData? defaultValue]) {
    return parseElevatedButtonTheme(get(propertyName), theme, defaultValue);
  }

  OutlinedButtonThemeData? getOutlinedButtonTheme(
      String propertyName, ThemeData theme,
      [OutlinedButtonThemeData? defaultValue]) {
    return parseOutlinedButtonTheme(get(propertyName), theme, defaultValue);
  }

  TextButtonThemeData? getTextButtonTheme(String propertyName, ThemeData theme,
      [TextButtonThemeData? defaultValue]) {
    return parseTextButtonTheme(get(propertyName), theme, defaultValue);
  }

  FilledButtonThemeData? getFilledButtonTheme(
      String propertyName, ThemeData theme,
      [FilledButtonThemeData? defaultValue]) {
    return parseFilledButtonTheme(get(propertyName), theme, defaultValue);
  }

  IconButtonThemeData? getIconButtonTheme(String propertyName, ThemeData theme,
      [IconButtonThemeData? defaultValue]) {
    return parseIconButtonTheme(get(propertyName), theme, defaultValue);
  }

  DataTableThemeData? getDataTableTheme(
      String propertyName, BuildContext context,
      [DataTableThemeData? defaultValue]) {
    return parseDataTableTheme(get(propertyName), context, defaultValue);
  }

  ScrollbarThemeData? getScrollbarTheme(String propertyName, ThemeData theme,
      [ScrollbarThemeData? defaultValue]) {
    return parseScrollBarTheme(get(propertyName), theme, defaultValue);
  }

  TabBarThemeData? getTabBarTheme(String propertyName, ThemeData theme,
      [TabBarThemeData? defaultValue]) {
    return parseTabBarTheme(get(propertyName), theme, defaultValue);
  }

  DialogThemeData? getDialogTheme(String propertyName, ThemeData theme,
      [DialogThemeData? defaultValue]) {
    return parseDialogTheme(get(propertyName), theme, defaultValue);
  }

  BottomSheetThemeData? getBottomSheetTheme(
      String propertyName, ThemeData theme,
      [BottomSheetThemeData? defaultValue]) {
    return parseBottomSheetTheme(get(propertyName), theme, defaultValue);
  }

  CardThemeData? getCardTheme(String propertyName, ThemeData theme,
      [CardThemeData? defaultValue]) {
    return parseCardTheme(get(propertyName), theme, defaultValue);
  }

  ChipThemeData? getChipTheme(String propertyName, ThemeData theme,
      [ChipThemeData? defaultValue]) {
    return parseChipTheme(get(propertyName), theme, defaultValue);
  }

  FloatingActionButtonThemeData? getFloatingActionButtonTheme(
      String propertyName, ThemeData theme,
      [FloatingActionButtonThemeData? defaultValue]) {
    return parseFloatingActionButtonTheme(
        get(propertyName), theme, defaultValue);
  }

  NavigationRailThemeData? getNavigationRailTheme(
      String propertyName, ThemeData theme,
      [NavigationRailThemeData? defaultValue]) {
    return parseNavigationRailTheme(get(propertyName), theme, defaultValue);
  }

  AppBarTheme? getAppBarTheme(String propertyName, ThemeData theme,
      [AppBarTheme? defaultValue]) {
    return parseAppBarTheme(get(propertyName), theme, defaultValue);
  }

  BottomAppBarTheme? getBottomAppBarTheme(String propertyName, ThemeData theme,
      [BottomAppBarTheme? defaultValue]) {
    return parseBottomAppBarTheme(get(propertyName), theme, defaultValue);
  }

  RadioThemeData? getRadioTheme(String propertyName, ThemeData theme,
      [RadioThemeData? defaultValue]) {
    return parseRadioTheme(get(propertyName), theme, defaultValue);
  }

  CheckboxThemeData? getCheckboxTheme(String propertyName, ThemeData theme,
      [CheckboxThemeData? defaultValue]) {
    return parseCheckboxTheme(get(propertyName), theme, defaultValue);
  }

  BadgeThemeData? getBadgeTheme(String propertyName, ThemeData theme,
      [BadgeThemeData? defaultValue]) {
    return parseBadgeTheme(get(propertyName), theme, defaultValue);
  }

  SwitchThemeData? getSwitchTheme(String propertyName, ThemeData theme,
      [SwitchThemeData? defaultValue]) {
    return parseSwitchTheme(get(propertyName), theme, defaultValue);
  }

  DividerThemeData? getDividerTheme(String propertyName, ThemeData theme,
      [DividerThemeData? defaultValue]) {
    return parseDividerTheme(get(propertyName), theme, defaultValue);
  }

  SnackBarThemeData? getSnackBarTheme(String propertyName, ThemeData theme,
      [SnackBarThemeData? defaultValue]) {
    return parseSnackBarTheme(get(propertyName), theme, defaultValue);
  }

  MaterialBannerThemeData? getBannerTheme(String propertyName, ThemeData theme,
      [MaterialBannerThemeData? defaultValue]) {
    return parseBannerTheme(get(propertyName), theme, defaultValue);
  }

  DatePickerThemeData? getDatePickerTheme(String propertyName, ThemeData theme,
      [DatePickerThemeData? defaultValue]) {
    return parseDatePickerTheme(get(propertyName), theme, defaultValue);
  }

  TimePickerThemeData? getTimePickerTheme(String propertyName, ThemeData theme,
      [TimePickerThemeData? defaultValue]) {
    return parseTimePickerTheme(get(propertyName), theme, defaultValue);
  }

  DropdownMenuThemeData? getDropdownMenuTheme(
      String propertyName, ThemeData theme,
      [DropdownMenuThemeData? defaultValue]) {
    return parseDropdownMenuTheme(get(propertyName), theme, defaultValue);
  }

  ListTileThemeData? getListTileTheme(String propertyName, ThemeData theme,
      [ListTileThemeData? defaultValue]) {
    return parseListTileTheme(get(propertyName), theme, defaultValue);
  }

  TooltipThemeData? getTooltipTheme(String propertyName, BuildContext context,
      [TooltipThemeData? defaultValue]) {
    return parseTooltipTheme(get(propertyName), context, defaultValue);
  }

  ExpansionTileThemeData? getExpansionTileTheme(
      String propertyName, ThemeData theme,
      [ExpansionTileThemeData? defaultValue]) {
    return parseExpansionTileTheme(get(propertyName), theme, defaultValue);
  }

  SliderThemeData? getSliderTheme(String propertyName, ThemeData theme,
      [SliderThemeData? defaultValue]) {
    return parseSliderTheme(get(propertyName), theme, defaultValue);
  }

  ProgressIndicatorThemeData? getProgressIndicatorTheme(
      String propertyName, ThemeData theme,
      [ProgressIndicatorThemeData? defaultValue]) {
    return parseProgressIndicatorTheme(get(propertyName), theme, defaultValue);
  }

  PopupMenuThemeData? getPopupMenuTheme(String propertyName, ThemeData theme,
      [PopupMenuThemeData? defaultValue]) {
    return parsePopupMenuTheme(get(propertyName), theme, defaultValue);
  }

  SearchBarThemeData? getSearchBarTheme(String propertyName, ThemeData theme,
      [SearchBarThemeData? defaultValue]) {
    return parseSearchBarTheme(get(propertyName), theme, defaultValue);
  }

  SearchViewThemeData? getSearchViewTheme(String propertyName, ThemeData theme,
      [SearchViewThemeData? defaultValue]) {
    return parseSearchViewTheme(get(propertyName), theme, defaultValue);
  }

  NavigationDrawerThemeData? getNavigationDrawerTheme(
      String propertyName, ThemeData theme,
      [NavigationDrawerThemeData? defaultValue]) {
    return parseNavigationDrawerTheme(get(propertyName), theme, defaultValue);
  }

  NavigationBarThemeData? getNavigationBarTheme(
      String propertyName, ThemeData theme,
      [NavigationBarThemeData? defaultValue]) {
    return parseNavigationBarTheme(get(propertyName), theme, defaultValue);
  }

  SegmentedButtonThemeData? getSegmentedButtonTheme(
      String propertyName, ThemeData theme,
      [SegmentedButtonThemeData? defaultValue]) {
    return parseSegmentedButtonTheme(get(propertyName), theme, defaultValue);
  }

  IconThemeData? getIconTheme(String propertyName, ThemeData theme,
      [IconThemeData? defaultValue]) {
    return parseIconTheme(get(propertyName), theme, defaultValue);
  }
}

extension UserFontParsers on Control {
  Map<String, String>? getFonts(String propertyName,
      [Map<String, String>? defaultValue]) {
    return parseFonts(get(propertyName), defaultValue);
  }
}
