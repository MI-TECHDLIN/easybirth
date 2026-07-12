import 'package:flutter/material.dart';
import '../models/pregnancy_profile.dart';
import '../models/vaccine_schedule.dart';
import '../theme.dart';

class ProgressTrackerCard extends StatelessWidget {
  final PregnancyProfile profile;
  final List<ScheduleEntry> schedule;

  const ProgressTrackerCard({
    super.key,
    required this.profile,
    required this.schedule,
  });

  @override
  Widget build(BuildContext context) {
    final today = DateTime.now();
    final entries = schedule.map((entry) {
      final status = entry.completedDate != null
          ? DoseStatus.completed
          : entry.computeStatus(today, profile.lastMenstrualPeriod);
      return entry.copyWith(status: status);
    }).toList();

    final upcomingCount = entries
        .where((entry) => entry.status == DoseStatus.upcoming)
        .length;
    final dueSoonCount = entries
        .where((entry) => entry.status == DoseStatus.dueSoon)
        .length;
    final missedCount = entries
        .where((entry) => entry.status == DoseStatus.missed)
        .length;

    final summaryParts = <String>[];
    if (upcomingCount + dueSoonCount > 0) {
      summaryParts.add(
        '${upcomingCount + dueSoonCount} upcoming ${upcomingCount + dueSoonCount == 1 ? 'item' : 'items'}',
      );
    }
    if (missedCount > 0) {
      summaryParts.add('$missedCount missed');
    }
    final summary = summaryParts.isEmpty
        ? 'All scheduled items are on track.'
        : summaryParts.join(' · ');

    final progress = (profile.currentGestationalWeek / 40).clamp(0.0, 1.0);

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
          Row(
            children: [
              _ProgressRing(progress: progress),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${profile.currentGestationalWeek} / 40 weeks',
                      style: AppTextStyles.headline,
                    ),
                    const SizedBox(height: 6),
                    Chip(
                      label: Text(profile.trimester),
                      backgroundColor: AppColors.secondaryContainer,
                      labelStyle: AppTextStyles.label.copyWith(
                        color: AppColors.secondary,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            'Estimated due date ${_formatDate(profile.estimatedDueDate)} · ${profile.daysRemaining} days to go',
            style: AppTextStyles.bodyMedium.copyWith(
              color: AppColors.textSecondary,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            summary,
            style: AppTextStyles.bodyMedium.copyWith(
              color: AppColors.textSecondary,
            ),
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
  }
}

class _ProgressRing extends StatelessWidget {
  final double progress;

  const _ProgressRing({required this.progress});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 72,
      height: 72,
      child: Stack(
        alignment: Alignment.center,
        children: [
          CircularProgressIndicator(
            value: progress,
            strokeWidth: 8,
            color: AppColors.primary,
            backgroundColor: AppColors.surfaceVariant,
          ),
          Text(
            '${(progress * 100).round()}%',
            style: AppTextStyles.label.copyWith(color: AppColors.textPrimary),
          ),
        ],
      ),
    );
  }
}
