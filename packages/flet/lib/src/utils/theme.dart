import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../models/control.dart';
import '../utils/transforms.dart';
import 'alignment.dart';
import 'borders.dart';
import 'box.dart';
import 'buttons.dart';
import 'colors.dart';
import 'dismissible.dart';
import 'edge_insets.dart';
import 'icons.dart';
import 'locale.dart';
import 'material_state.dart';
import 'menu.dart';
import 'misc.dart';
import 'mouse.dart';
import 'numbers.dart';
import 'overlay_style.dart';
import 'text.dart';
import 'time.dart';
import 'tooltip.dart';

class SystemUiOverlayStyleTheme
    extends ThemeExtension<SystemUiOverlayStyleTheme> {
  final SystemUiOverlayStyle? systemUiOverlayStyle;
  SystemUiOverlayStyleTheme(this.systemUiOverlayStyle);

  @override
  SystemUiOverlayStyleTheme copyWith() {
    return SystemUiOverlayStyleTheme(systemUiOverlayStyle);
  }

  @override
  SystemUiOverlayStyleTheme lerp(
      covariant SystemUiOverlayStyleTheme? other, double t) {
    if (other is! SystemUiOverlayStyleTheme) {
      return this;
    }
    return other;
  }

  @override
  bool operator ==(Object other) {
    return systemUiOverlayStyle ==
        (other as SystemUiOverlayStyleTheme).systemUiOverlayStyle;
  }

  @override
  int get hashCode => systemUiOverlayStyle.hashCode;
}

CupertinoThemeData parseCupertinoTheme(
    dynamic value, BuildContext context, Brightness? brightness,
    {ThemeData? parentTheme}) {
  var theme = parseTheme(value, context, brightness);
  var cupertinoTheme = MaterialBasedCupertinoThemeData(materialTheme: theme);
  return fixCupertinoTheme(cupertinoTheme, theme);
}

CupertinoThemeData fixCupertinoTheme(
    CupertinoThemeData cupertinoTheme, ThemeData theme) {
  var r = cupertinoTheme.copyWith(
      applyThemeToAll: true,
      barBackgroundColor: theme.colorScheme.surface,
      textTheme: cupertinoTheme.textTheme.copyWith(
          navTitleTextStyle: cupertinoTheme.textTheme.navTitleTextStyle
              .copyWith(color: theme.colorScheme.onSurface)));
  return r;
}

Brightness? parseBrightness(String? value, [Brightness? defaultValue]) {
  if (value == null) return defaultValue;
  return Brightness.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ThemeMode? parseThemeMode(String? value, [ThemeMode? defaultValue]) {
  if (value == null) return defaultValue;
  return ThemeMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ThemeData parseTheme(
    dynamic value, BuildContext context, Brightness? brightness,
    {ThemeData? parentTheme}) {
  ThemeData? theme = parentTheme;

  var primarySwatch = parseColor(value?["primary_swatch"], theme);
  var colorSchemeSeed = parseColor(value?["color_scheme_seed"], theme);

  if (colorSchemeSeed != null) primarySwatch = null;

  if (colorSchemeSeed == null && primarySwatch == null) {
    colorSchemeSeed = Colors.blue;
  }

  // create new theme
  theme ??= ThemeData(
    primarySwatch:
        primarySwatch != null ? primarySwatch as MaterialColor : null,
    colorSchemeSeed: colorSchemeSeed,
    fontFamily: value?["font_family"],
    brightness: brightness,
    useMaterial3: value?["use_material3"] ?? primarySwatch == null,
  );

  theme = theme.copyWith(
    extensions: {
      SystemUiOverlayStyleTheme(value?["system_overlay_style"] != null
          ? parseSystemUiOverlayStyle(
              value?["system_overlay_style"], theme, brightness)
          : null)
    },
    visualDensity:
        parseVisualDensity(value?["visual_density"], theme.visualDensity)!,
    pageTransitionsTheme: parsePageTransitions(
        value?["page_transitions"], theme.pageTransitionsTheme)!,
    colorScheme: parseColorScheme(value?["color_scheme"], theme),
    textTheme: parseTextTheme(value?["text_theme"], theme, theme.textTheme),
    primaryTextTheme: parseTextTheme(
        value?["primary_text_theme"], theme, theme.primaryTextTheme),
    scrollbarTheme: parseScrollBarTheme(value?["scrollbar_theme"], theme),
    tabBarTheme: parseTabBarTheme(value?["tabs_theme"], theme),
    splashColor: parseColor(value?["splash_color"], theme),
    highlightColor: parseColor(value?["highlight_color"], theme),
    hoverColor: parseColor(value?["hover_color"], theme),
    focusColor: parseColor(value?["focus_color"], theme),
    unselectedWidgetColor:
        parseColor(value?["unselected_control_color"], theme),
    disabledColor: parseColor(value?["disabled_color"], theme),
    canvasColor: parseColor(value?["canvas_color"], theme),
    scaffoldBackgroundColor: parseColor(value?["scaffold_bgcolor"], theme),
    cardColor: parseColor(value?["card_color"], theme),
    dividerColor: parseColor(value?["divider_color"], theme),
    indicatorColor: parseColor(value?["indicator_color"], theme),
    hintColor: parseColor(value?["hint_color"], theme),
    shadowColor: parseColor(value?["shadow_color"], theme),
    secondaryHeaderColor: parseColor(value?["secondary_header_color"], theme),
    primaryColor: parseColor(value?["primary_color"], theme),
    primaryColorLight: parseColor(value?["primary_color_light"], theme),
    primaryColorDark: parseColor(value?["primary_color_dark"], theme),
    dialogTheme: parseDialogTheme(value?["dialog_theme"], theme),
    bottomSheetTheme:
        parseBottomSheetTheme(value?["bottom_sheet_theme"], theme),
    cardTheme: parseCardTheme(value?["card_theme"], theme),
    chipTheme: parseChipTheme(value?["chip_theme"], theme),
    floatingActionButtonTheme: parseFloatingActionButtonTheme(
        value?["floating_action_button_theme"], theme),
    bottomAppBarTheme:
        parseBottomAppBarTheme(value?["bottom_app_bar_theme"], theme),
    checkboxTheme: parseCheckboxTheme(value?["checkbox_theme"], theme),
    radioTheme: parseRadioTheme(value?["radio_theme"], theme),
    badgeTheme: parseBadgeTheme(value?["badge_theme"], theme),
    switchTheme: parseSwitchTheme(value?["switch_theme"], theme),
    dividerTheme: parseDividerTheme(value?["divider_theme"], theme),
    snackBarTheme: parseSnackBarTheme(value?["snackbar_theme"], theme),
    bannerTheme: parseBannerTheme(value?["banner_theme"], theme),
    datePickerTheme: parseDatePickerTheme(value?["date_picker_theme"], theme),
    navigationRailTheme:
        parseNavigationRailTheme(value?["navigation_rail_theme"], theme),
    appBarTheme: parseAppBarTheme(value?["appbar_theme"], theme),
    dropdownMenuTheme:
        parseDropdownMenuTheme(value?["dropdown_menu_theme"], theme),
    listTileTheme: parseListTileTheme(value?["list_tile_theme"], theme),
    tooltipTheme: parseTooltipTheme(value?["tooltip_theme"], context),
    expansionTileTheme:
        parseExpansionTileTheme(value?["expansion_tile_theme"], theme),
    sliderTheme: parseSliderTheme(value?["slider_theme"], theme),
    progressIndicatorTheme:
        parseProgressIndicatorTheme(value?["progress_indicator_theme"], theme),
    popupMenuTheme: parsePopupMenuTheme(value?["popup_menu_theme"], theme),
    searchBarTheme: parseSearchBarTheme(value?["search_bar_theme"], theme),
    searchViewTheme: parseSearchViewTheme(value?["search_view_theme"], theme),
    navigationDrawerTheme:
        parseNavigationDrawerTheme(value?["navigation_drawer_theme"], theme),
    navigationBarTheme:
        parseNavigationBarTheme(value?["navigation_bar_theme"], theme),
    dataTableTheme: parseDataTableTheme(value?["data_table_theme"], context),
    buttonTheme: parseButtonTheme(value?["button_theme"], theme),
    elevatedButtonTheme:
        parseElevatedButtonTheme(value?["elevated_button_theme"], theme),
    outlinedButtonTheme:
        parseOutlinedButtonTheme(value?["outlined_button_theme"], theme),
    textButtonTheme: parseTextButtonTheme(value?["text_button_theme"], theme),
    filledButtonTheme:
        parseFilledButtonTheme(value?["filled_button_theme"], theme),
    iconButtonTheme: parseIconButtonTheme(value?["icon_button_theme"], theme),
    segmentedButtonTheme:
        parseSegmentedButtonTheme(value?["segmented_button_theme"], theme),
    iconTheme: parseIconTheme(value?["icon_theme"], theme),
    timePickerTheme: parseTimePickerTheme(value?["time_picker_theme"], theme),
  );

  return theme.copyWith(
      cupertinoOverrideTheme: fixCupertinoTheme(
          MaterialBasedCupertinoThemeData(materialTheme: theme), theme));
}

ColorScheme? parseColorScheme(Map<String, dynamic>? value, ThemeData theme,
    [ColorScheme? defaultValue]) {
  if (value == null) return defaultValue;
  return theme.colorScheme.copyWith(
    primary: parseColor(value["primary"], theme),
    onPrimary: parseColor(value["on_primary"], theme),
    primaryContainer: parseColor(value["primary_container"], theme),
    onPrimaryContainer: parseColor(value["on_primary_container"], theme),
    secondary: parseColor(value["secondary"], theme),
    onSecondary: parseColor(value["on_secondary"], theme),
    secondaryContainer: parseColor(value["secondary_container"], theme),
    onSecondaryContainer: parseColor(value["on_secondary_container"], theme),
    tertiary: parseColor(value["tertiary"], theme),
    onTertiary: parseColor(value["on_tertiary"], theme),
    tertiaryContainer: parseColor(value["tertiary_container"], theme),
    onTertiaryContainer: parseColor(value["on_tertiary_container"], theme),
    error: parseColor(value["error"], theme),
    onError: parseColor(value["on_error"], theme),
    errorContainer: parseColor(value["error_container"], theme),
    onErrorContainer: parseColor(value["on_error_container"], theme),
    surface: parseColor(value["surface"], theme),
    onSurface: parseColor(value["on_surface"], theme),
    surfaceContainerHighest: parseColor(value["surface_variant"], theme),
    onSurfaceVariant: parseColor(value["on_surface_variant"], theme),
    outline: parseColor(value["outline"], theme),
    outlineVariant: parseColor(value["outline_variant"], theme),
    shadow: parseColor(value["shadow"], theme),
    scrim: parseColor(value["scrim"], theme),
    inverseSurface: parseColor(value["inverse_surface"], theme),
    onInverseSurface: parseColor(value["on_inverse_surface"], theme),
    inversePrimary: parseColor(value["inverse_primary"], theme),
    surfaceTint: parseColor(value["surface_tint"], theme),
    onPrimaryFixed: parseColor(value["on_primary_fixed"], theme),
    onSecondaryFixed: parseColor(value["on_secondary_fixed"], theme),
    onTertiaryFixed: parseColor(value["on_tertiary_fixed"], theme),
    onPrimaryFixedVariant: parseColor(value["on_primary_fixed_variant"], theme),
    onSecondaryFixedVariant:
        parseColor(value["on_secondary_fixed_variant"], theme),
    onTertiaryFixedVariant:
        parseColor(value["on_tertiary_fixed_variant"], theme),
    primaryFixed: parseColor(value["primary_fixed"], theme),
    secondaryFixed: parseColor(value["secondary_fixed"], theme),
    tertiaryFixed: parseColor(value["tertiary_fixed"], theme),
    primaryFixedDim: parseColor(value["primary_fixed_dim"], theme),
    secondaryFixedDim: parseColor(value["secondary_fixed_dim"], theme),
    surfaceBright: parseColor(value["surface_bright"], theme),
    surfaceContainer: parseColor(value["surface_container"], theme),
    surfaceContainerHigh: parseColor(value["surface_container_high"], theme),
    surfaceContainerLow: parseColor(value["surface_container_low"], theme),
    surfaceContainerLowest:
        parseColor(value["surface_container_lowest"], theme),
    surfaceDim: parseColor(value["surface_dim"], theme),
    tertiaryFixedDim: parseColor(value["tertiary_fixed_dim"], theme),
  );
}

TextTheme? parseTextTheme(
    Map<String, dynamic>? value, ThemeData theme, TextTheme textTheme,
    [TextTheme? defaultValue]) {
  if (value == null) return defaultValue;

  return textTheme.copyWith(
    bodyLarge: parseTextStyle(value["body_large"], theme),
    bodyMedium: parseTextStyle(value["body_medium"], theme),
    bodySmall: parseTextStyle(value["body_small"], theme),
    displayLarge: parseTextStyle(value["display_large"], theme),
    displayMedium: parseTextStyle(value["display_medium"], theme),
    displaySmall: parseTextStyle(value["display_small"], theme),
    headlineLarge: parseTextStyle(value["headline_large"], theme),
    headlineMedium: parseTextStyle(value["headline_medium"], theme),
    headlineSmall: parseTextStyle(value["headline_small"], theme),
    labelLarge: parseTextStyle(value["label_large"], theme),
    labelMedium: parseTextStyle(value["label_medium"], theme),
    labelSmall: parseTextStyle(value["label_small"], theme),
    titleLarge: parseTextStyle(value["title_large"], theme),
    titleMedium: parseTextStyle(value["title_medium"], theme),
    titleSmall: parseTextStyle(value["title_small"], theme),
  );
}

ButtonThemeData? parseButtonTheme(Map<String, dynamic>? value, ThemeData theme,
    [ButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.buttonTheme.copyWith(
    buttonColor: parseColor(value["button_color"], theme),
    disabledColor: parseColor(value["disabled_color"], theme),
    hoverColor: parseColor(value["hover_color"], theme),
    focusColor: parseColor(value["focus_color"], theme),
    highlightColor: parseColor(value["highlight_color"], theme),
    splashColor: parseColor(value["splash_color"], theme),
    colorScheme: parseColorScheme(value["color_scheme"], theme),
    alignedDropdown: parseBool(value["aligned_dropdown"]),
    height: parseDouble(value["height"]),
    minWidth: parseDouble(value["min_width"]),
    shape: parseShape(value["shape"], theme),
    padding: parsePadding(value["padding"]),
  );
}

ElevatedButtonThemeData? parseElevatedButtonTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [ElevatedButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
    iconColor: parseColor(value["icon_color"], theme),
    foregroundColor: parseColor(value["foreground_color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    disabledBackgroundColor: parseColor(value["disabled_bgcolor"], theme),
    disabledForegroundColor:
        parseColor(value["disabled_foreground_color"], theme),
    disabledIconColor: parseColor(value["disabled_icon_color"], theme),
    overlayColor: parseColor(value["overlay_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    elevation: parseDouble(value["elevation"]),
    padding: parsePadding(value["padding"]),
    enableFeedback: parseBool(value["enable_feedback"]),
    disabledMouseCursor: parseMouseCursor(value["disabled_mouse_cursor"]),
    enabledMouseCursor: parseMouseCursor(value["enabled_mouse_cursor"]),
    shape: parseShape(value["shape"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
    visualDensity: parseVisualDensity(value["visual_density"]),
    side: parseBorderSide(value["border_side"], theme),
    animationDuration: parseDuration(value["animation_duration"]),
    alignment: parseAlignment(value["alignment"]),
    iconSize: parseDouble(value["icon_size"]),
    fixedSize: parseSize(value["fixed_size"]),
    maximumSize: parseSize(value["maximum_size"]),
    minimumSize: parseSize(value["minimum_size"]),
  ));
}

OutlinedButtonThemeData? parseOutlinedButtonTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [OutlinedButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
    iconColor: parseColor(value["icon_color"], theme),
    foregroundColor: parseColor(value["foreground_color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    disabledBackgroundColor: parseColor(value["disabled_bgcolor"], theme),
    disabledForegroundColor:
        parseColor(value["disabled_foreground_color"], theme),
    disabledIconColor: parseColor(value["disabled_icon_color"], theme),
    overlayColor: parseColor(value["overlay_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    elevation: parseDouble(value["elevation"]),
    padding: parsePadding(value["padding"]),
    enableFeedback: parseBool(value["enable_feedback"]),
    disabledMouseCursor: parseMouseCursor(value["disabled_mouse_cursor"]),
    enabledMouseCursor: parseMouseCursor(value["enabled_mouse_cursor"]),
    shape: parseShape(value["shape"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
    visualDensity: parseVisualDensity(value["visual_density"]),
    side: parseBorderSide(value["border_side"], theme),
    animationDuration: parseDuration(value["animation_duration"]),
    alignment: parseAlignment(value["alignment"]),
    iconSize: parseDouble(value["icon_size"]),
    fixedSize: parseSize(value["fixed_size"]),
    maximumSize: parseSize(value["maximum_size"]),
    minimumSize: parseSize(value["minimum_size"]),
  ));
}

TextButtonThemeData? parseTextButtonTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [TextButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return TextButtonThemeData(
      style: TextButton.styleFrom(
    iconColor: parseColor(value["icon_color"], theme),
    foregroundColor: parseColor(value["foreground_color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    disabledBackgroundColor: parseColor(value["disabled_bgcolor"], theme),
    disabledForegroundColor:
        parseColor(value["disabled_foreground_color"], theme),
    disabledIconColor: parseColor(value["disabled_icon_color"], theme),
    overlayColor: parseColor(value["overlay_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    elevation: parseDouble(value["elevation"]),
    padding: parsePadding(value["padding"]),
    enableFeedback: parseBool(value["enable_feedback"]),
    disabledMouseCursor: parseMouseCursor(value["disabled_mouse_cursor"]),
    enabledMouseCursor: parseMouseCursor(value["enabled_mouse_cursor"]),
    shape: parseShape(value["shape"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
    visualDensity: parseVisualDensity(value["visual_density"]),
    side: parseBorderSide(value["border_side"], theme),
    animationDuration: parseDuration(value["animation_duration"]),
    alignment: parseAlignment(value["alignment"]),
    iconSize: parseDouble(value["icon_size"]),
    fixedSize: parseSize(value["fixed_size"]),
    maximumSize: parseSize(value["maximum_size"]),
    minimumSize: parseSize(value["minimum_size"]),
  ));
}

FilledButtonThemeData? parseFilledButtonTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [FilledButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return FilledButtonThemeData(
      style: FilledButton.styleFrom(
    iconColor: parseColor(value["icon_color"], theme),
    foregroundColor: parseColor(value["foreground_color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    disabledBackgroundColor: parseColor(value["disabled_bgcolor"], theme),
    disabledForegroundColor:
        parseColor(value["disabled_foreground_color"], theme),
    disabledIconColor: parseColor(value["disabled_icon_color"], theme),
    overlayColor: parseColor(value["overlay_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    elevation: parseDouble(value["elevation"]),
    padding: parsePadding(value["padding"]),
    enableFeedback: parseBool(value["enable_feedback"]),
    disabledMouseCursor: parseMouseCursor(value["disabled_mouse_cursor"]),
    enabledMouseCursor: parseMouseCursor(value["enabled_mouse_cursor"]),
    shape: parseShape(value["shape"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
    visualDensity: parseVisualDensity(value["visual_density"]),
    side: parseBorderSide(value["border_side"], theme),
    animationDuration: parseDuration(value["animation_duration"]),
    alignment: parseAlignment(value["alignment"]),
    iconSize: parseDouble(value["icon_size"]),
    fixedSize: parseSize(value["fixed_size"]),
    maximumSize: parseSize(value["maximum_size"]),
    minimumSize: parseSize(value["minimum_size"]),
  ));
}

IconButtonThemeData? parseIconButtonTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [IconButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return IconButtonThemeData(
      style: IconButton.styleFrom(
    foregroundColor: parseColor(value["foreground_color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    disabledBackgroundColor: parseColor(value["disabled_bgcolor"], theme),
    disabledForegroundColor:
        parseColor(value["disabled_foreground_color"], theme),
    overlayColor: parseColor(value["overlay_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    focusColor: parseColor(value["focus_color"], theme),
    highlightColor: parseColor(value["highlight_color"], theme),
    hoverColor: parseColor(value["hover_color"], theme),
    elevation: parseDouble(value["elevation"]),
    padding: parsePadding(value["padding"]),
    enableFeedback: parseBool(value["enable_feedback"]),
    disabledMouseCursor: parseMouseCursor(value["disabled_mouse_cursor"]),
    enabledMouseCursor: parseMouseCursor(value["enabled_mouse_cursor"]),
    shape: parseShape(value["shape"], theme),
    visualDensity: parseVisualDensity(value["visual_density"]),
    side: parseBorderSide(value["border_side"], theme),
    animationDuration: parseDuration(value["animation_duration"]),
    alignment: parseAlignment(value["alignment"]),
    iconSize: parseDouble(value["icon_size"]),
    fixedSize: parseSize(value["fixed_size"]),
    maximumSize: parseSize(value["maximum_size"]),
    minimumSize: parseSize(value["minimum_size"]),
  ));
}

DataTableThemeData? parseDataTableTheme(
    Map<String, dynamic>? value, BuildContext context,
    [DataTableThemeData? defaultValue]) {
  if (value == null) return defaultValue;
  var theme = Theme.of(context);

  return theme.dataTableTheme.copyWith(
    checkboxHorizontalMargin: parseDouble(value["checkbox_horizontal_margin"]),
    columnSpacing: parseDouble(value["column_spacing"]),
    dataRowMaxHeight: parseDouble(value["data_row_max_height"]),
    dataRowMinHeight: parseDouble(value["data_row_min_height"]),
    dataRowColor: parseWidgetStateColor(value["data_row_color"], theme),
    dataTextStyle: parseTextStyle(value["data_text_style"], theme),
    dividerThickness: parseDouble(value["divider_thickness"]),
    horizontalMargin: parseDouble(value["horizontal_margin"]),
    headingTextStyle: parseTextStyle(value["heading_text_style"], theme),
    headingRowColor: parseWidgetStateColor(value["heading_row_color"], theme),
    headingRowHeight: parseDouble(value["heading_row_height"]),
    dataRowCursor: parseWidgetStateMouseCursor(value["data_row_cursor"]),
    decoration: parseBoxDecoration(value["decoration"], context),
    headingRowAlignment: parseMainAxisAlignment(value["heading_row_alignment"]),
    headingCellCursor:
        parseWidgetStateMouseCursor(value["heading_cell_cursor"]),
  );
}

ScrollbarThemeData? parseScrollBarTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [ScrollbarThemeData? defaultValue]) {
  if (value == null) return defaultValue;
  return theme.scrollbarTheme.copyWith(
    trackVisibility: parseWidgetStateBool(value["track_visibility"]),
    trackColor: parseWidgetStateColor(value["track_color"], theme),
    trackBorderColor: parseWidgetStateColor(value["track_border_color"], theme),
    thumbVisibility: parseWidgetStateBool(value["thumb_visibility"]),
    thumbColor: parseWidgetStateColor(value["thumb_color"], theme),
    thickness: parseWidgetStateDouble(value["thickness"]),
    radius: parseRadius(value["radius"]),
    crossAxisMargin: parseDouble(value["cross_axis_margin"]),
    mainAxisMargin: parseDouble(value["main_axis_margin"]),
    minThumbLength: parseDouble(value["min_thumb_length"]),
    interactive: parseBool(value["interactive"]),
  );
}

TabBarThemeData? parseTabBarTheme(Map<String, dynamic>? value, ThemeData theme,
    [TabBarThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  var indicatorColor = parseColor(value["indicator_color"], theme);

  return theme.tabBarTheme.copyWith(
      overlayColor: parseWidgetStateColor(value["overlay_color"], theme),
      dividerColor: parseColor(value["divider_color"], theme),
      indicatorColor: indicatorColor,
      labelColor: parseColor(value["label_color"], theme),
      unselectedLabelColor: parseColor(value["unselected_label_color"], theme),
      indicatorSize: parseBool(value["indicator_tab_size"], false)!
          ? TabBarIndicatorSize.tab
          : TabBarIndicatorSize.label,
      indicator: value["indicator_border_radius"] != null ||
              value["indicator_border_side"] != null ||
              value["indicator_padding"] != null
          ? UnderlineTabIndicator(
              borderRadius: parseBorderRadius(
                  value["indicator_border_radius"],
                  const BorderRadius.only(
                      topLeft: Radius.circular(2),
                      topRight: Radius.circular(2)))!,
              borderSide: parseBorderSide(value["indicator_border_side"], theme,
                  defaultSideColor: indicatorColor,
                  defaultValue: BorderSide(
                      width: 2.0,
                      color: indicatorColor ?? theme.colorScheme.primary))!,
              insets:
                  parsePadding(value["indicator_padding"], EdgeInsets.zero)!)
          : null,
      mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
      labelPadding: parsePadding(value["label_padding"]),
      dividerHeight: parseDouble(value["divider_height"]),
      labelStyle: parseTextStyle(value["label_text_style"], theme),
      unselectedLabelStyle:
          parseTextStyle(value["unselected_label_text_style"], theme));
}

VisualDensity? parseVisualDensity(String? density,
    [VisualDensity? defaultValue]) {
  switch (density?.toLowerCase()) {
    case "adaptiveplatformdensity":
      return VisualDensity.adaptivePlatformDensity;
    case "comfortable":
      return VisualDensity.comfortable;
    case "compact":
      return VisualDensity.compact;
    case "standard":
      return VisualDensity.standard;
    default:
      return defaultValue;
  }
}

PageTransitionsTheme? parsePageTransitions(Map<String, dynamic>? value,
    [PageTransitionsTheme? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return PageTransitionsTheme(builders: {
    TargetPlatform.android: parseTransitionsBuilder(
        value["android"], const FadeUpwardsPageTransitionsBuilder())!,
    TargetPlatform.iOS: parseTransitionsBuilder(
        value["ios"], const CupertinoPageTransitionsBuilder())!,
    TargetPlatform.linux: parseTransitionsBuilder(
        value["linux"], const ZoomPageTransitionsBuilder())!,
    TargetPlatform.macOS: parseTransitionsBuilder(
        value["macos"], const ZoomPageTransitionsBuilder())!,
    TargetPlatform.windows: parseTransitionsBuilder(
        value["windows"], const ZoomPageTransitionsBuilder())!,
  });
}

DialogThemeData? parseDialogTheme(Map<String, dynamic>? value, ThemeData theme,
    [DialogThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.dialogTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    iconColor: parseColor(value["icon_color"], theme),
    elevation: parseDouble(value["elevation"]),
    shape: parseShape(value["shape"], theme),
    titleTextStyle: parseTextStyle(value["title_text_style"], theme),
    contentTextStyle: parseTextStyle(value["content_text_style"], theme),
    alignment: parseAlignment(value["alignment"]),
    actionsPadding: parsePadding(value["actions_padding"]),
    clipBehavior: parseClip(value["clip_behavior"]),
    barrierColor: parseColor(value["barrier_color"], theme),
    insetPadding: parsePadding(value["inset_padding"]),
  );
}

BottomSheetThemeData? parseBottomSheetTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [BottomSheetThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.bottomSheetTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    dragHandleColor: parseColor(value["drag_handle_color"], theme),
    elevation: parseDouble(value["elevation"]),
    shape: parseShape(value["shape"], theme),
    showDragHandle: parseBool(value["show_drag_handle"]),
    modalBackgroundColor: parseColor(value["modal_bgcolor"], theme),
    modalElevation: parseDouble(value["modal_elevation"]),
    clipBehavior: parseClip(value["clip_behavior"]),
    constraints: parseBoxConstraints(value["size_constraints"]),
    modalBarrierColor: parseColor(value["modal_barrier_color"], theme),
  );
}

CardThemeData? parseCardTheme(Map<String, dynamic>? value, ThemeData theme,
    [CardThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.cardTheme.copyWith(
      color: parseColor(value["color"], theme),
      shadowColor: parseColor(value["shadow_color"], theme),
      surfaceTintColor: parseColor(value["surface_tint_color"], theme),
      elevation: parseDouble(value["elevation"]),
      shape: parseShape(value["shape"], theme),
      clipBehavior: parseClip(value["clip_behavior"]),
      margin: parseMargin(value["margin"]));
}

ChipThemeData? parseChipTheme(Map<String, dynamic>? value, ThemeData theme,
    [ChipThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.chipTheme.copyWith(
    color: parseWidgetStateColor(value["color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    elevation: parseDouble(value["elevation"]),
    shape: parseShape(value["shape"], theme),
    padding: parsePadding(value["padding"]),
    labelPadding: parsePadding(value["label_padding"]),
    labelStyle: parseTextStyle(value["label_text_style"], theme),
    secondaryLabelStyle:
        parseTextStyle(value["secondary_label_text_style"], theme),
    disabledColor: parseColor(value["disabled_color"], theme),
    selectedColor: parseColor(value["selected_color"], theme),
    checkmarkColor: parseColor(value["check_color"], theme),
    deleteIconColor: parseColor(value["delete_icon_color"], theme),
    side: parseBorderSide(value["border_side"], theme),
    secondarySelectedColor:
        parseColor(value["secondary_selected_color"], theme),
    brightness: parseBrightness(value["brightness"]),
    selectedShadowColor: parseColor(value["selected_shadow_color"], theme),
    showCheckmark: parseBool(value["show_checkmark"]),
    pressElevation: parseDouble(value["click_elevation"]),
    avatarBoxConstraints: parseBoxConstraints(value["avatar_constraints"]),
    deleteIconBoxConstraints:
        parseBoxConstraints(value["delete_icon_size_constraints"]),
  );
}

FloatingActionButtonThemeData? parseFloatingActionButtonTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [FloatingActionButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.floatingActionButtonTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    hoverColor: parseColor(value["hover_color"], theme),
    focusColor: parseColor(value["focus_color"], theme),
    foregroundColor: parseColor(value["foreground_color"], theme),
    splashColor: parseColor(value["splash_color"], theme),
    elevation: parseDouble(value["elevation"]),
    focusElevation: parseDouble(value["focus_elevation"]),
    hoverElevation: parseDouble(value["hover_elevation"]),
    highlightElevation: parseDouble(value["highlight_elevation"]),
    disabledElevation: parseDouble(value["disabled_elevation"]),
    shape: parseShape(value["shape"], theme),
    enableFeedback: parseBool(value["enable_feedback"]),
    extendedPadding: parsePadding(value["extended_padding"]),
    extendedTextStyle: parseTextStyle(value["extended_text_style"], theme),
    extendedIconLabelSpacing: parseDouble(value["extended_icon_label_spacing"]),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
    iconSize: parseDouble(value["icon_size"]),
    extendedSizeConstraints:
        parseBoxConstraints(value["extended_size_constraints"]),
    sizeConstraints: parseBoxConstraints(value["size_constraints"]),
    smallSizeConstraints: parseBoxConstraints(value["small_size_constraints"]),
    largeSizeConstraints: parseBoxConstraints(value["large_size_constraints"]),
  );
}

NavigationRailThemeData? parseNavigationRailTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [NavigationRailThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.navigationRailTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    elevation: parseDouble(value["elevation"]),
    indicatorColor: parseColor(value["indicator_color"], theme),
    unselectedLabelTextStyle:
        parseTextStyle(value["unselected_label_text_style"], theme),
    selectedLabelTextStyle:
        parseTextStyle(value["selected_label_text_style"], theme),
    minWidth: parseDouble(value["min_width"]),
    labelType: parseNavigationRailLabelType(value["label_type"]),
    groupAlignment: parseDouble(value["group_alignment"]),
    indicatorShape: parseShape(value["indicator_shape"], theme),
    minExtendedWidth: parseDouble(value["min_extended_width"]),
    useIndicator: parseBool(value["use_indicator"]),
  );
}

AppBarTheme? parseAppBarTheme(Map<String, dynamic>? value, ThemeData theme,
    [AppBarTheme? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.appBarTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    color: parseColor(value["color"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    foregroundColor: parseColor(value["foreground_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    titleTextStyle: parseTextStyle(value["title_text_style"], theme),
    toolbarTextStyle: parseTextStyle(value["toolbar_text_style"], theme),
    shape: parseShape(value["shape"], theme),
    elevation: parseDouble(value["elevation"]),
    centerTitle: parseBool(value["center_title"]),
    titleSpacing: parseDouble(value["title_spacing"]),
    scrolledUnderElevation: parseDouble(value["scroll_elevation"]),
    toolbarHeight: parseDouble(value["toolbar_height"]),
    actionsPadding: parsePadding(value["actions_padding"]),
  );
}

BottomAppBarTheme? parseBottomAppBarTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [BottomAppBarTheme? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.bottomAppBarTheme.copyWith(
    color: parseColor(value["color"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    elevation: parseDouble(value["elevation"]),
    height: parseDouble(value["height"]),
    padding: parsePadding(value["padding"]),
    shape: parseNotchedShape(value["shape"]),
  );
}

RadioThemeData? parseRadioTheme(Map<String, dynamic>? value, ThemeData theme,
    [RadioThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.radioTheme.copyWith(
    fillColor: parseWidgetStateColor(value["fill_color"], theme),
    splashRadius: parseDouble(value["splash_radius"]),
    overlayColor: parseWidgetStateColor(value["overlay_color"], theme),
    visualDensity: parseVisualDensity(value["visual_density"]),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
  );
}

CheckboxThemeData? parseCheckboxTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [CheckboxThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.checkboxTheme.copyWith(
    fillColor: parseWidgetStateColor(value["fill_color"], theme),
    splashRadius: parseDouble(value["splash_radius"]),
    overlayColor: parseWidgetStateColor(value["overlay_color"], theme),
    visualDensity: parseVisualDensity(value["visual_density"]),
    checkColor: parseWidgetStateColor(value["check_color"], theme),
    side: parseBorderSide(value["border_side"], theme),
    shape: parseShape(value["shape"], theme),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
  );
}

BadgeThemeData? parseBadgeTheme(Map<String, dynamic>? value, ThemeData theme,
    [BadgeThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.badgeTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
    padding: parsePadding(value["padding"]),
    alignment: parseAlignment(value["alignment"]),
    textColor: parseColor(value["text_color"], theme),
    offset: parseOffset(value["offset"]),
    smallSize: parseDouble(value["small_size"]),
    largeSize: parseDouble(value["large_size"]),
  );
}

SwitchThemeData? parseSwitchTheme(Map<String, dynamic>? value, ThemeData theme,
    [SwitchThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.switchTheme.copyWith(
    thumbColor: parseWidgetStateColor(value["thumb_color"], theme),
    trackColor: parseWidgetStateColor(value["track_color"], theme),
    overlayColor: parseWidgetStateColor(value["overlay_color"], theme),
    splashRadius: parseDouble(value["splash_radius"]),
    thumbIcon: parseWidgetStateIcon(value["thumb_icon"], theme),
    trackOutlineColor:
        parseWidgetStateColor(value["track_outline_color"], theme),
    trackOutlineWidth: parseWidgetStateDouble(value["track_outline_width"]),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
    padding: parsePadding(value["padding"]),
  );
}

DividerThemeData? parseDividerTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [DividerThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.dividerTheme.copyWith(
    color: parseColor(value["color"], theme),
    space: parseDouble(value["space"]),
    thickness: parseDouble(value["thickness"]),
    indent: parseDouble(value["leading_indent"]),
    endIndent: parseDouble(value["trailing_indent"]),
  );
}

SnackBarThemeData? parseSnackBarTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [SnackBarThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.snackBarTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    actionTextColor: parseColor(value["action_text_color"], theme),
    actionBackgroundColor: parseColor(value["action_bgcolor"], theme),
    closeIconColor: parseColor(value["close_icon_color"], theme),
    disabledActionTextColor:
        parseColor(value["disabled_action_text_color"], theme),
    disabledActionBackgroundColor:
        parseColor(value["disabled_action_bgcolor"], theme),
    elevation: parseDouble(value["elevation"]),
    shape: parseShape(value["shape"], theme),
    behavior: parseSnackBarBehavior(value["behavior"]),
    contentTextStyle: parseTextStyle(value["content_text_style"], theme),
    width: parseDouble(value["width"]),
    insetPadding: parsePadding(value["inset_padding"]),
    dismissDirection: parseDismissDirection(value["dismiss_direction"]),
    showCloseIcon: parseBool(value["show_close_icon"]),
    actionOverflowThreshold: parseDouble(value["action_overflow_threshold"]),
  );
}

MaterialBannerThemeData? parseBannerTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [MaterialBannerThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.bannerTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    elevation: parseDouble(value["elevation"]),
    dividerColor: parseColor(value["divider_color"], theme),
    padding: parsePadding(value["padding"]),
    leadingPadding: parsePadding(value["leading_padding"]),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    contentTextStyle: parseTextStyle(value["content_text_style"], theme),
  );
}

DatePickerThemeData? parseDatePickerTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [DatePickerThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.datePickerTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    elevation: parseDouble(value["elevation"]),
    dividerColor: parseColor(value["divider_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    cancelButtonStyle: parseButtonStyle(value["cancel_button_style"], theme),
    confirmButtonStyle: parseButtonStyle(value["confirm_button_style"], theme),
    dayBackgroundColor: parseWidgetStateColor(value["day_bgcolor"], theme),
    yearStyle: parseTextStyle(value["year_text_style"], theme),
    dayStyle: parseTextStyle(value["day_text_style"], theme),
    shape: parseShape(value["shape"], theme),
    dayOverlayColor: parseWidgetStateColor(value["day_overlay_color"], theme),
    headerBackgroundColor: parseColor(value["header_bgcolor"], theme),
    dayForegroundColor:
        parseWidgetStateColor(value["day_foreground_color"], theme),
    rangePickerElevation: parseDouble(value["range_picker_elevation"]),
    todayBackgroundColor: parseWidgetStateColor(value["today_bgcolor"], theme),
    headerForegroundColor: parseColor(value["header_foreground_color"], theme),
    headerHeadlineStyle:
        parseTextStyle(value["header_headline_text_style"], theme),
    headerHelpStyle: parseTextStyle(value["header_help_text_style"], theme),
    rangePickerBackgroundColor:
        parseColor(value["range_picker_bgcolor"], theme),
    rangePickerHeaderBackgroundColor:
        parseColor(value["range_picker_header_bgcolor"], theme),
    rangePickerHeaderForegroundColor:
        parseColor(value["range_picker_header_foreground_color"], theme),
    rangePickerShadowColor:
        parseColor(value["range_picker_shadow_color"], theme),
    todayForegroundColor:
        parseWidgetStateColor(value["today_foreground_color"], theme),
    rangePickerShape: parseShape(value["range_picker_shape"], theme),
    rangePickerHeaderHelpStyle:
        parseTextStyle(value["range_picker_header_help_text_style"], theme),
    rangePickerHeaderHeadlineStyle:
        parseTextStyle(value["range_picker_header_headline_text_style"], theme),
    rangePickerSurfaceTintColor:
        parseColor(value["range_picker_surface_tint_color"], theme),
    rangeSelectionBackgroundColor:
        parseColor(value["range_selection_bgcolor"], theme),
    rangeSelectionOverlayColor:
        parseWidgetStateColor(value["range_selection_overlay_color"], theme),
    todayBorder: parseBorderSide(value["today_border_side"], theme),
    yearBackgroundColor: parseWidgetStateColor(value["year_bgcolor"], theme),
    yearForegroundColor:
        parseWidgetStateColor(value["year_foreground_color"], theme),
    yearOverlayColor: parseWidgetStateColor(value["year_overlay_color"], theme),
    weekdayStyle: parseTextStyle(value["weekday_text_style"], theme),
    dayShape: parseWidgetStateOutlinedBorder(value["day_shape"], theme),
    locale: parseLocale(value["locale"]),
  );
}

TimePickerThemeData? parseTimePickerTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [TimePickerThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.timePickerTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    elevation: parseDouble(value["elevation"]),
    padding: parsePadding(value["padding"]),
    shape: parseShape(value["shape"], theme),
    dayPeriodBorderSide:
        parseBorderSide(value["day_period_border_side"], theme),
    dayPeriodButtonStyle:
        parseButtonStyle(value["day_period_button_style"], theme),
    dayPeriodColor: parseColor(value["day_period_color"], theme),
    dayPeriodShape: parseShape(value["day_period_shape"], theme),
    dayPeriodTextColor: parseColor(value["day_period_text_color"], theme),
    dayPeriodTextStyle: parseTextStyle(value["day_period_text_style"], theme),
    dialBackgroundColor: parseColor(value["dial_bgcolor"], theme),
    dialHandColor: parseColor(value["dial_hand_color"], theme),
    dialTextColor: parseColor(value["dial_text_color"], theme),
    dialTextStyle: parseTextStyle(value["dial_text_style"], theme),
    entryModeIconColor: parseColor(value["entry_mode_icon_color"], theme),
    helpTextStyle: parseTextStyle(value["help_text_style"], theme),
    hourMinuteColor: parseColor(value["hour_minute_color"], theme),
    hourMinuteTextColor: parseColor(value["hour_minute_text_color"], theme),
    hourMinuteTextStyle: parseTextStyle(value["hour_minute_text_style"], theme),
    hourMinuteShape: parseShape(value["hour_minute_shape"], theme),
    cancelButtonStyle: parseButtonStyle(value["cancel_button_style"], theme),
    confirmButtonStyle: parseButtonStyle(value["confirm_button_style"], theme),
    timeSelectorSeparatorColor:
        parseWidgetStateColor(value["time_selector_separator_color"], theme),
    timeSelectorSeparatorTextStyle: parseWidgetStateTextStyle(
        value["time_selector_separator_text_style"], theme),
  );
}

DropdownMenuThemeData? parseDropdownMenuTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [DropdownMenuThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.dropdownMenuTheme.copyWith(
    menuStyle: parseMenuStyle(value["menu_style"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
  );
}

ListTileThemeData? parseListTileTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [ListTileThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.listTileTheme.copyWith(
    iconColor: parseColor(value["icon_color"], theme),
    textColor: parseColor(value["text_color"], theme),
    tileColor: parseColor(value["bgcolor"], theme),
    shape: parseShape(value["shape"], theme),
    contentPadding: parsePadding(value["content_padding"]),
    selectedColor: parseColor(value["selected_color"], theme),
    selectedTileColor: parseColor(value["selected_tile_color"], theme),
    isThreeLine: parseBool(value["is_three_line"]),
    visualDensity: parseVisualDensity(value["visual_density"]),
    titleTextStyle: parseTextStyle(value["title_text_style"], theme),
    subtitleTextStyle: parseTextStyle(value["subtitle_text_style"], theme),
    minVerticalPadding: parseDouble(value["min_vertical_padding"]),
    enableFeedback: parseBool(value["enable_feedback"]),
    dense: parseBool(value["dense"]),
    horizontalTitleGap: parseDouble(value["horizontal_spacing"]),
    minLeadingWidth: parseDouble(value["min_leading_width"]),
    leadingAndTrailingTextStyle:
        parseTextStyle(value["leading_and_trailing_text_style"], theme),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
    minTileHeight: parseDouble(value["min_tile_height"]),
  );
}

TooltipThemeData? parseTooltipTheme(
    Map<String, dynamic>? value, BuildContext context,
    [TooltipThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  var theme = Theme.of(context);

  return theme.tooltipTheme.copyWith(
    enableFeedback: parseBool(value["enable_feedback"]),
    height: parseDouble(value["height"]),
    excludeFromSemantics: parseBool(value["exclude_from_semantics"]),
    textStyle: parseTextStyle(value["text_style"], theme),
    preferBelow: parseBool(value["prefer_below"]),
    verticalOffset: parseDouble(value["vertical_offset"]),
    padding: parsePadding(value["padding"]),
    waitDuration: parseDuration(value["wait_duration"]),
    exitDuration: parseDuration(value["exit_duration"]),
    showDuration: parseDuration(value["show_duration"]),
    margin: parseMargin(value["margin"]),
    textAlign: parseTextAlign(value["text_align"]),
    triggerMode: parseTooltipTriggerMode(value["trigger_mode"]),
    decoration: parseBoxDecoration(value["decoration"], context),
  );
}

ExpansionTileThemeData? parseExpansionTileTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [ExpansionTileThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.expansionTileTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    iconColor: parseColor(value["icon_color"], theme),
    textColor: parseColor(value["text_color"], theme),
    collapsedBackgroundColor: parseColor(value["collapsed_bgcolor"], theme),
    collapsedIconColor: parseColor(value["collapsed_icon_color"], theme),
    clipBehavior: parseClip(value["clip_behavior"]),
    collapsedTextColor: parseColor(value["collapsed_text_color"], theme),
    tilePadding: parsePadding(value["tile_padding"]),
    expandedAlignment: parseAlignment(value["expanded_alignment"]),
    childrenPadding: parsePadding(value["controls_padding"]),
  );
}

SliderThemeData? parseSliderTheme(Map<String, dynamic>? value, ThemeData theme,
    [SliderThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.sliderTheme.copyWith(
    activeTrackColor: parseColor(value["active_track_color"], theme),
    inactiveTrackColor: parseColor(value["inactive_track_color"], theme),
    thumbColor: parseColor(value["thumb_color"], theme),
    overlayColor: parseColor(value["overlay_color"], theme),
    valueIndicatorColor: parseColor(value["value_indicator_color"], theme),
    disabledThumbColor: parseColor(value["disabled_thumb_color"], theme),
    valueIndicatorTextStyle:
        parseTextStyle(value["value_indicator_text_style"], theme),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
    activeTickMarkColor: parseColor(value["active_tick_mark_color"], theme),
    disabledActiveTickMarkColor:
        parseColor(value["disabled_active_tick_mark_color"], theme),
    disabledActiveTrackColor:
        parseColor(value["disabled_active_track_color"], theme),
    disabledInactiveTickMarkColor:
        parseColor(value["disabled_inactive_tick_mark_color"], theme),
    disabledInactiveTrackColor:
        parseColor(value["disabled_inactive_track_color"], theme),
    disabledSecondaryActiveTrackColor:
        parseColor(value["disabled_secondary_active_track_color"], theme),
    inactiveTickMarkColor: parseColor(value["inactive_tick_mark_color"], theme),
    overlappingShapeStrokeColor:
        parseColor(value["overlapping_shape_stroke_color"], theme),
    minThumbSeparation: parseDouble(value["min_thumb_separation"]),
    secondaryActiveTrackColor:
        parseColor(value["secondary_active_track_color"], theme),
    trackHeight: parseDouble(value["track_height"]),
    valueIndicatorStrokeColor:
        parseColor(value["value_indicator_stroke_color"], theme),
    allowedInteraction: parseSliderInteraction(value["interaction"]),
    padding: parsePadding(value["padding"]),
    trackGap: parseDouble(value["track_gap"]),
    thumbSize: getWidgetStateProperty<Size?>(
        value["thumb_size"], (jv) => parseSize(jv)),
    // TODO: deprecated in v0.27.0, to be removed in future versions
    year2023: parseBool(value["year_2023"]),
  );
}

ProgressIndicatorThemeData? parseProgressIndicatorTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [ProgressIndicatorThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.progressIndicatorTheme.copyWith(
    color: parseColor(value["color"], theme),
    circularTrackColor: parseColor(value["circular_track_color"], theme),
    linearTrackColor: parseColor(value["linear_track_color"], theme),
    refreshBackgroundColor: parseColor(value["refresh_bgcolor"], theme),
    linearMinHeight: parseDouble(value["linear_min_height"]),
    borderRadius: parseBorderRadius(value["border_radius"]),
    trackGap: parseDouble(value["track_gap"]),
    circularTrackPadding: parsePadding(value["circular_track_padding"]),
    constraints: parseBoxConstraints(value["size_constraints"]),
    stopIndicatorColor: parseColor(value["stop_indicator_color"], theme),
    stopIndicatorRadius: parseDouble(value["stop_indicator_radius"]),
    strokeAlign: parseDouble(value["stroke_align"]),
    strokeCap: parseStrokeCap(value["stroke_cap"]),
    strokeWidth: parseDouble(value["stroke_width"]),
    year2023: parseBool(value["year_2023"]),
  );
}

PopupMenuThemeData? parsePopupMenuTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [PopupMenuThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.popupMenuTheme.copyWith(
    color: parseColor(value["color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    iconColor: parseColor(value["icon_color"], theme),
    textStyle: parseTextStyle(value["text_style"], theme),
    labelTextStyle: parseWidgetStateTextStyle(value["label_text_style"], theme),
    enableFeedback: parseBool(value["enable_feedback"]),
    elevation: parseDouble(value["elevation"]),
    iconSize: parseDouble(value["icon_size"]),
    position: parsePopupMenuPosition(value["menu_position"]),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
    shape: parseShape(value["shape"], theme),
    menuPadding: parsePadding(value["menu_padding"]),
  );
}

SearchBarThemeData? parseSearchBarTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [SearchBarThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.searchBarTheme.copyWith(
    surfaceTintColor: parseWidgetStateColor(value["surface_tint_color"], theme),
    shadowColor: parseWidgetStateColor(value["shadow_color"], theme),
    elevation: parseWidgetStateDouble(value["elevation"]),
    backgroundColor: parseWidgetStateColor(value["bgcolor"], theme),
    overlayColor: parseWidgetStateColor(value["overlay_color"], theme),
    textStyle: parseWidgetStateTextStyle(value["text_style"], theme),
    hintStyle: parseWidgetStateTextStyle(value["hint_style"], theme),
    shape: parseWidgetStateOutlinedBorder(value["shape"], theme),
    textCapitalization: parseTextCapitalization(value["text_capitalization"]),
    padding: parseWidgetStatePadding(value["padding"]),
    constraints: parseBoxConstraints(value["size_constraints"]),
    side: parseWidgetStateBorderSide(value["border_side"], theme),
  );
}

SearchViewThemeData? parseSearchViewTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [SearchViewThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.searchViewTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    dividerColor: parseColor(value["divider_color"], theme),
    elevation: parseDouble(value["elevation"]),
    headerHintStyle: parseTextStyle(value["header_hint_text_style"], theme),
    headerTextStyle: parseTextStyle(value["header_text_style"], theme),
    shape: parseShape(value["shape"], theme),
    side: parseBorderSide(value["border_side"], theme),
    constraints: parseBoxConstraints(value["size_constraints"]),
    headerHeight: parseDouble(value["header_height"]),
    padding: parsePadding(value["padding"]),
    barPadding: parsePadding(value["bar_padding"]),
    shrinkWrap: parseBool(value["shrink_wrap"]),
  );
}

NavigationDrawerThemeData? parseNavigationDrawerTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [NavigationDrawerThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.navigationDrawerTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    indicatorColor: parseColor(value["indicator_color"], theme),
    elevation: parseDouble(value["elevation"]),
    indicatorSize: parseSize(value["indicator_size"]),
    tileHeight: parseDouble(value["tile_height"]),
    labelTextStyle: parseWidgetStateTextStyle(value["label_text_style"], theme),
    indicatorShape: parseShape(value["indicator_shape"], theme),
  );
}

NavigationBarThemeData? parseNavigationBarTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [NavigationBarThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.navigationBarTheme.copyWith(
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadowColor: parseColor(value["shadow_color"], theme),
    surfaceTintColor: parseColor(value["surface_tint_color"], theme),
    indicatorColor: parseColor(value["indicator_color"], theme),
    overlayColor: parseWidgetStateColor(value["overlay_color"], theme),
    elevation: parseDouble(value["elevation"]),
    height: parseDouble(value["height"]),
    labelTextStyle: parseWidgetStateTextStyle(value["label_text_style"], theme),
    indicatorShape: parseShape(value["indicator_shape"], theme),
    labelBehavior:
        parseNavigationDestinationLabelBehavior(value["label_behavior"]),
    labelPadding: parsePadding(value["label_padding"]),
  );
}

SegmentedButtonThemeData? parseSegmentedButtonTheme(
    Map<String, dynamic>? value, ThemeData theme,
    [SegmentedButtonThemeData? defaultValue]) {
  if (value == null) return defaultValue;
  var selectedIcon = parseIcon(value["selected_icon"]);

  return theme.segmentedButtonTheme.copyWith(
    selectedIcon: selectedIcon != null ? Icon(selectedIcon) : null,
    style: parseButtonStyle(value["style"], theme),
  );
}

IconThemeData? parseIconTheme(Map<String, dynamic>? value, ThemeData theme,
    [IconThemeData? defaultValue]) {
  if (value == null) return defaultValue;

  return theme.iconTheme.copyWith(
    color: parseColor(value["color"], theme),
    applyTextScaling: parseBool(value["apply_text_scaling"]),
    fill: parseDouble(value["fill"]),
    opacity: parseDouble(value["opacity"]),
    size: parseDouble(value["size"]),
    opticalSize: parseDouble(value["optical_size"]),
    grade: parseDouble(value["grade"]),
    weight: parseDouble(value["weight"]),
    shadows: parseBoxShadows(value["shadows"], theme),
  );
}

PageTransitionsBuilder? parseTransitionsBuilder(String? value,
    [PageTransitionsBuilder? defaultValue]) {
  var buildersMap = {
    "fadeupwards": const FadeUpwardsPageTransitionsBuilder(),
    "openupwards": const OpenUpwardsPageTransitionsBuilder(),
    "cupertino": const CupertinoPageTransitionsBuilder(),
    "zoom": const ZoomPageTransitionsBuilder(),
    "none": const NoPageTransitionsBuilder(),
    "predictive": const PredictiveBackPageTransitionsBuilder(),
    "fadeforwards": const FadeForwardsPageTransitionsBuilder(),
  };
  return buildersMap[value?.toLowerCase()] ?? defaultValue;
}

class NoPageTransitionsBuilder extends PageTransitionsBuilder {
  const NoPageTransitionsBuilder();

  @override
  Widget buildTransitions<T>(PageRoute<T>? route,
      BuildContext? context,
      Animation<double> animation,
      Animation<double> secondaryAnimation,
      Widget? child) {
    // only return the child without warping it with animations
    return child!;
  }
}

// Trying to fix https://github.com/flutter/flutter/issues/165455
// TODO: remove this when the fix is available
bool themesEqual(ThemeData a, ThemeData b) {
  return mapEquals(a.adaptationMap, b.adaptationMap) &&
      a.applyElevationOverlayColor == b.applyElevationOverlayColor &&
      //a.cupertinoOverrideTheme == b.cupertinoOverrideTheme &&
      mapEquals(a.extensions, b.extensions) &&
      a.inputDecorationTheme == b.inputDecorationTheme &&
      a.materialTapTargetSize == b.materialTapTargetSize &&
      a.pageTransitionsTheme == b.pageTransitionsTheme &&
      a.platform == b.platform &&
      a.scrollbarTheme == b.scrollbarTheme &&
      a.splashFactory == b.splashFactory &&
      a.useMaterial3 == b.useMaterial3 &&
      a.visualDensity == b.visualDensity &&
      // COLOR
      a.canvasColor == b.canvasColor &&
      a.cardColor == b.cardColor &&
      a.colorScheme == b.colorScheme &&
      a.disabledColor == b.disabledColor &&
      a.dividerColor == b.dividerColor &&
      a.focusColor == b.focusColor &&
      a.highlightColor == b.highlightColor &&
      a.hintColor == b.hintColor &&
      a.hoverColor == b.hoverColor &&
      a.indicatorColor == b.indicatorColor &&
      a.primaryColor == b.primaryColor &&
      a.primaryColorDark == b.primaryColorDark &&
      a.primaryColorLight == b.primaryColorLight &&
      a.scaffoldBackgroundColor == b.scaffoldBackgroundColor &&
      a.secondaryHeaderColor == b.secondaryHeaderColor &&
      a.shadowColor == b.shadowColor &&
      a.splashColor == b.splashColor &&
      a.unselectedWidgetColor == b.unselectedWidgetColor &&
      // TYPOGRAPHY & ICONOGRAPHY
      a.iconTheme == b.iconTheme &&
      a.primaryIconTheme == b.primaryIconTheme &&
      a.primaryTextTheme == b.primaryTextTheme &&
      a.textTheme == b.textTheme &&
      a.typography == b.typography &&
      // COMPONENT THEMES
      a.actionIconTheme == b.actionIconTheme &&
      a.appBarTheme == b.appBarTheme &&
      a.badgeTheme == b.badgeTheme &&
      a.bannerTheme == b.bannerTheme &&
      a.bottomAppBarTheme == b.bottomAppBarTheme &&
      a.bottomNavigationBarTheme == b.bottomNavigationBarTheme &&
      a.bottomSheetTheme == b.bottomSheetTheme &&
      a.buttonTheme == b.buttonTheme &&
      a.cardTheme == b.cardTheme &&
      a.checkboxTheme == b.checkboxTheme &&
      a.chipTheme == b.chipTheme &&
      a.dataTableTheme == b.dataTableTheme &&
      a.datePickerTheme == b.datePickerTheme &&
      a.dialogTheme == b.dialogTheme &&
      a.dividerTheme == b.dividerTheme &&
      a.drawerTheme == b.drawerTheme &&
      a.dropdownMenuTheme == b.dropdownMenuTheme &&
      a.elevatedButtonTheme == b.elevatedButtonTheme &&
      a.expansionTileTheme == b.expansionTileTheme &&
      a.filledButtonTheme == b.filledButtonTheme &&
      a.floatingActionButtonTheme == b.floatingActionButtonTheme &&
      a.iconButtonTheme == b.iconButtonTheme &&
      a.listTileTheme == b.listTileTheme &&
      a.menuBarTheme == b.menuBarTheme &&
      a.menuButtonTheme == b.menuButtonTheme &&
      a.menuTheme == b.menuTheme &&
      a.navigationBarTheme == b.navigationBarTheme &&
      a.navigationDrawerTheme == b.navigationDrawerTheme &&
      a.navigationRailTheme == b.navigationRailTheme &&
      a.outlinedButtonTheme == b.outlinedButtonTheme &&
      a.popupMenuTheme == b.popupMenuTheme &&
      a.progressIndicatorTheme == b.progressIndicatorTheme &&
      a.radioTheme == b.radioTheme &&
      a.searchBarTheme == b.searchBarTheme &&
      a.searchViewTheme == b.searchViewTheme &&
      a.segmentedButtonTheme == b.segmentedButtonTheme &&
      a.sliderTheme == b.sliderTheme &&
      a.snackBarTheme == b.snackBarTheme &&
      a.switchTheme == b.switchTheme &&
      a.tabBarTheme == b.tabBarTheme &&
      a.textButtonTheme == b.textButtonTheme &&
      a.textSelectionTheme == b.textSelectionTheme &&
      a.timePickerTheme == b.timePickerTheme &&
      a.toggleButtonsTheme == b.toggleButtonsTheme &&
      a.tooltipTheme == b.tooltipTheme;
}

extension ThemeParsers on Control {
  Brightness? getBrightness(String propertyName, [Brightness? defaultValue]) {
    return parseBrightness(get(propertyName), defaultValue);
  }

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
