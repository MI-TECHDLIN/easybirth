// ai_processing_screen.dart
// S08 — AI Processing State
// Drop into: lib/screens/ai_processing_screen.dart

import 'dart:async';
import 'package:flutter/material.dart';
import '../theme.dart';
import '../widgets/breathing_orb.dart';
import 'risk_result_screen.dart';

class AiProcessingScreen extends StatefulWidget {
  /// Injected by the inference pipeline once TFLite / risk classification
  /// completes. Defaults to a demo HIGH RISK result for the prototype.
  final RiskLevel? seedResultLevel;

  const AiProcessingScreen({super.key, this.seedResultLevel});

  @override
  State<AiProcessingScreen> createState() => _AiProcessingScreenState();
}

class _AiProcessingScreenState extends State<AiProcessingScreen> {
  Timer? _dotsTimer;
  Timer? _navigateTimer;
  int _dotCount = 1;

  @override
  void initState() {
    super.initState();

    _dotsTimer = Timer.periodic(const Duration(milliseconds: 600), (_) {
      setState(() => _dotCount = (_dotCount % 3) + 1);
    });

    // Simulated 1-3s on-device inference window. Replace with a callback
    // from the tflite_flutter compute() isolate on inference complete.
    _navigateTimer = Timer(const Duration(milliseconds: 1800), () {
      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => RiskResultScreen(
            riskLevel: widget.seedResultLevel ?? RiskLevel.high,
            symptoms: const [
              'Severe headache',
              'Swollen hands',
              'Blurred vision',
            ],
            transcript:
                '"Ina jin ciwon kai sosai... idanuna na gani duhun-...',
          ),
        ),
      );
    });
  }

  @override
  void dispose() {
    _dotsTimer?.cancel();
    _navigateTimer?.cancel();
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
                  const Icon(Icons.lock_outline, color: Colors.white38, size: 16),
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