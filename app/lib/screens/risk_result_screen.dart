// risk_result_screen.dart
// S05 — Risk Result
// Drop into: lib/screens/risk_result_screen.dart

import 'package:flutter/material.dart';
import '../models/triage_response.dart';
import '../theme.dart';
import 'home_screen.dart';

class RiskResultScreen extends StatelessWidget {
  final RiskLevel riskLevel;
  final List<String> symptoms;
  final String transcript;
  final String recommendation;
  final String? reasoning;
  final double confidence; // 0.0 - 1.0
  final double inferenceSeconds;
  final bool chwNotified;

  const RiskResultScreen({
    super.key,
    required this.riskLevel,
    required this.symptoms,
    required this.transcript,
    required this.recommendation,
    this.reasoning,
    this.confidence = 0.94,
    this.inferenceSeconds = 0.8,
    this.chwNotified = true,
  });

  factory RiskResultScreen.fromTriageResponse(
    TriageResponse response, {
    required String transcript,
    double confidence = 0.94,
    double inferenceSeconds = 0.8,
    bool chwNotified = true,
  }) {
    return RiskResultScreen(
      riskLevel: response.riskLevel,
      symptoms: response.detectedSymptoms,
      transcript: transcript,
      recommendation:
          response.recommendation ?? response.riskLevel.recommendation,
      reasoning: response.reasoning,
      confidence: confidence,
      inferenceSeconds: inferenceSeconds,
      chwNotified: chwNotified,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.surface,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => Navigator.of(context).pushAndRemoveUntil(
            MaterialPageRoute(builder: (_) => const HomeScreen()),
            (route) => false,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(
              Icons.share_outlined,
              color: AppColors.textPrimary,
            ),
            onPressed: () {
              // Hand off to CHW / share sheet — wire up share_plus here.
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _RecordingBar(transcript: transcript),
            const SizedBox(height: 24),
            Center(child: _RiskPill(riskLevel: riskLevel)),
            const SizedBox(height: 16),
            Text(
              recommendation,
              textAlign: TextAlign.center,
              style: AppTextStyles.bodyMedium,
            ),
            const SizedBox(height: 12),
            Center(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(
                    Icons.help_outline,
                    size: 14,
                    color: AppColors.secondary,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    'AI Confidence: ${(confidence * 100).round()}%',
                    style: AppTextStyles.caption.copyWith(
                      color: AppColors.secondary,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text('|', style: AppTextStyles.caption),
                  const SizedBox(width: 8),
                  Text(
                    '${inferenceSeconds}s on-device',
                    style: AppTextStyles.monoData.copyWith(
                      fontSize: 12,
                      color: AppColors.outline,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Symptoms heard',
              style: AppTextStyles.caption.copyWith(letterSpacing: 0.4),
            ),
            const SizedBox(height: 10),
            SizedBox(
              height: 40,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                itemCount: symptoms.length,
                separatorBuilder: (_, _) => const SizedBox(width: 8),
                itemBuilder: (context, i) {
                  return Chip(
                    label: Text(symptoms[i], style: AppTextStyles.label),
                    backgroundColor: AppColors.surfaceVariant,
                    side: BorderSide.none,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 20),
            _RecommendationCard(riskLevel: riskLevel),
            if (reasoning != null && reasoning!.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(
                'Why this recommendation?',
                style: AppTextStyles.caption.copyWith(
                  color: AppColors.textSecondary,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                reasoning!,
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
            ],
            if (chwNotified) ...[
              const SizedBox(height: 16),
              const _ChwBanner(),
            ],
            const SizedBox(height: 24),
            FilledButton.icon(
              style: FilledButton.styleFrom(
                backgroundColor: riskLevel == RiskLevel.high
                    ? AppColors.highRisk
                    : AppColors.primary,
              ),
              onPressed: () {
                // Navigate to PHC Referral Finder (S12).
              },
              icon: const Icon(Icons.location_on_outlined, color: Colors.white),
              label: const Text('Find Nearest Health Centre'),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () {
                // Launch tel: URI to CHW via url_launcher.
              },
              icon: const Icon(Icons.call_outlined),
              label: const Text('Call CHW'),
            ),
            const SizedBox(height: 12),
            Center(
              child: TextButton(
                onPressed: () {
                  // Navigate to Danger Signs Education (S09).
                },
                child: Text(
                  'Learn about these symptoms',
                  style: AppTextStyles.label.copyWith(
                    color: AppColors.secondary,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _RecordingBar extends StatelessWidget {
  final String transcript;
  const _RecordingBar({required this.transcript});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.voiceModeDark,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: const BoxDecoration(
              color: AppColors.primaryContainer,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 10),
          const Icon(
            Icons.graphic_eq,
            color: AppColors.primaryContainer,
            size: 20,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              transcript,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: AppTextStyles.bodyMedium.copyWith(
                color: Colors.white70,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
          const SizedBox(width: 8),
          TextButton.icon(
            style: TextButton.styleFrom(
              foregroundColor: Colors.white,
              backgroundColor: AppColors.primary,
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
            ),
            onPressed: () {
              // Replay recorded audio via just_audio.
            },
            icon: const Icon(Icons.play_arrow, size: 16),
            label: Text(
              'Replay',
              style: AppTextStyles.label.copyWith(
                color: Colors.white,
                fontSize: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _RiskPill extends StatelessWidget {
  final RiskLevel riskLevel;
  const _RiskPill({required this.riskLevel});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 56,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      decoration: BoxDecoration(
        color: riskLevel.containerColor,
        borderRadius: BorderRadius.circular(28),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(riskLevel.icon, style: const TextStyle(fontSize: 20)),
          const SizedBox(width: 10),
          Text(
            riskLevel.label,
            style: AppTextStyles.title.copyWith(
              color: riskLevel.color,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}

class _RecommendationCard extends StatelessWidget {
  final RiskLevel riskLevel;
  const _RecommendationCard({required this.riskLevel});

  String get _title {
    switch (riskLevel) {
      case RiskLevel.high:
        return 'Go to your nearest health centre now';
      case RiskLevel.moderate:
        return 'Rest and watch these signs closely';
      case RiskLevel.low:
        return 'Keep your next ANC appointment';
    }
  }

  String get _subtitle {
    switch (riskLevel) {
      case RiskLevel.high:
        return 'Tell them about your symptoms when you arrive';
      case RiskLevel.moderate:
        return 'Call your CHW if they get worse in the next few hours';
      case RiskLevel.low:
        return 'Continue eating well and attending checkups';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border(left: BorderSide(color: riskLevel.color, width: 3)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            _title,
            style: AppTextStyles.title.copyWith(fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 4),
          Text(
            _subtitle,
            style: AppTextStyles.bodyMedium.copyWith(
              color: AppColors.textSecondary,
            ),
          ),
        ],
      ),
    );
  }
}

class _ChwBanner extends StatelessWidget {
  const _ChwBanner();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.safeRiskContainer,
        borderRadius: BorderRadius.circular(16),
        border: const Border(
          left: BorderSide(color: AppColors.safeRisk, width: 3),
        ),
      ),
      child: Row(
        children: [
          const Icon(Icons.check_circle, color: AppColors.primary, size: 18),
          const SizedBox(width: 8),
          Text(
            'Your CHW has been notified ✓',
            style: AppTextStyles.label.copyWith(color: AppColors.primary),
          ),
          const Spacer(),
          Text('2 min ago', style: AppTextStyles.caption),
        ],
      ),
    );
  }
}
