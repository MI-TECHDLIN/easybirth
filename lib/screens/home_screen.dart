// home_screen.dart
// S03 — Home / Voice Entry
// Drop into: lib/screens/home_screen.dart

import 'package:flutter/material.dart';
import '../../theme.dart';
import '../../widgets/breathing_orb.dart';
import 'voice_listening_screen.dart';

class HomeScreen extends StatefulWidget {
  final String userName;
  final int gestationalWeek;
  final String languageCode; // e.g. 'ha' for Hausa

  const HomeScreen({
    super.key,
    this.userName = 'Amina',
    this.gestationalWeek = 30,
    this.languageCode = 'ha',
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _navIndex = 0;

  // Suggestion chips keyed by language. Extend with more languages as
  // translations become available.
  static const Map<String, List<String>> _suggestionsByLanguage = {
    'ha': ['Ina jin ciwon kai', 'Hannuna yana kumbura', 'Ina jin zafi'],
    'yo': ['Mo ni efori', 'Owo mi n wu', 'Ara mi n gbona'],
    'ig': ['Ana m enwe isi ọwụwa', 'Aka m na-afụ', 'Ana m ekpo ọkụ'],
    'pcm': ['My head dey pain me', 'My hand dey swell', 'My body hot'],
  };

  List<String> get _suggestions =>
      _suggestionsByLanguage[widget.languageCode] ??
      _suggestionsByLanguage['ha']!;

  void _openVoiceTriage({String? prefillText}) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => VoiceListeningScreen(
          languageLabel: 'Hausa',
          prefillTranscript: prefillText,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Column(
          children: [
            // Greeting row
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          'Good morning, ${widget.userName} 👋',
                          style: AppTextStyles.headline,
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 14,
                          vertical: 8,
                        ),
                        decoration: BoxDecoration(
                          color: AppColors.primaryContainer,
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          '${widget.gestationalWeek} wks',
                          style: AppTextStyles.label.copyWith(
                            color: AppColors.primary,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Week ${widget.gestationalWeek} of your pregnancy',
                    style: AppTextStyles.bodyMedium.copyWith(
                      color: AppColors.textSecondary,
                    ),
                  ),
                ],
              ),
            ),

            // Orb hero — center of remaining space
            Expanded(
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    BreathingOrb(
                      state: OrbState.idle,
                      onTap: () => _openVoiceTriage(),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      'Tap to speak your symptoms',
                      style: AppTextStyles.bodyMedium.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: List.generate(
                        3,
                        (i) => Container(
                          margin: const EdgeInsets.symmetric(horizontal: 3),
                          width: 6,
                          height: 6,
                          decoration: const BoxDecoration(
                            color: AppColors.outline,
                            shape: BoxShape.circle,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Suggestion chips
            Padding(
              padding: const EdgeInsets.only(left: 16, bottom: 8),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'HAUSA SUGGESTIONS',
                  style: AppTextStyles.caption.copyWith(
                    letterSpacing: 0.6,
                  ),
                ),
              ),
            ),
            SizedBox(
              height: 44,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: _suggestions.length,
                separatorBuilder: (_, __) => const SizedBox(width: 10),
                itemBuilder: (context, index) {
                  final text = _suggestions[index];
                  final selected = index == 0;
                  return ActionChip(
                    label: Text(text, style: AppTextStyles.label),
                    backgroundColor: selected
                        ? AppColors.primaryContainer
                        : Colors.transparent,
                    side: BorderSide(
                      color: selected
                          ? Colors.transparent
                          : AppColors.outline.withOpacity(0.4),
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    onPressed: () => _openVoiceTriage(prefillText: text),
                  );
                },
              ),
            ),
            const SizedBox(height: 8),
          ],
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _navIndex,
        onDestinationSelected: (i) => setState(() => _navIndex = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.medical_services_outlined), selectedIcon: Icon(Icons.medical_services), label: 'Triage'),
          NavigationDestination(icon: Icon(Icons.menu_book_outlined), selectedIcon: Icon(Icons.menu_book), label: 'Learn'),
          NavigationDestination(icon: Icon(Icons.calendar_today_outlined), selectedIcon: Icon(Icons.calendar_today), label: 'ANC'),
        ],
      ),
    );
  }
}