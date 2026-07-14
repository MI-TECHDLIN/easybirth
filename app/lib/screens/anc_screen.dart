import 'package:flutter/material.dart';
import '../models/pregnancy_profile.dart';
import '../models/vaccine_schedule.dart';
import '../widgets/pregnancy_journey_graph.dart';
import '../widgets/progress_tracker_card.dart';
import '../theme.dart';

class AncScreen extends StatelessWidget {
  final PregnancyProfile profile;
  final List<ScheduleEntry> schedule;

  const AncScreen({super.key, required this.profile, required this.schedule});

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
              Text('ANC & Vaccine Plan', style: AppTextStyles.headline),
              const SizedBox(height: 12),
              Text(
                'Track your appointments and vaccines in one place.',
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: 20),
              ProgressTrackerCard(profile: profile, schedule: schedule),
              const SizedBox(height: 20),
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(16),
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
                      Text('Pregnancy Journey', style: AppTextStyles.title),
                      const SizedBox(height: 16),
                      Expanded(
                        child: PregnancyJourneyGraph(
                          profile: profile,
                          schedule: schedule,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
