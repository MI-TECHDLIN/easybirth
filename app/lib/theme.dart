// theme.dart
// AmaraAI ("easybirth") — Design tokens & Material 3 ThemeData
// Drop into: lib/theme.dart
//
// Requires in pubspec.yaml:
//   google_fonts: ^6.2.1

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Color palette — matches DESIGN SYSTEM tokens.
class AppColors {
  AppColors._();

  // Primary — Healing Green
  static const Color primary = Color(0xFF1B6B4A);
  static const Color primaryContainer = Color(0xFFB7E4C7);

  // Secondary — Maternal Lavender
  static const Color secondary = Color(0xFF6B4E9E);
  static const Color secondaryContainer = Color(0xFFD9CFEF);

  // Tertiary — Urgency Amber
  static const Color tertiary = Color(0xFFC96E3A);
  static const Color tertiaryContainer = Color(0xFFFFDBC7);

  // Surfaces & background
  static const Color surface = Color(0xFFF7F3EF);
  static const Color background = Color(0xFFF2EDE8);
  static const Color surfaceVariant = Color(0xFFEDE7E1);

  // Voice mode
  static const Color voiceModeDark = Color(0xFF0D1F17);

  // Risk semantics
  static const Color highRisk = Color(0xFFE63946);
  static const Color highRiskContainer = Color(0xFFFFDDE0);
  static const Color moderateRisk = Color(0xFFF4A261);
  static const Color moderateRiskContainer = Color(0xFFFFF0E4);
  static const Color safeRisk = Color(0xFF52B788);
  static const Color safeRiskContainer = Color(0xFFE8F5EE);

  // Text & outline
  static const Color textPrimary = Color(0xFF1A1A1A);
  static const Color textSecondary = Color(0xFF5C5C5C);
  static const Color outline = Color(0xFF9B8F87);
}

/// Typography scale — matches DESIGN SYSTEM tokens.
class AppTextStyles {
  AppTextStyles._();

  // Plus Jakarta Sans family
  static TextStyle displayLarge = GoogleFonts.plusJakartaSans(
    fontSize: 32,
    fontWeight: FontWeight.w700,
    color: AppColors.textPrimary,
  );

  static TextStyle displayMedium = GoogleFonts.plusJakartaSans(
    fontSize: 26,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
  );

  static TextStyle headline = GoogleFonts.plusJakartaSans(
    fontSize: 22,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
  );

  static TextStyle title = GoogleFonts.plusJakartaSans(
    fontSize: 18,
    fontWeight: FontWeight.w500,
    color: AppColors.textPrimary,
  );

  // Nunito family
  static TextStyle bodyLarge = GoogleFonts.nunito(
    fontSize: 18,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
  );

  static TextStyle bodyMedium = GoogleFonts.nunito(
    fontSize: 16,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
  );

  static TextStyle label = GoogleFonts.nunito(
    fontSize: 14,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
  );

  static TextStyle caption = GoogleFonts.nunito(
    fontSize: 12,
    fontWeight: FontWeight.w400,
    color: AppColors.outline,
  );

  // JetBrains Mono
  static TextStyle monoData = GoogleFonts.jetBrainsMono(
    fontSize: 14,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
  );
}

/// Border radii — matches Material 3 Setup tokens.
class AppRadii {
  AppRadii._();

  static const double card = 20;
  static const double button = 16;
  static const double dialog = 24;
}

/// Risk level enum — drives color/copy/icon across screens.
enum RiskLevel { high, moderate, low }

extension RiskLevelX on RiskLevel {
  Color get color {
    switch (this) {
      case RiskLevel.high:
        return AppColors.highRisk;
      case RiskLevel.moderate:
        return AppColors.moderateRisk;
      case RiskLevel.low:
        return AppColors.safeRisk;
    }
  }

  Color get containerColor {
    switch (this) {
      case RiskLevel.high:
        return AppColors.highRiskContainer;
      case RiskLevel.moderate:
        return AppColors.moderateRiskContainer;
      case RiskLevel.low:
        return AppColors.safeRiskContainer;
    }
  }

  String get label {
    switch (this) {
      case RiskLevel.high:
        return 'HIGH RISK';
      case RiskLevel.moderate:
        return 'MONITOR';
      case RiskLevel.low:
        return 'LOOKING GOOD';
    }
  }

  String get icon {
    switch (this) {
      case RiskLevel.high:
        return '⚠️';
      case RiskLevel.moderate:
        return '🔶';
      case RiskLevel.low:
        return '✓';
    }
  }

  String get recommendation {
    switch (this) {
      case RiskLevel.high:
        return 'Go to your health centre now. Do not wait. Your baby and '
            'your health are at risk.';
      case RiskLevel.moderate:
        return 'Rest and watch these signs closely. Call your CHW if they '
            'get worse in the next few hours.';
      case RiskLevel.low:
        return 'Everything seems normal. Keep your next ANC appointment and '
            'continue eating well.';
    }
  }
}

/// Builds the app's Material 3 ThemeData.
ThemeData buildAppTheme() {
  final colorScheme = ColorScheme.fromSeed(
    seedColor: AppColors.primary,
    brightness: Brightness.light,
  ).copyWith(
    primary: AppColors.primary,
    primaryContainer: AppColors.primaryContainer,
    secondary: AppColors.secondary,
    secondaryContainer: AppColors.secondaryContainer,
    tertiary: AppColors.tertiary,
    tertiaryContainer: AppColors.tertiaryContainer,
    surface: AppColors.surface,
    surfaceVariant: AppColors.surfaceVariant,
    error: AppColors.highRisk,
    errorContainer: AppColors.highRiskContainer,
  );

  return ThemeData(
    useMaterial3: true,
    colorScheme: colorScheme,
    scaffoldBackgroundColor: AppColors.background,
    fontFamily: GoogleFonts.nunito().fontFamily,
    textTheme: TextTheme(
      displayLarge: AppTextStyles.displayLarge,
      displayMedium: AppTextStyles.displayMedium,
      headlineMedium: AppTextStyles.headline,
      titleLarge: AppTextStyles.title,
      bodyLarge: AppTextStyles.bodyLarge,
      bodyMedium: AppTextStyles.bodyMedium,
      labelLarge: AppTextStyles.label,
      bodySmall: AppTextStyles.caption,
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        minimumSize: const Size.fromHeight(56),
        textStyle: AppTextStyles.label.copyWith(color: Colors.white),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.button),
        ),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: AppColors.primary,
        side: const BorderSide(color: AppColors.primary),
        minimumSize: const Size.fromHeight(56),
        textStyle: AppTextStyles.label.copyWith(color: AppColors.primary),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.button),
        ),
      ),
    ),
    navigationBarTheme: NavigationBarThemeData(
      backgroundColor: Colors.white,
      indicatorColor: AppColors.primaryContainer,
      labelTextStyle: MaterialStateProperty.all(AppTextStyles.label),
    ),
  );
}