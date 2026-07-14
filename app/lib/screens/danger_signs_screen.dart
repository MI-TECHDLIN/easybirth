import 'package:flutter/material.dart';
import '../theme.dart';
import 'voice_listening_screen.dart';
import 'package:uuid/uuid.dart';

class DangerSignsScreen extends StatelessWidget {
  final String languageLabel;

  const DangerSignsScreen({super.key, this.languageLabel = 'Hausa'});

  void _openVoiceTriage(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => VoiceListeningScreen(
          languageLabel: languageLabel,
          sessionId: const Uuid().v4(),
          conversationHistory: const [],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Danger Signs'),
        backgroundColor: AppColors.surface,
        elevation: 0,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.highRiskContainer,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  'If you notice any of these signs, go to the health centre immediately.',
                  style: AppTextStyles.bodyLarge.copyWith(
                    color: AppColors.highRisk,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Expanded(
                child: ListView(
                  children: const [
                    _DangerTile(
                      title: 'Severe headache',
                      description:
                          'A bad headache that does not go away could be a sign of pre-eclampsia.',
                      icon: Icons.headphones,
                    ),
                    _DangerTile(
                      title: 'Swollen face or hands',
                      description:
                          'Sudden swelling may indicate a serious blood pressure problem.',
                      icon: Icons.pan_tool,
                    ),
                    _DangerTile(
                      title: 'Blurred vision or seeing spots',
                      description:
                          'Changes to your eyesight can be a warning sign during pregnancy.',
                      icon: Icons.visibility,
                    ),
                    _DangerTile(
                      title: 'Heavy vaginal bleeding',
                      description:
                          'Heavy bleeding in pregnancy needs immediate medical attention.',
                      icon: Icons.bloodtype,
                    ),
                    _DangerTile(
                      title: 'High fever',
                      description:
                          'A high fever can signal infection and must be checked quickly.',
                      icon: Icons.thermostat,
                    ),
                    _DangerTile(
                      title: 'Baby not moving',
                      description:
                          'A decrease in baby movement is concerning and should be evaluated.',
                      icon: Icons.baby_changing_station,
                    ),
                  ],
                ),
              ),
              FilledButton.icon(
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(56),
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                ),
                onPressed: () => _openVoiceTriage(context),
                icon: const Icon(Icons.mic),
                label: const Text('Speak your symptoms'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _DangerTile extends StatelessWidget {
  final String title;
  final String description;
  final IconData icon;

  const _DangerTile({
    required this.title,
    required this.description,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: ExpansionTile(
        leading: CircleAvatar(
          backgroundColor: AppColors.primaryContainer,
          child: Icon(icon, color: AppColors.primary),
        ),
        title: Text(title, style: AppTextStyles.title.copyWith(fontSize: 16)),
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              description,
              style: AppTextStyles.bodyMedium.copyWith(
                color: AppColors.textSecondary,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
