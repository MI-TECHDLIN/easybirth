class ConversationTurn {
  final String role;
  final String content;

  ConversationTurn({required this.role, required this.content});

  factory ConversationTurn.fromJson(Map<String, dynamic> json) {
    return ConversationTurn(
      role: json['role'] as String? ?? 'user',
      content: json['content'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {'role': role, 'content': content};
  }
}
