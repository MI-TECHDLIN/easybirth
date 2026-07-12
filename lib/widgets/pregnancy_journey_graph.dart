import 'package:flutter/material.dart';
import '../models/pregnancy_day.dart';
import '../models/pregnancy_profile.dart';
import '../models/vaccine_schedule.dart';
import '../theme.dart';

class PregnancyJourneyGraph extends StatefulWidget {
  final PregnancyProfile profile;
  final List<ScheduleEntry> schedule;

  const PregnancyJourneyGraph({
    super.key,
    required this.profile,
    required this.schedule,
  });

  @override
  State<PregnancyJourneyGraph> createState() => _PregnancyJourneyGraphState();
}

class _PregnancyJourneyGraphState extends State<PregnancyJourneyGraph> {
  late List<ScheduleEntry> entries;

  @override
  void initState() {
    super.initState();
    final today = DateTime.now();
    entries = widget.schedule.map((entry) {
      final status = entry.completedDate != null
          ? DoseStatus.completed
          : entry.computeStatus(today, widget.profile.lastMenstrualPeriod);
      return entry.copyWith(status: status);
    }).toList();
  }

  void _markCompleted(ScheduleEntry entry) {
    setState(() {
      entries = entries.map((e) {
        if (e.code == entry.code) {
          return e.copyWith(
            status: DoseStatus.completed,
            completedDate: DateTime.now(),
          );
        }
        return e;
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    final today = DateTime.now();
    final calendar = buildPregnancyCalendar(widget.profile, entries);
    final todayIndex = calendar.indexWhere((day) {
      return day.calendarDate.year == today.year &&
          day.calendarDate.month == today.month &&
          day.calendarDate.day == today.day;
    });

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Pregnancy Journey', style: AppTextStyles.headline),
        const SizedBox(height: 12),
        Expanded(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: GridView.builder(
              scrollDirection: Axis.horizontal,
              physics: const BouncingScrollPhysics(),
              itemCount: calendar.length,
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 7,
                crossAxisSpacing: 4,
                mainAxisSpacing: 4,
                childAspectRatio: 1,
              ),
              itemBuilder: (context, index) {
                final day = calendar[index];
                final isToday = index == todayIndex;
                return _DayCell(
                  day: day,
                  isToday: isToday,
                  onTap: day.events.isEmpty
                      ? null
                      : () => _showEntryDetails(context, day),
                );
              },
            ),
          ),
        ),
      ],
    );
  }

  void _showEntryDetails(BuildContext context, PregnancyDay day) {
    final entry = day.events.first;
    final scheduledDate = entry.scheduledDate(
      widget.profile.lastMenstrualPeriod,
    );
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(entry.label, style: AppTextStyles.headline),
              const SizedBox(height: 10),
              Text(
                'Due date: ${scheduledDate.day.toString().padLeft(2, '0')}/${scheduledDate.month.toString().padLeft(2, '0')}/${scheduledDate.year}',
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                'Status: ${entry.status.name.replaceAll(RegExp(r'([A-Z])'), ' ').trim()}',
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: 20),
              FilledButton(
                onPressed: entry.status == DoseStatus.completed
                    ? null
                    : () {
                        Navigator.of(context).pop();
                        _markCompleted(entry);
                      },
                child: Text(
                  entry.status == DoseStatus.completed
                      ? 'Already completed'
                      : 'Mark as completed',
                ),
              ),
              const SizedBox(height: 16),
            ],
          ),
        );
      },
    );
  }
}

class _DayCell extends StatelessWidget {
  final PregnancyDay day;
  final bool isToday;
  final VoidCallback? onTap;

  const _DayCell({required this.day, required this.isToday, this.onTap});

  @override
  Widget build(BuildContext context) {
    final color = _cellColor(day);
    final border = isToday
        ? Border.all(color: AppColors.secondary, width: 2)
        : Border.all(color: Colors.transparent);

    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: color,
          border: border,
          borderRadius: BorderRadius.circular(6),
        ),
        child: Center(
          child: day.events.isNotEmpty
              ? Icon(
                  _cellIcon(day.events.first.status),
                  size: 14,
                  color: day.events.first.status == DoseStatus.completed
                      ? Colors.white
                      : AppColors.textPrimary,
                )
              : const SizedBox.shrink(),
        ),
      ),
    );
  }

  Color _cellColor(PregnancyDay day) {
    if (day.events.isEmpty) {
      return AppColors.surfaceVariant;
    }

    switch (day.events.first.status) {
      case DoseStatus.upcoming:
      case DoseStatus.dueSoon:
        return AppColors.tertiaryContainer;
      case DoseStatus.completed:
        return AppColors.safeRiskContainer;
      case DoseStatus.missed:
        return AppColors.highRiskContainer;
    }
  }

  IconData _cellIcon(DoseStatus status) {
    switch (status) {
      case DoseStatus.upcoming:
      case DoseStatus.dueSoon:
        return Icons.calendar_today;
      case DoseStatus.completed:
        return Icons.check;
      case DoseStatus.missed:
        return Icons.close;
    }
  }
}
