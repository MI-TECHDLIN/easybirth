import 'package:dio/dio.dart';

import '../config/api_config.dart';

class ApiService {
  ApiService._();

  static final ApiService instance = ApiService._();

  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: AppConfig.apiBaseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      responseType: ResponseType.json,
    ),
  );

  Future<bool> checkHealth() async {
    try {
      final response = await _dio.get('/api/v1/health');
      return response.data['status'] == 'ok';
    } catch (error) {
      // Keep the app running even if backend is unavailable.
      print('ApiService health check failed: $error');
      return false;
    }
  }
}
