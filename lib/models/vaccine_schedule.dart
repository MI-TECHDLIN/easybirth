enum DoseType { anc, vaccine }

enum DoseStatus { upcoming, dueSoon, completed, missed }

class ScheduleEntry {
  final String code;
  final DoseType type;
  final int scheduledWeek;
  final int scheduledDayOfWeek;
  final String label;
  final DateTime? completedDate;
  final DoseStatus status;

  ScheduleEntry({
    required this.code,
    required this.type,
    required this.scheduledWeek,
    this.scheduledDayOfWeek = 1,
    required this.label,
    this.completedDate,
    this.status = DoseStatus.upcoming,
  });

  ScheduleEntry copyWith({DateTime? completedDate, DoseStatus? status}) {
    return ScheduleEntry(
      code: code,
      type: type,
      scheduledWeek: scheduledWeek,
      scheduledDayOfWeek: scheduledDayOfWeek,
      label: label,
      completedDate: completedDate ?? this.completedDate,
      status: status ?? this.status,
    );
  }

  DateTime scheduledDate(DateTime lmp) {
    final daysFromLmp = (scheduledWeek - 1) * 7 + (scheduledDayOfWeek - 1);
    return lmp.add(Duration(days: daysFromLmp));
  }

  DoseStatus computeStatus(DateTime today, DateTime lmp) {
    if (completedDate != null) return DoseStatus.completed;

    final scheduled = scheduledDate(lmp);
    final delta = scheduled.difference(today).inDays;
    if (delta < 0) return DoseStatus.missed;
    if (delta <= 7) return DoseStatus.dueSoon;
    return DoseStatus.upcoming;
  }
}

final List<ScheduleEntry> defaultSchedule = [
  ScheduleEntry(
    code: 'anc_1',
    type: DoseType.anc,
    scheduledWeek: 12,
    label: 'ANC contact 1/8',
  ),
  ScheduleEntry(
    code: 'tt1',
    type: DoseType.vaccine,
    scheduledWeek: 12,
    scheduledDayOfWeek: 3,
    label: 'TT1 – Tetanus Toxoid',
  ),
  ScheduleEntry(
    code: 'tt2',
    type: DoseType.vaccine,
    scheduledWeek: 16,
    scheduledDayOfWeek: 3,
    label: 'TT2 – Tetanus Toxoid',
  ),
  ScheduleEntry(
    code: 'anc_2',
    type: DoseType.anc,
    scheduledWeek: 20,
    label: 'ANC contact 2/8',
  ),
  ScheduleEntry(
    code: 'anc_3',
    type: DoseType.anc,
    scheduledWeek: 26,
    label: 'ANC contact 3/8',
  ),
  ScheduleEntry(
    code: 'anc_4',
    type: DoseType.anc,
    scheduledWeek: 30,
    label: 'ANC contact 4/8',
  ),
  ScheduleEntry(
    code: 'anc_5',
    type: DoseType.anc,
    scheduledWeek: 34,
    label: 'ANC contact 5/8',
  ),
  ScheduleEntry(
    code: 'anc_6',
    type: DoseType.anc,
    scheduledWeek: 36,
    label: 'ANC contact 6/8',
  ),
  ScheduleEntry(
    code: 'anc_7',
    type: DoseType.anc,
    scheduledWeek: 38,
    label: 'ANC contact 7/8',
  ),
  ScheduleEntry(
    code: 'anc_8',
    type: DoseType.anc,
    scheduledWeek: 40,
    label: 'ANC contact 8/8',
  ),
];
