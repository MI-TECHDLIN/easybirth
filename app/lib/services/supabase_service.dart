import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/pregnancy_profile.dart';
import '../models/vaccine_schedule.dart';

class SupabaseService {
  static const String patientTable = 'patients';
  static const String vaccineTable = 'vaccine_doses';

  static SupabaseClient get client => Supabase.instance.client;

  static Future<void> init({
    required String url,
    required String anonKey,
  }) async {
    await Supabase.initialize(url: url, anonKey: anonKey);
  }

  static Future<void> syncPatientProfile(PregnancyProfile profile) async {
    await client.from(patientTable).upsert({
      'id': profile.patientId,
      'name': profile.patientName,
      'phone': profile.phoneNumber,
      'last_menstrual_period': profile.lastMenstrualPeriod.toIso8601String(),
    });
  }

  static Future<void> syncScheduleEntries(
    PregnancyProfile profile,
    List<ScheduleEntry> entries,
  ) async {
    final payload = entries.map((entry) {
      return {
        'patient_id': profile.patientId,
        'dose_code': entry.code,
        'scheduled_date': entry
            .scheduledDate(profile.lastMenstrualPeriod)
            .toIso8601String(),
        'administered_date': entry.completedDate?.toIso8601String(),
        'status': entry.status.name,
      };
    }).toList();

    await client.from(vaccineTable).upsert(payload);
  }
}
