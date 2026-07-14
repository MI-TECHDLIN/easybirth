// voice_listening_screen.dart
// S04 — Voice Listening State
// Drop into: lib/screens/voice_listening_screen.dart

import 'dart:async';
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../theme.dart';
import '../widgets/breathing_orb.dart';
import 'ai_processing_screen.dart';

/// Demo transcript lines (Hausa) with English translation, matching the
/// pitch-video reference in the spec. Swap for the real speech_to_text /
/// on-device recognition stream when wiring up recording.
const List<String> _demoTranscriptLines = [
  'Ina jin ciwon kai sosai...',
  'tafin hannuna yana kumbura...',
  'idanuna na gani duhun-duhun',
];

const String _demoTranslation =
    'I have a severe headache... my palms are swelling... my vision is '
    'going dark';

class VoiceListeningScreen extends StatefulWidget {
  final String languageLabel;
  final String flagEmoji;

  /// If provided (e.g. tapped from a suggestion chip), the transcript is
  /// pre-filled instead of being built up from the simulated stream.
  final String? prefillTranscript;
  final String? promptMessage;

  const VoiceListeningScreen({
    super.key,
    this.languageLabel = 'Hausa',
    this.flagEmoji = '🇳🇬',
    this.prefillTranscript,
    this.promptMessage,
  });

  @override
  State<VoiceListeningScreen> createState() => _VoiceListeningScreenState();
}

class _VoiceListeningScreenState extends State<VoiceListeningScreen> {
  final List<String> _revealedLines = [];
  final math.Random _rng = math.Random();
  List<double> _barHeights = List.filled(5, 8);

  Timer? _transcriptTimer;
  Timer? _amplitudeTimer;
  int _lineIndex = 0;

  @override
  void initState() {
    super.initState();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);

    // Simulated mic amplitude stream — replace with `record` /
    // `speech_to_text` amplitude callback.
    _amplitudeTimer = Timer.periodic(const Duration(milliseconds: 120), (_) {
      setState(() {
        _barHeights = List.generate(5, (_) => 8 + _rng.nextDouble() * 40);
      });
    });

    if (widget.prefillTranscript != null) {
      _revealedLines.add(widget.prefillTranscript!);
    } else {
      // Simulated speech-to-text stream, revealing one line at a time.
      _transcriptTimer = Timer.periodic(const Duration(milliseconds: 1200), (
        timer,
      ) {
        if (_lineIndex >= _demoTranscriptLines.length) {
          timer.cancel();
          return;
        }
        setState(() {
          _revealedLines.add(_demoTranscriptLines[_lineIndex]);
          _lineIndex++;
        });
      });
    }
  }

  @override
  void dispose() {
    _transcriptTimer?.cancel();
    _amplitudeTimer?.cancel();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    super.dispose();
  }

  String get _languageCode {
    return widget.languageLabel.toLowerCase() == 'pidgin'
        ? 'pidgin'
        : widget.languageLabel.toLowerCase();
  }

  void _finish() {
    final transcript = widget.prefillTranscript ?? _revealedLines.join(' ');
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => AiProcessingScreen(
          transcript: transcript,
          language: _languageCode,
          patientName: 'Amina',
          gestationalWeek: 30,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.voiceModeDark,
      body: SafeArea(
        child: Column(
          children: [
            // Top bar: back arrow + language badge
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back, color: Colors.white),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 14,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: Colors.white54),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          widget.flagEmoji,
                          style: const TextStyle(fontSize: 12),
                        ),
                        const SizedBox(width: 6),
                        Text(
                          widget.languageLabel,
                          style: AppTextStyles.label.copyWith(
                            color: Colors.white,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),
            if (widget.promptMessage != null)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Follow-up question',
                        style: AppTextStyles.caption.copyWith(
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        widget.promptMessage!,
                        style: AppTextStyles.bodyLarge.copyWith(
                          color: Colors.white,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 24),
            const BreathingOrb(state: OrbState.listening),
            const SizedBox(height: 8),

            // Amplitude bars
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(5, (i) {
                return AnimatedContainer(
                  duration: const Duration(milliseconds: 100),
                  margin: const EdgeInsets.symmetric(horizontal: 6),
                  width: 6,
                  height: _barHeights[i],
                  decoration: BoxDecoration(
                    color: AppColors.primaryContainer.withOpacity(0.6),
                    borderRadius: BorderRadius.circular(3),
                  ),
                );
              }),
            ),

            const SizedBox(height: 20),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'LISTENING...',
                  style: AppTextStyles.caption.copyWith(
                    color: Colors.white54,
                    letterSpacing: 1.2,
                  ),
                ),
              ),
            ),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 24, vertical: 8),
              child: Divider(color: Colors.white24, height: 1),
            ),

            // Live transcript
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Align(
                  alignment: Alignment.topLeft,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      for (final line in _revealedLines)
                        Padding(
                          padding: const EdgeInsets.only(bottom: 4),
                          child: AnimatedOpacity(
                            opacity: 1.0,
                            duration: const Duration(milliseconds: 150),
                            child: Text(
                              line,
                              style: AppTextStyles.bodyLarge.copyWith(
                                color: Colors.white,
                              ),
                            ),
                          ),
                        ),
                      if (widget.prefillTranscript == null &&
                          _revealedLines.length == _demoTranscriptLines.length)
                        Padding(
                          padding: const EdgeInsets.only(top: 8),
                          child: Text(
                            _demoTranslation,
                            style: AppTextStyles.bodyMedium.copyWith(
                              color: Colors.white54,
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            ),

            // Finish button
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 16),
              child: FilledButton.tonal(
                style: FilledButton.styleFrom(
                  backgroundColor: Colors.white12,
                  foregroundColor: Colors.white,
                  minimumSize: const Size.fromHeight(56),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                onPressed: _finish,
                child: const Text('Ana shirye  (Done)'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
