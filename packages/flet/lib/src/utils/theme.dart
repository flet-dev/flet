import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/src/utils/others.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'borders.dart';
import 'buttons.dart';
import 'colors.dart';
import 'drawing.dart';
import 'edge_insets.dart';
import 'icons.dart';
import 'material_state.dart';
import 'menu.dart';
import 'mouse.dart';
import 'numbers.dart';
import 'overlay_style.dart';
import 'shadows.dart';
import 'text.dart';

class SystemUiOverlayStyleTheme
    extends ThemeExtension<SystemUiOverlayStyleTheme> {
  final SystemUiOverlayStyle? systemUiOverlayStyle;
  SystemUiOverlayStyleTheme(this.systemUiOverlayStyle);

  @override
  ThemeExtension<SystemUiOverlayStyleTheme> copyWith() {
    return SystemUiOverlayStyleTheme(systemUiOverlayStyle);
  }

  @override
  ThemeExtension<SystemUiOverlayStyleTheme> lerp(
      covariant ThemeExtension<SystemUiOverlayStyleTheme>? other, double t) {
    return this;
  }
}

CupertinoThemeData parseCupertinoTheme(
    Control control, String propName, Brightness? brightness,
    {ThemeData? parentTheme}) {
  var theme = parseTheme(control, propName, brightness);
  var cupertinoTheme = MaterialBasedCupertinoThemeData(materialTheme: theme);
  return fixCupertinoTheme(cupertinoTheme, theme);
}

CupertinoThemeData fixCupertinoTheme(
    CupertinoThemeData cupertinoTheme, ThemeData theme) {
  return cupertinoTheme.copyWith(
      applyThemeToAll: true,
      barBackgroundColor: theme.colorScheme.background,
      textTheme: cupertinoTheme.textTheme.copyWith(
          navTitleTextStyle: cupertinoTheme.textTheme.navTitleTextStyle
              .copyWith(color: theme.colorScheme.onBackground)));
}

ThemeData parseTheme(Control control, String propName, Brightness? brightness,
    {ThemeData? parentTheme}) {
  dynamic j;
  var v = control.attrString(propName);
  if (v != null) {
    j = json.decode(v);
  }
  return themeFromJson(j, brightness, parentTheme);
}

ThemeData themeFromJson(Map<String, dynamic>? json, Brightness? brightness,
    ThemeData? parentTheme) {
  ThemeData? theme = parentTheme;

  var primarySwatch = parseColor(null, json?["primary_swatch"]);

  var colorSchemeSeed = parseColor(null, json?["color_scheme_seed"]);

  if (colorSchemeSeed != null) {
    primarySwatch = null;
  }

  if (colorSchemeSeed == null && primarySwatch == null) {
    colorSchemeSeed = Colors.blue;
  }

  // create new theme
  theme ??= ThemeData(
      primarySwatch:
          primarySwatch != null ? primarySwatch as MaterialColor : null,
      colorSchemeSeed: colorSchemeSeed,
      fontFamily: json?["font_family"],
      brightness: brightness,
      useMaterial3: json?["use_material3"] ?? primarySwatch == null);

  theme = theme.copyWith(
    visualDensity:
        parseVisualDensity(json?["visual_density"], theme.visualDensity)!,
    pageTransitionsTheme: json?["page_transitions"] != null
        ? parsePageTransitions(json?["page_transitions"])
        : theme.pageTransitionsTheme,
    colorScheme: parseColorScheme(theme, json?["color_scheme"]),
    textTheme: parseTextTheme(theme, theme.textTheme, json?["text_theme"]),
    primaryTextTheme: parseTextTheme(
        theme, theme.primaryTextTheme, json?["primary_text_theme"]),
    scrollbarTheme: parseScrollBarTheme(theme, json?["scrollbar_theme"]),
    tabBarTheme: parseTabBarTheme(theme, json?["tabs_theme"]),
    splashColor: parseColor(theme, json?["splash_color"]),
    highlightColor: parseColor(theme, json?["highlight_color"]),
    hoverColor: parseColor(theme, json?["hover_color"]),
    focusColor: parseColor(theme, json?["focus_color"]),
    unselectedWidgetColor: parseColor(theme, json?["unselected_widget_color"]),
    disabledColor: parseColor(theme, json?["disabled_color"]),
    canvasColor: parseColor(theme, json?["canvas_color"]),
    scaffoldBackgroundColor: parseColor(theme, json?["scaffold_bg_color"]),
    cardColor: parseColor(theme, json?["card_color"]),
    dividerColor: parseColor(theme, json?["divider_color"]),
    dialogBackgroundColor: parseColor(theme, json?["dialog_bg_color"]),
    indicatorColor: parseColor(theme, json?["indicator_color"]),
    hintColor: parseColor(theme, json?["hint_color"]),
    shadowColor: parseColor(theme, json?["shadow_color"]),
    secondaryHeaderColor: parseColor(theme, json?["secondary_header_color"]),
    dialogTheme: parseDialogTheme(theme, json?["dialog_theme"]),
    bottomSheetTheme: parseBottomSheetTheme(theme, json?["bottom_sheet_theme"]),
    primaryColor: parseColor(theme, json?["primary_color"]),
    primaryColorLight: parseColor(theme, json?["primary_color_light"]),
    primaryColorDark: parseColor(theme, json?["primary_color_dark"]),
    cardTheme: parseCardTheme(theme, json?["card_theme"]),
    chipTheme: parseChipTheme(theme, json?["chip_theme"]),
    floatingActionButtonTheme: parseFloatingActionButtonTheme(
        theme, json?["floating_action_button_theme"]),
    bottomAppBarTheme:
        parseBottomAppBarTheme(theme, json?["bottom_app_bar_theme"]),
    checkboxTheme: parseCheckboxTheme(theme, json?["checkbox_theme"]),
    radioTheme: parseRadioTheme(theme, json?["radio_theme"]),
    badgeTheme: parseBadgeTheme(theme, json?["badge_theme"]),
    switchTheme: parseSwitchTheme(theme, json?["switch_theme"]),
    dividerTheme: parseDividerTheme(theme, json?["divider_theme"]),
    snackBarTheme: parseSnackBarTheme(theme, json?["snackbar_theme"]),
    bannerTheme: parseBannerTheme(theme, json?["banner_theme"]),
    datePickerTheme: parseDatePickerTheme(theme, json?["banner_theme"]),
    navigationRailTheme:
        parseNavigationRailTheme(theme, json?["navigation_rail_theme"]),
    appBarTheme: parseAppBarTheme(theme, json?["appbar_theme"]),
    dropdownMenuTheme:
        parseDropdownMenuTheme(theme, json?["dropdown_menu_theme"]),
    listTileTheme: parseListTileTheme(theme, json?["list_tile_theme"]),
    tooltipTheme: parseTooltipTheme(theme, json?["tooltip_theme"]),
    expansionTileTheme:
        parseExpansionTileTheme(theme, json?["expansion_tile_theme"]),
    sliderTheme: parseSliderTheme(theme, json?["slider_theme"]),
    progressIndicatorTheme:
        parseProgressIndicatorTheme(theme, json?["progress_indicator_theme"]),
    popupMenuTheme: parsePopupMenuTheme(theme, json?["popup_menu_theme"]),
    searchBarTheme: parseSearchBarTheme(theme, json?["search_bar_theme"]),
    searchViewTheme: parseSearchViewTheme(theme, json?["search_view_theme"]),
    bottomNavigationBarTheme: parseBottomNavigationBarTheme(
        theme, json?["bottom_navigation_bar_theme"]),
    navigationDrawerTheme:
        parseNavigationDrawerTheme(theme, json?["navigation_drawer_theme"]),
    navigationBarTheme: parseNavigationBarTheme(
      theme,
      json?["navigation_bar_theme"],
    ),
    segmentedButtonTheme: parseSegmentedButtonTheme(
      theme,
      json?["segmented_button_theme"],
    ),
    iconTheme: parseIconTheme(theme, json?["icon_theme"]),
    timePickerTheme: parseTimePickerTheme(theme, json?["time_picker_theme"]),
  );

  var systemOverlayStyle = json?["system_overlay_style"] != null
      ? overlayStyleFromJson(theme, json?["system_overlay_style"], brightness)
      : null;

  return theme.copyWith(
      extensions: {SystemUiOverlayStyleTheme(systemOverlayStyle)},
      cupertinoOverrideTheme: fixCupertinoTheme(
          MaterialBasedCupertinoThemeData(materialTheme: theme), theme));
}

ColorScheme? parseColorScheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  return theme.colorScheme.copyWith(
    primary: parseColor(null, j["primary"]),
    onPrimary: parseColor(null, j["on_primary"]),
    primaryContainer: parseColor(null, j["primary_container"]),
    onPrimaryContainer: parseColor(null, j["on_primary_container"]),
    secondary: parseColor(null, j["secondary"]),
    onSecondary: parseColor(null, j["on_secondary"]),
    secondaryContainer: parseColor(null, j["secondary_container"]),
    onSecondaryContainer: parseColor(null, j["on_secondary_container"]),
    tertiary: parseColor(null, j["tertiary"]),
    onTertiary: parseColor(null, j["on_tertiary"]),
    tertiaryContainer: parseColor(null, j["tertiary_container"]),
    onTertiaryContainer: parseColor(null, j["on_tertiary_container"]),
    error: parseColor(null, j["error"]),
    onError: parseColor(null, j["on_error"]),
    errorContainer: parseColor(null, j["error_container"]),
    onErrorContainer: parseColor(null, j["on_error_container"]),
    background: parseColor(null, j["background"]),
    onBackground: parseColor(null, j["on_background"]),
    surface: parseColor(null, j["surface"]),
    onSurface: parseColor(null, j["on_surface"]),
    surfaceVariant: parseColor(null, j["surface_variant"]),
    onSurfaceVariant: parseColor(null, j["on_surface_variant"]),
    outline: parseColor(null, j["outline"]),
    outlineVariant: parseColor(null, j["outline_variant"]),
    shadow: parseColor(null, j["shadow"]),
    scrim: parseColor(null, j["scrim"]),
    inverseSurface: parseColor(null, j["inverse_surface"]),
    onInverseSurface: parseColor(null, j["on_inverse_surface"]),
    inversePrimary: parseColor(null, j["inverse_primary"]),
    surfaceTint: parseColor(null, j["surface_tint"]),
  );
}

TextTheme? parseTextTheme(
    ThemeData theme, TextTheme textTheme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return textTheme.copyWith(
    bodyLarge: parseTextStyle("body_large"),
    bodyMedium: parseTextStyle("body_medium"),
    bodySmall: parseTextStyle("body_small"),
    displayLarge: parseTextStyle("display_large"),
    displayMedium: parseTextStyle("display_medium"),
    displaySmall: parseTextStyle("display_small"),
    headlineLarge: parseTextStyle("headline_large"),
    headlineMedium: parseTextStyle("headline_medium"),
    headlineSmall: parseTextStyle("headline_small"),
    labelLarge: parseTextStyle("label_large"),
    labelMedium: parseTextStyle("label_medium"),
    labelSmall: parseTextStyle("label_small"),
    titleLarge: parseTextStyle("title_large"),
    titleMedium: parseTextStyle("title_medium"),
    titleSmall: parseTextStyle("title_small"),
  );
}

ScrollbarThemeData? parseScrollBarTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  return theme.scrollbarTheme.copyWith(
    trackVisibility: getMaterialStateProperty<bool?>(
        j["track_visibility"], (jv) => parseBool(jv)),
    trackColor: getMaterialStateProperty<Color?>(
        j["track_color"], (jv) => parseColor(theme, jv as String)),
    trackBorderColor: getMaterialStateProperty<Color?>(
        j["track_border_color"], (jv) => parseColor(theme, jv as String)),
    thumbVisibility: getMaterialStateProperty<bool?>(
        j["thumb_visibility"], (jv) => parseBool(jv)),
    thumbColor: getMaterialStateProperty<Color?>(
        j["thumb_color"], (jv) => parseColor(theme, jv as String)),
    thickness: getMaterialStateProperty<double?>(
        j["thickness"], (jv) => parseDouble(jv)),
    radius:
        j["radius"] != null ? Radius.circular(parseDouble(j["radius"])) : null,
    crossAxisMargin: j["cross_axis_margin"] != null
        ? parseDouble(j["cross_axis_margin"])
        : null,
    mainAxisMargin: j["main_axis_margin"] != null
        ? parseDouble(j["main_axis_margin"])
        : null,
    minThumbLength: j["min_thumb_length"] != null
        ? parseDouble(j["min_thumb_length"])
        : null,
    interactive: j["interactive"] != null ? parseBool(j["interactive"]) : null,
  );
}

TabBarTheme? parseTabBarTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  var indicatorColor = parseColor(theme, j["indicator_color"]);

  return theme.tabBarTheme.copyWith(
    overlayColor: getMaterialStateProperty<Color?>(
        j["overlay_color"], (jv) => parseColor(theme, jv as String)),
    dividerColor: parseColor(theme, j["divider_color"]),
    indicatorColor: indicatorColor,
    labelColor: parseColor(theme, j["label_color"]),
    unselectedLabelColor: parseColor(theme, j["unselected_label_color"]),
    indicatorSize: parseBool(j["indicator_tab_size"], false)
        ? TabBarIndicatorSize.tab
        : TabBarIndicatorSize.label,
    indicator: j["indicator_border_radius"] != null ||
            j["indicator_border_side"] != null ||
            j["indicator_padding"] != null
        ? UnderlineTabIndicator(
            borderRadius: j["indicator_border_radius"] != null
                ? borderRadiusFromJSON(j["indicator_border_radius"])
                : const BorderRadius.only(
                    topLeft: Radius.circular(2), topRight: Radius.circular(2)),
            borderSide: borderSideFromJSON(
                    theme, j["indicator_border_side"], indicatorColor) ??
                BorderSide(
                    width: 2.0,
                    color: indicatorColor ?? theme.colorScheme.primary),
            insets:
                edgeInsetsFromJson(j["indicator_padding"]) ?? EdgeInsets.zero)
        : null,
    mouseCursor: getMaterialStateProperty<MouseCursor?>(
        j["mouse_cursor"], (jv) => parseMouseCursor(jv)),
    labelPadding: edgeInsetsFromJson(j["label_padding"]),
    dividerHeight:
        j["divider_height"] != null ? parseDouble(j["divider_height"]) : null,
    labelStyle: j["label_text_style"] != null
        ? textStyleFromJson(theme, j["label_text_style"])
        : null,
    unselectedLabelStyle: j["unselected_label_text_style"] != null
        ? textStyleFromJson(theme, j["unselected_label_text_style"])
        : null,
  );
}

VisualDensity? parseVisualDensity(String? density, [VisualDensity? defValue]) {
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
      return defValue;
  }
}

PageTransitionsTheme parsePageTransitions(Map<String, dynamic>? json) {
  return PageTransitionsTheme(builders: {
    TargetPlatform.android: parseTransitionsBuilder(
        json?["android"], const FadeUpwardsPageTransitionsBuilder()),
    TargetPlatform.iOS: parseTransitionsBuilder(
        json?["ios"], const CupertinoPageTransitionsBuilder()),
    TargetPlatform.linux: parseTransitionsBuilder(
        json?["linux"], const ZoomPageTransitionsBuilder()),
    TargetPlatform.macOS: parseTransitionsBuilder(
        json?["macos"], const ZoomPageTransitionsBuilder()),
    TargetPlatform.windows: parseTransitionsBuilder(
        json?["windows"], const ZoomPageTransitionsBuilder()),
  });
}

DialogTheme? parseDialogTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.dialogTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    iconColor: parseColor(theme, j["icon_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    titleTextStyle: parseTextStyle("title_text_style"),
    contentTextStyle: parseTextStyle("content_text_style"),
    alignment:
        j["alignment"] != null ? alignmentFromJson(j["alignment"]) : null,
    actionsPadding: edgeInsetsFromJson(j["actions_padding"]),
  );
}

BottomSheetThemeData? parseBottomSheetTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.bottomSheetTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    dragHandleColor: parseColor(theme, j["drag_handle_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    showDragHandle:
        j["show_drag_handle"] != null ? parseBool(j["show_drag_handle"]) : null,
    modalBackgroundColor: parseColor(theme, j["modal_bgcolor"]),
    modalElevation:
        j["modal_elevation"] != null ? parseDouble(j["modal_elevation"]) : null,
    clipBehavior: parseClip(j["clip_behavior"]),
  );
}

CardTheme? parseCardTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.cardTheme.copyWith(
      color: parseColor(theme, j["color"]),
      shadowColor: parseColor(theme, j["shadow_color"]),
      surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
      elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
      shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
      clipBehavior: parseClip(j["clip_behavior"]),
      margin: edgeInsetsFromJson(j["margin"]));
}

ChipThemeData? parseChipTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.chipTheme.copyWith(
    color: getMaterialStateProperty<Color?>(
        j["color"], (jv) => parseColor(theme, jv as String)),
    backgroundColor: parseColor(theme, j["bgcolor"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    padding: edgeInsetsFromJson(j["padding"]),
    labelPadding: edgeInsetsFromJson(j["label_padding"]),
    labelStyle: parseTextStyle("label_text_style"),
    secondaryLabelStyle: parseTextStyle("secondary_label_text_style"),
    disabledColor: parseColor(theme, j["disabled_color"]),
    selectedColor: parseColor(theme, j["selected_color"]),
    checkmarkColor: parseColor(theme, j["check_color"]),
    deleteIconColor: parseColor(theme, j["delete_icon_color"]),
    side: j["border_side"] != null
        ? borderSideFromJSON(theme, j["border_side"], null)
        : null,
    secondarySelectedColor: parseColor(theme, j["secondary_selected_color"]),
    brightness: j["brightness"] != null
        ? Brightness.values.firstWhereOrNull(
            (b) => b.name.toLowerCase() == j["brightness"].toLowerCase())
        : null,
    selectedShadowColor: parseColor(theme, j["selected_shadow_color"]),
    showCheckmark:
        j["show_checkmark"] != null ? parseBool(j["show_checkmark"]) : null,
    pressElevation:
        j["click_elevation"] != null ? parseDouble(j["click_elevation"]) : null,
  );
}

FloatingActionButtonThemeData? parseFloatingActionButtonTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.floatingActionButtonTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    hoverColor: parseColor(theme, j["hover_color"]),
    focusColor: parseColor(theme, j["focus_color"]),
    foregroundColor: parseColor(theme, j["foreground_color"]),
    splashColor: parseColor(theme, j["splash_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    focusElevation:
        j["focus_elevation"] != null ? parseDouble(j["focus_elevation"]) : null,
    hoverElevation:
        j["hover_elevation"] != null ? parseDouble(j["hover_elevation"]) : null,
    highlightElevation: j["highlight_elevation"] != null
        ? parseDouble(j["highlight_elevation"])
        : null,
    disabledElevation: j["disabled_elevation"] != null
        ? parseDouble(j["disabled_elevation"])
        : null,
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    enableFeedback:
        j["enable_feedback"] != null ? parseBool(j["enable_feedback"]) : null,
    extendedPadding: edgeInsetsFromJson(j["extended_padding"]),
    extendedTextStyle: parseTextStyle("extended_text_style"),
    extendedIconLabelSpacing: j["extended_icon_label_spacing"] != null
        ? parseDouble(j["extended_icon_label_spacing"])
        : null,
    mouseCursor: getMaterialStateProperty<MouseCursor?>(
        j["mouse_cursor"], (jv) => parseMouseCursor(jv)),
    iconSize: j["icon_size"] != null ? parseDouble(j["icon_size"]) : null,
  );
}

NavigationRailThemeData? parseNavigationRailTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.navigationRailTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    indicatorColor: parseColor(theme, j["indicator_color"]),
    unselectedLabelTextStyle: parseTextStyle("unselected_label_text_style"),
    selectedLabelTextStyle: parseTextStyle("selected_label_text_style"),
    minWidth: j["min_width"] != null ? parseDouble(j["min_width"]) : null,
    labelType: j["label_type"] != null
        ? NavigationRailLabelType.values
            .firstWhereOrNull((c) => c.name == j["label_type"])
        : null,
    groupAlignment:
        j["group_alignment"] != null ? parseDouble(j["group_alignment"]) : null,
    indicatorShape: j["indicator_shape"] != null
        ? outlinedBorderFromJSON(j["indicator_shape"])
        : null,
    minExtendedWidth: j["min_extended_width"] != null
        ? parseDouble(j["min_extended_width"])
        : null,
    useIndicator:
        j["use_indicator"] != null ? parseBool(j["use_indicator"]) : null,
  );
}

AppBarTheme? parseAppBarTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.appBarTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    color: parseColor(theme, j["color"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    foregroundColor: parseColor(theme, j["foreground_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    titleTextStyle: parseTextStyle("title_text_style"),
    toolbarTextStyle: parseTextStyle("toolbar_text_style"),
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    centerTitle:
        j["center_title"] != null ? parseBool(j["center_title"]) : null,
    titleSpacing:
        j["title_spacing"] != null ? parseDouble(j["title_spacing"]) : null,
    scrolledUnderElevation: j["scroll_elevation"] != null
        ? parseDouble(j["scroll_elevation"])
        : null,
    toolbarHeight:
        j["toolbar_height"] != null ? parseDouble(j["toolbar_height"]) : null,
  );
}

BottomAppBarTheme? parseBottomAppBarTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.bottomAppBarTheme.copyWith(
    color: parseColor(theme, j["color"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    height: j["height"] != null ? parseDouble(j["height"]) : null,
    padding: edgeInsetsFromJson(j["padding"]),
    //shape:
  );
}

RadioThemeData? parseRadioTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.radioTheme.copyWith(
    fillColor: getMaterialStateProperty<Color?>(
        j["fill_color"], (jv) => parseColor(theme, jv as String)),
    splashRadius:
        j["splash_radius"] != null ? parseDouble(j["splash_radius"]) : null,
    overlayColor: getMaterialStateProperty<Color?>(
        j["overlay_color"], (jv) => parseColor(theme, jv as String)),
    visualDensity: parseVisualDensity(j["visual_density"]),
    mouseCursor: getMaterialStateProperty<MouseCursor?>(
        j["mouse_cursor"], (jv) => parseMouseCursor(jv)),
  );
}

CheckboxThemeData? parseCheckboxTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.checkboxTheme.copyWith(
    fillColor: getMaterialStateProperty<Color?>(
        j["fill_color"], (jv) => parseColor(theme, jv as String)),
    splashRadius:
        j["splash_radius"] != null ? parseDouble(j["splash_radius"]) : null,
    overlayColor: getMaterialStateProperty<Color?>(
        j["overlay_color"], (jv) => parseColor(theme, jv as String)),
    visualDensity: parseVisualDensity(j["visual_density"]),
    checkColor: getMaterialStateProperty<Color?>(
        j["check_color"], (jv) => parseColor(theme, jv as String)),
    side: j["border_side"] != null
        ? borderSideFromJSON(theme, j["border_side"], null)
        : null,
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    mouseCursor: getMaterialStateProperty<MouseCursor?>(
        j["mouse_cursor"], (jv) => parseMouseCursor(jv)),
  );
}

BadgeThemeData? parseBadgeTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.badgeTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    textStyle: parseTextStyle("text_style"),
    padding: edgeInsetsFromJson(j["padding"]),
    alignment:
        j["alignment"] != null ? alignmentFromJson(j["alignment"]) : null,
    textColor: parseColor(theme, j["text_color"]),
    offset: j["offset"] != null ? offsetFromJson(j["offset"]) : null,
    smallSize: j["small_size"] != null ? parseDouble(j["small_size"]) : null,
    largeSize: j["large_size"] != null ? parseDouble(j["large_size"]) : null,
  );
}

SwitchThemeData? parseSwitchTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.switchTheme.copyWith(
    thumbColor: getMaterialStateProperty<Color?>(
        j["thumb_color"], (jv) => parseColor(theme, jv as String)),
    trackColor: getMaterialStateProperty<Color?>(
        j["track_color"], (jv) => parseColor(theme, jv as String)),
    overlayColor: getMaterialStateProperty<Color?>(
        j["overlay_color"], (jv) => parseColor(theme, jv as String)),
    splashRadius:
        j["splash_radius"] != null ? parseDouble(j["splash_radius"]) : null,
    thumbIcon: getMaterialStateProperty<Icon?>(
        j["thumb_icon"], (jv) => Icon(parseIcon(jv as String))),
    trackOutlineColor: getMaterialStateProperty<Color?>(
        j["track_outline_color"],
        (jv) => parseColor(theme, jv as String),
        null),
    trackOutlineWidth: getMaterialStateProperty<double?>(
        j["track_outline_width"], (jv) => parseDouble(jv)),
    mouseCursor: getMaterialStateProperty<MouseCursor?>(
        j["mouse_cursor"], (jv) => parseMouseCursor(jv)),
  );
}

DividerThemeData? parseDividerTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.dividerTheme.copyWith(
    color: parseColor(theme, j["color"]),
    space: j["space"] != null ? parseDouble(j["space"]) : null,
    thickness: j["thickness"] != null ? parseDouble(j["thickness"]) : null,
    indent:
        j["leading_indent"] != null ? parseDouble(j["leading_indent"]) : null,
    endIndent:
        j["trailing_indent"] != null ? parseDouble(j["trailing_indent"]) : null,
  );
}

SnackBarThemeData? parseSnackBarTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.snackBarTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    actionTextColor: parseColor(theme, j["action_text_color"]),
    actionBackgroundColor: parseColor(theme, j["action_bgcolor"]),
    closeIconColor: parseColor(theme, j["close_icon_color"]),
    disabledActionTextColor: parseColor(theme, j["disabled_action_text_color"]),
    disabledActionBackgroundColor:
        parseColor(theme, j["disabled_action_bgcolor"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    behavior: j["behavior"] != null
        ? SnackBarBehavior.values.firstWhereOrNull(
            (c) => c.name.toLowerCase() == j["behavior"].toLowerCase())
        : null,
    contentTextStyle: parseTextStyle("content_text_style"),
    width: j["width"] != null ? parseDouble(j["width"]) : null,
    insetPadding: edgeInsetsFromJson(j["inset_padding"]),
    dismissDirection: j["dismiss_direction"] != null
        ? DismissDirection.values.firstWhereOrNull(
            (c) => c.name.toLowerCase() == j["dismiss_direction"].toLowerCase())
        : null,
    showCloseIcon:
        j["show_close_icon"] != null ? parseBool(j["show_close_icon"]) : null,
    actionOverflowThreshold: j["action_overflow_threshold"] != null
        ? parseDouble(j["action_overflow_threshold"])
        : null,
  );
}

MaterialBannerThemeData? parseBannerTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.bannerTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    dividerColor: parseColor(theme, j["divider_color"]),
    padding: edgeInsetsFromJson(j["padding"]),
    leadingPadding: edgeInsetsFromJson(j["leading_padding"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    contentTextStyle: parseTextStyle("content_text_style"),
  );
}

DatePickerThemeData? parseDatePickerTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.datePickerTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    dividerColor: parseColor(theme, j["divider_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    cancelButtonStyle: buttonStyleFromJSON(theme, j["cancel_button_style"]),
    confirmButtonStyle: buttonStyleFromJSON(theme, j["confirm_button_style"]),
    dayBackgroundColor: getMaterialStateProperty<Color?>(
        j["day_bgcolor"], (jv) => parseColor(theme, jv as String)),
    yearStyle: parseTextStyle("year_text_style"),
    dayStyle: parseTextStyle("day_text_style"),
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    dayOverlayColor: getMaterialStateProperty<Color?>(
        j["day_overlay_color"], (jv) => parseColor(theme, jv as String)),
    headerBackgroundColor: parseColor(theme, j["header_bgcolor"]),
    dayForegroundColor: getMaterialStateProperty<Color?>(
        j["day_foreground_color"], (jv) => parseColor(theme, jv as String)),
    rangePickerElevation: j["range_picker_elevation"] != null
        ? parseDouble(j["range_picker_elevation"])
        : null,
    todayBackgroundColor: getMaterialStateProperty<Color?>(
        j["today_bgcolor"], (jv) => parseColor(theme, jv as String)),
    headerForegroundColor: parseColor(theme, j["header_foreground_color"]),
    headerHeadlineStyle: parseTextStyle("header_headline_text_style"),
    headerHelpStyle: parseTextStyle("header_help_text_style"),
    rangePickerBackgroundColor: parseColor(theme, j["range_picker_bgcolor"]),
    rangePickerHeaderBackgroundColor:
        parseColor(theme, j["range_picker_header_bgcolor"]),
    rangePickerHeaderForegroundColor:
        parseColor(theme, j["range_picker_header_foreground_color"]),
    rangePickerShadowColor: parseColor(theme, j["range_picker_shadow_color"]),
    todayForegroundColor: getMaterialStateProperty<Color?>(
        j["today_foreground_color"], (jv) => parseColor(theme, jv as String)),
    rangePickerShape: j["range_picker_shape"] != null
        ? outlinedBorderFromJSON(j["range_picker_shape"])
        : null,
    rangePickerHeaderHelpStyle:
        parseTextStyle("range_picker_header_help_text_style"),
    rangePickerHeaderHeadlineStyle:
        parseTextStyle("range_picker_header_headline_text_style"),
    rangePickerSurfaceTintColor:
        parseColor(theme, j["range_picker_surface_tint_color"]),
    rangeSelectionBackgroundColor:
        parseColor(theme, j["range_selection_bgcolor"]),
    rangeSelectionOverlayColor: getMaterialStateProperty<Color?>(
        j["range_selection_overlay_color"],
        (jv) => parseColor(theme, jv as String)),
    todayBorder: j["today_border_side"] != null
        ? borderSideFromJSON(theme, j["today_border_side"])
        : null,
    yearBackgroundColor: getMaterialStateProperty<Color?>(
        j["year_bgcolor"], (jv) => parseColor(theme, jv as String)),
    yearForegroundColor: getMaterialStateProperty<Color?>(
        j["year_foreground_color"], (jv) => parseColor(theme, jv as String)),
    yearOverlayColor: getMaterialStateProperty<Color?>(
        j["year_overlay_color"], (jv) => parseColor(theme, jv as String)),
    weekdayStyle: parseTextStyle("weekday_text_style"),
  );
}

TimePickerThemeData? parseTimePickerTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.timePickerTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    padding: edgeInsetsFromJson(j["padding"]),
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    dayPeriodBorderSide: j["day_period_border_side"] != null
        ? borderSideFromJSON(theme, j["day_period_border_side"])
        : null,
    dayPeriodButtonStyle:
        buttonStyleFromJSON(theme, j["day_period_button_style"]),
    dayPeriodColor: parseColor(theme, j["day_period_color"]),
    dayPeriodShape: j["day_period_shape"] != null
        ? outlinedBorderFromJSON(j["day_period_shape"])
        : null,
    dayPeriodTextColor: parseColor(theme, j["day_period_text_color"]),
    dayPeriodTextStyle: parseTextStyle("day_period_text_style"),
    dialBackgroundColor: parseColor(theme, j["dial_bgcolor"]),
    dialHandColor: parseColor(theme, j["dial_hand_color"]),
    dialTextColor: parseColor(theme, j["dial_text_color"]),
    dialTextStyle: parseTextStyle("dial_text_style"),
    entryModeIconColor: parseColor(theme, j["entry_mode_icon_color"]),
    helpTextStyle: parseTextStyle("help_text_style"),
    hourMinuteColor: parseColor(theme, j["hour_minute_color"]),
    hourMinuteTextColor: parseColor(theme, j["hour_minute_text_color"]),
    hourMinuteTextStyle: parseTextStyle("hour_minute_text_style"),
    hourMinuteShape: j["hour_minute_shape"] != null
        ? outlinedBorderFromJSON(j["hour_minute_shape"])
        : null,
    cancelButtonStyle: buttonStyleFromJSON(theme, j["cancel_button_style"]),
    confirmButtonStyle: buttonStyleFromJSON(theme, j["confirm_button_style"]),
  );
}

DropdownMenuThemeData? parseDropdownMenuTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.dropdownMenuTheme.copyWith(
    menuStyle: j["menu_style"] != null
        ? menuStyleFromJSON(theme, j["menu_style"])
        : null,
    textStyle: parseTextStyle("text_style"),
  );
}

ListTileThemeData? parseListTileTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.listTileTheme.copyWith(
    iconColor: parseColor(theme, j["icon_color"]),
    textColor: parseColor(theme, j["text_color"]),
    tileColor: parseColor(theme, j["bgcolor"]),
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    contentPadding: edgeInsetsFromJson(j["content_padding"]),
    selectedColor: parseColor(theme, j["selected_color"]),
    selectedTileColor: parseColor(theme, j["selected_tile_color"]),
    isThreeLine:
        j["is_three_line"] != null ? parseBool(j["is_three_line"]) : null,
    visualDensity: parseVisualDensity(j["visual_density"]),
    titleTextStyle: parseTextStyle("title_text_style"),
    subtitleTextStyle: parseTextStyle("subtitle_text_style"),
    minVerticalPadding: j["min_vertical_padding"] != null
        ? parseDouble(j["min_vertical_padding"])
        : null,
    enableFeedback:
        j["enable_feedback"] != null ? parseBool(j["enable_feedback"]) : null,
    dense: j["dense"] != null ? parseBool(j["dense"]) : null,
    // style:
    horizontalTitleGap: j["horizontal_spacing"] != null
        ? parseDouble(j["horizontal_spacing"])
        : null,
    // titleAlignment: j["title_alignment"] != null ? alignmentFromJson(j["title_alignment"]) : null,
    minLeadingWidth: j["min_leading_width"] != null
        ? parseDouble(j["min_leading_width"])
        : null,
    leadingAndTrailingTextStyle:
        parseTextStyle("leading_and_trailing_text_style"),
  );
}

TooltipThemeData? parseTooltipTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.tooltipTheme.copyWith(
    enableFeedback: j["enable_feedback"] != null,
    height: j["height"] != null ? parseDouble(j["height"]) : null,
    excludeFromSemantics: j["exclude_from_semantics"] != null
        ? parseBool(j["exclude_from_semantics"])
        : null,
    textStyle: parseTextStyle("text_style"),
  );
}

ExpansionTileThemeData? parseExpansionTileTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.expansionTileTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    iconColor: parseColor(theme, j["icon_color"]),
    textColor: parseColor(theme, j["text_color"]),
    collapsedBackgroundColor: parseColor(theme, j["collapsed_bgcolor"]),
    collapsedIconColor: parseColor(theme, j["collapsed_icon_color"]),
  );
}

SliderThemeData? parseSliderTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.sliderTheme.copyWith(
    activeTrackColor: parseColor(theme, j["active_track_color"]),
    inactiveTrackColor: parseColor(theme, j["inactive_track_color"]),
    thumbColor: parseColor(theme, j["thumb_color"]),
    overlayColor: parseColor(theme, j["overlay_color"]),
    valueIndicatorColor: parseColor(theme, j["value_indicator_color"]),
    disabledThumbColor: parseColor(theme, j["disabled_thumb_color"]),
    valueIndicatorTextStyle: parseTextStyle("value_indicator_text_style"),
  );
}

ProgressIndicatorThemeData? parseProgressIndicatorTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.progressIndicatorTheme.copyWith(
    color: parseColor(theme, j["color"]),
    circularTrackColor: parseColor(theme, j["circular_track_color"]),
    linearTrackColor: parseColor(theme, j["linear_track_color"]),
    refreshBackgroundColor: parseColor(theme, j["refresh_bgcolor"]),
    linearMinHeight: j["linear_min_height"] != null
        ? parseDouble(j["linear_min_height"])
        : null,
  );
}

PopupMenuThemeData? parsePopupMenuTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.popupMenuTheme.copyWith(
    color: parseColor(theme, j["color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    iconColor: parseColor(theme, j["icon_color"]),
    textStyle: parseTextStyle("text_style"),
    labelTextStyle: getMaterialStateProperty<TextStyle?>(
        j["label_text_style"], (jv) => parseTextStyle(jv)),
    enableFeedback: parseBool(j["enable_feedback"], true),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    iconSize: j["icon_size"] != null ? parseDouble(j["icon_size"]) : null,
    position: j["menu_position"] != null
        ? PopupMenuPosition.values.firstWhereOrNull(
            (c) => c.name.toLowerCase() == j["menu_position"].toLowerCase())
        : null,
    mouseCursor: getMaterialStateProperty<MouseCursor?>(
        j["mouse_cursor"], (jv) => parseMouseCursor(jv)),
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
  );
}

SearchBarThemeData? parseSearchBarTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.searchBarTheme.copyWith(
    surfaceTintColor: getMaterialStateProperty<Color?>(
        j["surface_tint_color"], (jv) => parseColor(theme, jv as String)),
    shadowColor: getMaterialStateProperty<Color?>(
        j["shadow_color"], (jv) => parseColor(theme, jv as String)),
    elevation: getMaterialStateProperty<double?>(
        j["elevation"], (jv) => parseDouble(jv)),
    backgroundColor: getMaterialStateProperty<Color?>(
        j["bgcolor"], (jv) => parseColor(theme, jv as String)),
    overlayColor: getMaterialStateProperty<Color?>(
        j["overlay_color"], (jv) => parseColor(theme, jv as String)),
    textStyle: getMaterialStateProperty<TextStyle?>(
        j["text_style"], (jv) => parseTextStyle(jv)),
    hintStyle: getMaterialStateProperty<TextStyle?>(
        j["hint_style"], (jv) => parseTextStyle(jv)),
    shape: getMaterialStateProperty<OutlinedBorder?>(
        j["shape"], (jv) => outlinedBorderFromJSON(jv)),
    textCapitalization: j["text_capitalization"] != null
        ? TextCapitalization.values.firstWhereOrNull((c) =>
            c.name.toLowerCase() == j["text_capitalization"].toLowerCase())
        : null,
    padding: getMaterialStateProperty<EdgeInsetsGeometry?>(
        j["padding"], (jv) => edgeInsetsFromJson(jv)),
  );
}

SearchViewThemeData? parseSearchViewTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.searchViewTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    dividerColor: parseColor(theme, j["divider_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    headerHintStyle: parseTextStyle("header_hint_text_style"),
    headerTextStyle: parseTextStyle("header_text_style"),
    shape: j["shape"] != null ? outlinedBorderFromJSON(j["shape"]) : null,
    side: j["border_side"] != null
        ? borderSideFromJSON(theme, j["border_side"])
        : null,
  );
}

BottomNavigationBarThemeData? parseBottomNavigationBarTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.bottomNavigationBarTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    selectedItemColor: parseColor(theme, j["selected_item_color"]),
    unselectedItemColor: parseColor(theme, j["unselected_item_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    enableFeedback: parseBool(j["enable_feedback"], true),
    showSelectedLabels: j["show_selected_labels"] != null
        ? parseBool(j["show_selected_labels"])
        : null,
    showUnselectedLabels: j["show_unselected_labels"] != null
        ? parseBool(j["show_unselected_labels"])
        : null,
    selectedLabelStyle: parseTextStyle("selected_label_text_style"),
    unselectedLabelStyle: parseTextStyle("unselected_label_text_style"),
  );
}

NavigationDrawerThemeData? parseNavigationDrawerTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.navigationDrawerTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    indicatorColor: parseColor(theme, j["indicator_color"]),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    //indicatorSize: ,
    tileHeight: j["tile_height"] != null ? parseDouble(j["tile_height"]) : null,
    labelTextStyle: getMaterialStateProperty<TextStyle?>(
        j["label_text_style"], (jv) => parseTextStyle(jv)),
    indicatorShape: j["indicator_shape"] != null
        ? outlinedBorderFromJSON(j["indicator_shape"])
        : null,
  );
}

NavigationBarThemeData? parseNavigationBarTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return theme.navigationBarTheme.copyWith(
    backgroundColor: parseColor(theme, j["bgcolor"]),
    shadowColor: parseColor(theme, j["shadow_color"]),
    surfaceTintColor: parseColor(theme, j["surface_tint_color"]),
    indicatorColor: parseColor(theme, j["indicator_color"]),
    overlayColor: getMaterialStateProperty<Color?>(
        j["overlay_color"], (jv) => parseColor(theme, jv as String)),
    elevation: j["elevation"] != null ? parseDouble(j["elevation"]) : null,
    height: j["height"] != null ? parseDouble(j["height"]) : null,
    labelTextStyle: getMaterialStateProperty<TextStyle?>(
        j["label_text_style"], (jv) => parseTextStyle(jv)),
    indicatorShape: j["indicator_shape"] != null
        ? outlinedBorderFromJSON(j["indicator_shape"])
        : null,
    labelBehavior: j["label_behavior"] != null
        ? NavigationDestinationLabelBehavior.values.firstWhereOrNull(
            (c) => c.name.toLowerCase() == j["label_behavior"].toLowerCase())
        : null,
  );
}

SegmentedButtonThemeData? parseSegmentedButtonTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.segmentedButtonTheme.copyWith(
    // selectedIcon: ,
    style: buttonStyleFromJSON(theme, j["style"]),
  );
}

IconThemeData? parseIconTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  return theme.iconTheme.copyWith(
    color: parseColor(theme, j["color"]),
    applyTextScaling: parseBool(j["apply_text_scaling"]),
    fill: j["fill"] != null ? parseDouble(j["fill"]) : null,
    opacity: j["opacity"] != null ? parseDouble(j["opacity"]) : null,
    size: j["size"] != null ? parseDouble(j["size"]) : null,
    opticalSize:
        j["optical_size"] != null ? parseDouble(j["optical_size"]) : null,
    grade: j["grade"] != null ? parseDouble(j["grade"]) : null,
    weight: j["weight"] != null ? parseDouble(j["weight"]) : null,
    shadows:
        j["shadows"] != null ? boxShadowsFromJSON(theme, j["shadows"]) : null,
  );
}

PageTransitionsBuilder parseTransitionsBuilder(
    String? tb, PageTransitionsBuilder defaultBuilder) {
  switch (tb?.toLowerCase()) {
    case "fadeupwards":
      return const FadeUpwardsPageTransitionsBuilder();
    case "openupwards":
      return const OpenUpwardsPageTransitionsBuilder();
    case "cupertino":
      return const CupertinoPageTransitionsBuilder();
    case "zoom":
      return const ZoomPageTransitionsBuilder();
    case "none":
      return const NoPageTransitionsBuilder();
    default:
      return defaultBuilder;
  }
}

class NoPageTransitionsBuilder extends PageTransitionsBuilder {
  const NoPageTransitionsBuilder();

  @override
  Widget buildTransitions<T>(
    PageRoute<T>? route,
    BuildContext? context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget? child,
  ) {
    // only return the child without warping it with animations
    return child!;
  }
}
