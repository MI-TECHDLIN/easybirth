import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'theme.dart';
import 'screens/home_screen.dart';
import 'screens/onboarding_screen.dart';

void main() {
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

  @override
  void initState() {
    super.initState();
    _loadOnboardingState();
  }

  Future<void> _loadOnboardingState() async {
    final prefs = await SharedPreferences.getInstance();
    final hasSeenOnboarding = prefs.getBool('hasSeenOnboarding') ?? false;
    if (!mounted) return;
    setState(() {
      _showOnboarding = !hasSeenOnboarding;
      _isLoading = false;
    });
  }

  Future<void> _finishOnboarding() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('hasSeenOnboarding', true);
    if (!mounted) return;
    setState(() {
      _showOnboarding = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'easybirth',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: _isLoading
          ? const Scaffold(body: Center(child: CircularProgressIndicator()))
          : _showOnboarding
          ? OnboardingScreen(
              onComplete: _finishOnboarding,
              onSkip: _finishOnboarding,
            )
          : const HomeScreen(),
    );
  }
}
