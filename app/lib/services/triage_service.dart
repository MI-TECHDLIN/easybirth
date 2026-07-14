import 'package:dio/dio.dart';

import '../config/api_config.dart';
import '../models/conversation_turn.dart';
import '../models/triage_response.dart';

class TriageService {
  TriageService._();

  static final TriageService instance = TriageService._();
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: AppConfig.apiBaseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      responseType: ResponseType.json,
    ),
  );

  Future<TriageResponse> runTriage({
    required String sessionId,
    required String transcript,
    required String language,
    required List<ConversationTurn> conversationHistory,
    required int gestationalWeek,
    required String patientName,
    String? chwPhone,
  }) async {
    final payload = {
      'transcript': transcript,
      'language': language,
      'session_id': sessionId,
      'conversation_history': conversationHistory
          .map((turn) => turn.toJson())
          .toList(),
      'gestational_week': gestationalWeek,
      'patient_name': patientName,
      'chw_phone': chwPhone,
    };

    final response = await _dio.post('/api/v1/triage', data: payload);
    return TriageResponse.fromJson(response.data as Map<String, dynamic>);
  }
}
