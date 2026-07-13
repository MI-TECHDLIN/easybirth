import 'package:hive_flutter/hive_flutter.dart';
import '../models/pregnancy_profile.dart';
import '../models/vaccine_schedule.dart';

class StorageService {
  static const String _patientBox = 'patient_box';
  static const String _profileKey = 'patient_profile';
  static const String _scheduleKey = 'schedule_entries';

  static Future<void> init() async {
    await Hive.initFlutter();
    await Hive.openBox(_patientBox);
  }

  static Box get _box => Hive.box(_patientBox);

  static PregnancyProfile? loadProfile() {
    final raw = _box.get(_profileKey);
    if (raw is Map) {
      return PregnancyProfile.fromJson(Map<String, dynamic>.from(raw));
    }
    return null;
  }

  static Future<void> saveProfile(PregnancyProfile profile) async {
    await _box.put(_profileKey, profile.toJson());
  }

  static List<ScheduleEntry> loadScheduleEntries() {
    final raw = _box.get(_scheduleKey);
    if (raw is List) {
      return raw
          .whereType<Map>()
          .map(
            (entry) => ScheduleEntry.fromJson(Map<String, dynamic>.from(entry)),
          )
          .toList();
    }
    return defaultSchedule.map((entry) => entry.copyWith()).toList();
  }

  static Future<void> saveScheduleEntries(List<ScheduleEntry> entries) async {
    final payload = entries.map((entry) => entry.toJson()).toList();
    await _box.put(_scheduleKey, payload);
  }

  static Future<void> updateScheduleEntry(ScheduleEntry entry) async {
    final entries = loadScheduleEntries();
    final updated = entries
        .map((e) => e.code == entry.code ? entry : e)
        .toList();
    await saveScheduleEntries(updated);
  }
}
