// main.dart
// Drop into: lib/main.dart
// Entry point wiring the 4 core screens for local testing.
//
// pubspec.yaml dependency needed:
//   google_fonts: ^6.2.1

import 'package:flutter/material.dart';
import 'theme.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const EasyBirthApp());
}

class EasyBirthApp extends StatelessWidget {
  const EasyBirthApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'easybirth',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: const HomeScreen(),
    );
  }
}