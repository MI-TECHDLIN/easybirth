import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';
import '../theme.dart';
import '../widgets/breathing_orb.dart';
import 'voice_listening_screen.dart';

class TriageScreen extends StatelessWidget {
  final String languageCode;

  const TriageScreen({super.key, required this.languageCode});

  void _openVoiceTriage(BuildContext context, {String? prefillText}) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => VoiceListeningScreen(
          languageLabel: _languageLabel(languageCode),
          prefillTranscript: prefillText,
          sessionId: const Uuid().v4(),
          conversationHistory: const [],
        ),
      ),
    );
  }

  String _languageLabel(String code) {
    switch (code.toLowerCase()) {
      case 'yo':
        return 'Yoruba';
      case 'ig':
        return 'Igbo';
      case 'pcm':
        return 'Pidgin';
      default:
        return 'Hausa';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Triage', style: AppTextStyles.headline),
              const SizedBox(height: 12),
              Text(
                'Speak your symptoms and get a fast pregnancy risk check from AI.',
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: 24),
              const _TriageCard(),
              const SizedBox(height: 24),
              Text('Quick suggestions', style: AppTextStyles.title),
              const SizedBox(height: 12),
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children:
                    [
                      'Ina jin ciwon kai',
                      'Hannuna yana kumbura',
                      'Ina jin zafi',
                      'Idanuna na gani duhun-duhun',
                    ].map((text) {
                      return ActionChip(
                        label: Text(text, style: AppTextStyles.label),
                        backgroundColor: AppColors.surface,
                        side: BorderSide(color: AppColors.outline),
                        onPressed: () =>
                            _openVoiceTriage(context, prefillText: text),
                      );
                    }).toList(),
              ),
              const Spacer(),
              FilledButton.icon(
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(56),
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                ),
                onPressed: () => _openVoiceTriage(context),
                icon: const Icon(Icons.mic),
                label: const Text('Start voice triage'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _TriageCard extends StatelessWidget {
  const _TriageCard();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [
          BoxShadow(
            color: Color(0x14000000),
            blurRadius: 16,
            offset: Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Voice Triage', style: AppTextStyles.title),
          const SizedBox(height: 12),
          Text(
            'Speak about your symptoms in Hausa, Yoruba, Igbo or Pidgin. The AI will ask follow-up questions if needed.',
            style: AppTextStyles.bodyMedium.copyWith(
              color: AppColors.textSecondary,
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              const Icon(
                Icons.health_and_safety_outlined,
                color: AppColors.primary,
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  'Quick risk check for maternal danger signs.',
                  style: AppTextStyles.bodyMedium,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
