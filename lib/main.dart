// main.dart
// Drop into: lib/main.dart
// App entry point — decides between Loading / Onboarding / Sign Up / Home
// based on persisted flags in SharedPreferences.

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'config/supabase_config.dart';
import 'theme.dart';
import 'screens/home_screen.dart';
import 'screens/onboarding_screen.dart';
import 'screens/sign_up_screen.dart';
import 'services/supabase_service.dart';
import 'services/storage_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await StorageService.init();
  if (isSupabaseConfigured) {
    await SupabaseService.init(url: supabaseUrl, anonKey: supabaseAnonKey);
  }
  runApp(const EasyBirthApp());
}

class EasyBirthApp extends StatefulWidget {
  const EasyBirthApp({super.key});

  @override
  State<EasyBirthApp> createState() => _EasyBirthAppState();
}

class _EasyBirthAppState extends State<EasyBirthApp> {
  bool _isLoading = true;
  bool _showOnboarding = false;

  // NEW: true once onboarding is done but the user hasn't verified their
  // phone number yet (i.e. hasn't completed Sign Up + OTP).
  bool _showAuth = false;

  @override
  void initState() {
    super.initState();
    _loadAppState();
  }

  Future<void> _loadAppState() async {
    final prefs = await SharedPreferences.getInstance();
    final hasSeenOnboarding = prefs.getBool('hasSeenOnboarding') ?? false;
    final isVerified = prefs.getBool('isVerified') ?? false;
    if (!mounted) return;
    setState(() {
      _showOnboarding = !hasSeenOnboarding;
      _showAuth = hasSeenOnboarding && !isVerified;
      _isLoading = false;
    });
  }

  Future<void> _finishOnboarding() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('hasSeenOnboarding', true);
    if (!mounted) return;
    setState(() {
      _showOnboarding = false;
      _showAuth = true; // send the user into Sign Up next, not straight Home
    });
  }

  @override
  Widget build(BuildContext context) {
    Widget screen;
    if (_isLoading) {
      screen = const Scaffold(body: Center(child: CircularProgressIndicator()));
    } else if (_showOnboarding) {
      screen = OnboardingScreen(
        onComplete: _finishOnboarding,
        onSkip: _finishOnboarding,
      );
    } else if (_showAuth) {
      // SignUpScreen -> OtpVerificationScreen handles the rest of the auth
      // flow internally (pushed via Navigator) and persists 'isVerified'
      // to SharedPreferences once the code is confirmed, then routes to
      // HomeScreen. See otp_verification_screen.dart.
      screen = const SignUpScreen();
    } else {
      screen = const HomeScreen();
    }

    return MaterialApp(
      title: 'easybirth',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: screen,
    );
  }
}
