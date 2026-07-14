import '../theme.dart';

class TriageResponse {
  final String decision;
  final String? followUpQuestion;
  final RiskLevel riskLevel;
  final List<String> detectedSymptoms;
  final String? recommendation;
  final String? reasoning;

  TriageResponse({
    required this.decision,
    required this.riskLevel,
    required this.detectedSymptoms,
    this.followUpQuestion,
    this.recommendation,
    this.reasoning,
  });

  factory TriageResponse.fromJson(Map<String, dynamic> json) {
    return TriageResponse(
      decision: json['decision'] as String? ?? 'conclude',
      followUpQuestion: json['follow_up_question'] as String?,
      riskLevel: _parseRiskLevel(json['risk_level'] as String?),
      detectedSymptoms:
          (json['detected_symptoms'] as List<dynamic>?)
              ?.map((item) => item.toString())
              .toList() ??
          <String>[],
      recommendation: json['recommendation'] as String?,
      reasoning: json['reasoning'] as String?,
    );
  }

  static RiskLevel _parseRiskLevel(String? value) {
    switch (value?.toUpperCase()) {
      case 'HIGH':
        return RiskLevel.high;
      case 'MODERATE':
        return RiskLevel.moderate;
      case 'LOW':
        return RiskLevel.low;
      default:
        return RiskLevel.low;
    }
  }
}
