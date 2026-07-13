import 'pregnancy_profile.dart';
import 'vaccine_schedule.dart';

class PregnancyDay {
  final int dayIndex;
  final int week;
  final int dayOfWeek;
  final DateTime calendarDate;
  final List<ScheduleEntry> events;

  PregnancyDay({
    required this.dayIndex,
    required this.week,
    required this.dayOfWeek,
    required this.calendarDate,
    required this.events,
  });

  DoseStatus get cellStatus {
    if (events.isEmpty) {
      return DoseStatus.upcoming;
    }
    return events.first.status;
  }
}

List<PregnancyDay> buildPregnancyCalendar(
  PregnancyProfile profile,
  List<ScheduleEntry> schedule,
) {
  return List.generate(280, (index) {
    final dayIndex = index + 1;
    final week = (index ~/ 7) + 1;
    final dayOfWeek = (index % 7) + 1;
    final date = profile.lastMenstrualPeriod.add(Duration(days: index));
    final events = schedule.where((entry) {
      return entry.scheduledWeek == week &&
          entry.scheduledDayOfWeek == dayOfWeek;
    }).toList();

    return PregnancyDay(
      dayIndex: dayIndex,
      week: week,
      dayOfWeek: dayOfWeek,
      calendarDate: date,
      events: events,
    );
  });
}
