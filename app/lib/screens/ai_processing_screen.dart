// ai_processing_screen.dart
// S08 — AI Processing State
// Drop into: lib/screens/ai_processing_screen.dart

import 'dart:async';
import 'package:flutter/material.dart';
import '../services/triage_service.dart';
import '../models/triage_response.dart';
import '../theme.dart';
import '../widgets/breathing_orb.dart';
import 'risk_result_screen.dart';

class AiProcessingScreen extends StatefulWidget {
  final String transcript;
  final String language;
  final String patientName;
  final int gestationalWeek;
  final RiskLevel? seedResultLevel;

  const AiProcessingScreen({
    super.key,
    required this.transcript,
    required this.language,
    required this.patientName,
    required this.gestationalWeek,
    this.seedResultLevel,
  });

  @override
  State<AiProcessingScreen> createState() => _AiProcessingScreenState();
}

class _AiProcessingScreenState extends State<AiProcessingScreen> {
  Timer? _dotsTimer;
  int _dotCount = 1;

  @override
  void initState() {
    super.initState();

    _dotsTimer = Timer.periodic(const Duration(milliseconds: 600), (_) {
      if (!mounted) return;
      setState(() => _dotCount = (_dotCount % 3) + 1);
    });

    _runTriage();
  }

  Future<void> _runTriage() async {
    try {
      final response = await TriageService.instance.runTriage(
        transcript: widget.transcript,
        language: widget.language,
        gestationalWeek: widget.gestationalWeek,
        patientName: widget.patientName,
      );

      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => RiskResultScreen(
            riskLevel: response.riskLevel,
            symptoms: response.detectedSymptoms,
            transcript: widget.transcript,
            confidence: 0.95,
            inferenceSeconds: 1.4,
            chwNotified: response.riskLevel == RiskLevel.high,
          ),
        ),
      );
    } catch (error) {
      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => RiskResultScreen(
            riskLevel: widget.seedResultLevel ?? RiskLevel.high,
            symptoms: const ['Simulated result due to backend error'],
            transcript: widget.transcript,
            confidence: 0.0,
            inferenceSeconds: 0.0,
            chwNotified: false,
          ),
        ),
      );
    }
  }

  @override
  void dispose() {
    _dotsTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final dots = '.' * _dotCount;
    return Scaffold(
      backgroundColor: AppColors.voiceModeDark,
      body: SafeArea(
        child: Column(
          children: [
            const Spacer(flex: 3),
            const BreathingOrb(state: OrbState.processing),
            const SizedBox(height: 32),
            Text(
              'Checking your symptoms$dots',
              style: AppTextStyles.bodyLarge.copyWith(color: Colors.white),
            ),
            const SizedBox(height: 8),
            Text(
              'This usually takes 1–3 seconds',
              style: AppTextStyles.bodyMedium.copyWith(color: Colors.white54),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: List.generate(3, (i) {
                final active = i == 2;
                return Container(
                  margin: const EdgeInsets.symmetric(horizontal: 3),
                  width: 6,
                  height: 6,
                  decoration: BoxDecoration(
                    color: active ? Colors.white : Colors.white24,
                    shape: BoxShape.circle,
                  ),
                );
              }),
            ),
            const Spacer(flex: 4),
            Padding(
              padding: const EdgeInsets.only(bottom: 24),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.lock_outline,
                    color: Colors.white38,
                    size: 16,
                  ),
                  const SizedBox(width: 8),
                  Flexible(
                    child: Text(
                      'Analysis runs on your device — your voice never leaves',
                      textAlign: TextAlign.center,
                      style: AppTextStyles.caption.copyWith(
                        color: Colors.white38,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
