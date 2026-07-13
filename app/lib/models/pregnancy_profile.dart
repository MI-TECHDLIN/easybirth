class PregnancyProfile {
  final String patientId;
  final String patientName;
  final String phoneNumber;
  final DateTime lastMenstrualPeriod;

  const PregnancyProfile({
    required this.patientId,
    required this.patientName,
    required this.phoneNumber,
    required this.lastMenstrualPeriod,
  });

  factory PregnancyProfile.fromJson(Map<String, dynamic> json) {
    return PregnancyProfile(
      patientId: json['patientId'] as String,
      patientName: json['patientName'] as String,
      phoneNumber: json['phoneNumber'] as String,
      lastMenstrualPeriod: DateTime.parse(
        json['lastMenstrualPeriod'] as String,
      ),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'patientId': patientId,
      'patientName': patientName,
      'phoneNumber': phoneNumber,
      'lastMenstrualPeriod': lastMenstrualPeriod.toIso8601String(),
    };
  }

  DateTime get estimatedDueDate =>
      lastMenstrualPeriod.add(const Duration(days: 280));

  int get currentGestationalDay {
    final days = DateTime.now().difference(lastMenstrualPeriod).inDays;
    if (days < 0) return 0;
    if (days > 280) return 280;
    return days;
  }

  int get currentGestationalWeek {
    return (currentGestationalDay / 7).floor() + 1;
  }

  int get daysRemaining {
    final remaining = estimatedDueDate.difference(DateTime.now()).inDays;
    return remaining < 0 ? 0 : remaining;
  }

  String get trimester {
    if (currentGestationalWeek <= 12) return '1st trimester';
    if (currentGestationalWeek <= 26) return '2nd trimester';
    return '3rd trimester';
  }
}
