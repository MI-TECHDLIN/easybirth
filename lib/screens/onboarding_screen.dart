// ============================================================
// AmaraAI — Onboarding Screen
// ============================================================
// ASSET SETUP: Add these to your pubspec.yaml under flutter:
//   assets:
//     - assets/images/onboarding_slide_1.png
//     - assets/images/onboarding_slide_2.png
//     - assets/images/onboarding_slide_3.png
//
// FONTS: Add to pubspec.yaml under flutter > fonts:
//   PlusJakartaSans (Bold, SemiBold) and Nunito (Regular, SemiBold, Bold)
//   OR use google_fonts package: google_fonts: ^6.1.0
//
// PACKAGES NEEDED:
//   google_fonts: ^6.1.0
// ============================================================

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// ── Change these paths to match your actual asset filenames ──
const _kSlide1Asset = 'assets/design1.png';
const _kSlide2Asset = 'assets/design2.png';
const _kSlide3Asset = 'assets/design3.png';

// ── Design tokens ─────────────────────────────────────────────
const _kPrimary = Color(0xFF1B6B4A);
const _kTextPrimary = Color(0xFF1A1A1A);
const _kTextSub = Color(0xFF5C5C5C);
const _kIndicatorInactive = Color(0xFFCCC6BF);

// Per-slide background colors — matched to illustration palette
const _kBgColors = [
  Color(0xFFE8F5EE), // Slide 1: mint green tint
  Color(0xFFF0EDE6), // Slide 2: warm cream
  Color(0xFFF5EDE0), // Slide 3: peach cream
];

// ── Slide data ────────────────────────────────────────────────
class _SlideData {
  final String asset;
  final String title;
  final String body;
  const _SlideData({
    required this.asset,
    required this.title,
    required this.body,
  });
}

const _kSlides = [
  _SlideData(
    asset: _kSlide1Asset,
    title: 'Speak in your language',
    body:
        'Ask about your pregnancy in Hausa, Yoruba, Igbo, or Pidgin. The AI understands you.',
  ),
  _SlideData(
    asset: _kSlide2Asset,
    title: 'Works without internet',
    body:
        'All AI runs on your phone. Your voice never leaves your device. No data plan needed.',
  ),
  _SlideData(
    asset: _kSlide3Asset,
    title: 'Know when to act',
    body:
        'Get clear advice — safe to wait, or go to the health centre now. No guessing.',
  ),
];

// ============================================================
// MAIN SCREEN
// ============================================================
class OnboardingScreen extends StatefulWidget {
  /// Called when the user taps "Get Started" on the last slide.
  final VoidCallback? onComplete;

  /// Called when the user taps "Skip".
  final VoidCallback? onSkip;

  const OnboardingScreen({super.key, this.onComplete, this.onSkip});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen>
    with TickerProviderStateMixin {
  final PageController _pageController = PageController();
  int _currentPage = 0;
  bool _isAnimating = false;

  // ── Animation controllers ──────────────────────────────────

  // Illustration: scale + fade on each new page
  late final AnimationController _illustrationCtrl = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 550),
  );

  // Text block: slide-up + staggered fade
  late final AnimationController _textCtrl = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 500),
  );

  // Button: subtle scale press feedback
  late final AnimationController _buttonCtrl = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 120),
    lowerBound: 0.96,
    upperBound: 1.0,
  )..value = 1.0;

  // ── Derived animations ─────────────────────────────────────

  late final Animation<double> _illustrationScale =
      Tween<double>(begin: 0.88, end: 1.0).animate(
        CurvedAnimation(parent: _illustrationCtrl, curve: Curves.easeOutCubic),
      );

  late final Animation<double> _illustrationFade = Tween<double>(
    begin: 0.0,
    end: 1.0,
  ).animate(CurvedAnimation(parent: _illustrationCtrl, curve: Curves.easeIn));

  late final Animation<Offset> _textSlide = Tween<Offset>(
    begin: const Offset(0, 0.25),
    end: Offset.zero,
  ).animate(CurvedAnimation(parent: _textCtrl, curve: Curves.easeOutCubic));

  late final Animation<double> _headlineFade =
      Tween<double>(begin: 0.0, end: 1.0).animate(
        CurvedAnimation(
          parent: _textCtrl,
          curve: const Interval(0.0, 0.65, curve: Curves.easeIn),
        ),
      );

  late final Animation<double> _bodyFade = Tween<double>(begin: 0.0, end: 1.0)
      .animate(
        CurvedAnimation(
          parent: _textCtrl,
          curve: const Interval(0.25, 1.0, curve: Curves.easeIn),
        ),
      );

  // ── Lifecycle ──────────────────────────────────────────────

  @override
  void initState() {
    super.initState();
    _playEnterAnimations();
  }

  @override
  void dispose() {
    _pageController.dispose();
    _illustrationCtrl.dispose();
    _textCtrl.dispose();
    _buttonCtrl.dispose();
    super.dispose();
  }

  // ── Animation helpers ──────────────────────────────────────

  Future<void> _playEnterAnimations({
    Duration textDelay = Duration.zero,
  }) async {
    _illustrationCtrl.reset();
    _textCtrl.reset();
    _illustrationCtrl.forward();
    await Future.delayed(const Duration(milliseconds: 80) + textDelay);
    if (mounted) _textCtrl.forward();
  }

  void _onPageChanged(int index) {
    setState(() => _currentPage = index);
    HapticFeedback.selectionClick();
    _playEnterAnimations();
  }

  Future<void> _handleNext() async {
    if (_isAnimating) return;
    _isAnimating = true;

    // Button press animation
    await _buttonCtrl.reverse();
    await _buttonCtrl.forward();

    if (_currentPage < _kSlides.length - 1) {
      await _pageController.nextPage(
        duration: const Duration(milliseconds: 480),
        curve: Curves.easeInOutCubic,
      );
    } else {
      widget.onComplete?.call();
    }

    _isAnimating = false;
  }

  void _handleSkip() {
    widget.onSkip?.call();
  }

  // ── Build ──────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    return AnnotatedRegion<SystemUiOverlayStyle>(
      value: const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarIconBrightness: Brightness.dark,
      ),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 380),
        curve: Curves.easeInOut,
        color: _kBgColors[_currentPage],
        child: Scaffold(
          backgroundColor: Colors.transparent,
          body: SafeArea(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                _buildSkipButton(),
                _buildIllustrationPageView(),
                const SizedBox(height: 20),
                _buildPageIndicator(),
                const SizedBox(height: 28),
                _buildTextBlock(),
                const SizedBox(height: 32),
                _buildCTAButton(),
                const SizedBox(height: 28),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // ── Skip button ────────────────────────────────────────────

  Widget _buildSkipButton() {
    return SizedBox(
      height: 44,
      child: Align(
        alignment: Alignment.centerRight,
        child: AnimatedOpacity(
          opacity: _currentPage < _kSlides.length - 1 ? 1.0 : 0.0,
          duration: const Duration(milliseconds: 200),
          child: Padding(
            padding: const EdgeInsets.only(right: 8),
            child: TextButton(
              onPressed: _currentPage < _kSlides.length - 1
                  ? _handleSkip
                  : null,
              style: TextButton.styleFrom(
                foregroundColor: _kTextSub,
                textStyle: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),
              child: const Text('Skip'),
            ),
          ),
        ),
      ),
    );
  }

  // ── Illustration PageView ──────────────────────────────────

  Widget _buildIllustrationPageView() {
    return Expanded(
      child: PageView.builder(
        controller: _pageController,
        onPageChanged: _onPageChanged,
        itemCount: _kSlides.length,
        physics: const BouncingScrollPhysics(),
        itemBuilder: (context, index) {
          return _buildSlidePage(index);
        },
      ),
    );
  }

  Widget _buildSlidePage(int index) {
    final isActive = index == _currentPage;

    final child = _buildSlideImage(context, index);
    if (!isActive) {
      return child;
    }

    // Active slide: scale + fade entrance
    return AnimatedBuilder(
      animation: _illustrationCtrl,
      builder: (context, child) => Transform.scale(
        scale: _illustrationScale.value,
        child: Opacity(opacity: _illustrationFade.value, child: child),
      ),
      child: child,
    );
  }

  Widget _buildSlideImage(BuildContext context, int index) {
    final screenWidth = MediaQuery.of(context).size.width;
    return Center(
      child: SizedBox(
        width: screenWidth,
        child: Image.asset(
          _kSlides[index].asset,
          fit: BoxFit.fitWidth,
          alignment: Alignment.topCenter,
          errorBuilder: (_, __, ___) => _illustrationPlaceholder(index),
        ),
      ),
    );
  }

  // Fallback if asset not found during development
  Widget _illustrationPlaceholder(int index) {
    const icons = [
      Icons.record_voice_over_rounded,
      Icons.wifi_off_rounded,
      Icons.health_and_safety_rounded,
    ];
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icons[index], size: 80, color: _kPrimary.withOpacity(0.4)),
          const SizedBox(height: 12),
          Text(
            'Add your illustration\nto ${_kSlides[index].asset}',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 13, color: _kTextSub.withOpacity(0.6)),
          ),
        ],
      ),
    );
  }

  // ── Page indicator ─────────────────────────────────────────

  Widget _buildPageIndicator() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(_kSlides.length, (index) {
        final isActive = index == _currentPage;
        return AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeInOut,
          margin: const EdgeInsets.symmetric(horizontal: 4),
          width: isActive ? 28 : 8,
          height: 8,
          decoration: BoxDecoration(
            color: isActive ? _kPrimary : _kIndicatorInactive,
            borderRadius: BorderRadius.circular(4),
          ),
        );
      }),
    );
  }

  // ── Text block ─────────────────────────────────────────────

  Widget _buildTextBlock() {
    return AnimatedBuilder(
      animation: _textCtrl,
      builder: (context, _) {
        return SlideTransition(
          position: _textSlide,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 32),
            child: Column(
              children: [
                // Headline — fades in first
                Opacity(
                  opacity: _headlineFade.value,
                  child: AnimatedSwitcher(
                    duration: const Duration(milliseconds: 200),
                    child: Text(
                      _kSlides[_currentPage].title,
                      key: ValueKey('title_$_currentPage'),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontFamily:
                            'PlusJakartaSans', // swap for GoogleFonts.plusJakartaSans()
                        fontSize: 26,
                        fontWeight: FontWeight.w800,
                        color: _kTextPrimary,
                        height: 1.25,
                        letterSpacing: -0.3,
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 14),

                // Body — fades in slightly after headline
                Opacity(
                  opacity: _bodyFade.value,
                  child: AnimatedSwitcher(
                    duration: const Duration(milliseconds: 200),
                    child: Text(
                      _kSlides[_currentPage].body,
                      key: ValueKey('body_$_currentPage'),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontFamily: 'Nunito',
                        fontSize: 15,
                        fontWeight: FontWeight.w400,
                        color: _kTextSub,
                        height: 1.65,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  // ── CTA button ─────────────────────────────────────────────

  Widget _buildCTAButton() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: AnimatedBuilder(
        animation: _buttonCtrl,
        builder: (context, child) =>
            Transform.scale(scale: _buttonCtrl.value, child: child),
        child: SizedBox(
          width: double.infinity,
          height: 56,
          child: ElevatedButton(
            onPressed: _handleNext,
            style: ElevatedButton.styleFrom(
              backgroundColor: _kPrimary,
              foregroundColor: Colors.white,
              elevation: 0,
              shadowColor: Colors.transparent,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
            ),
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 240),
              transitionBuilder: (child, animation) {
                // Slide in from right, slide out to left
                return FadeTransition(
                  opacity: animation,
                  child: SlideTransition(
                    position:
                        Tween<Offset>(
                          begin: const Offset(0.25, 0),
                          end: Offset.zero,
                        ).animate(
                          CurvedAnimation(
                            parent: animation,
                            curve: Curves.easeOutCubic,
                          ),
                        ),
                    child: child,
                  ),
                );
              },
              child: Text(
                _currentPage == _kSlides.length - 1
                    ? 'Get Started →'
                    : 'Next →',
                key: ValueKey(_currentPage == _kSlides.length - 1),
                style: const TextStyle(
                  fontFamily: 'Nunito',
                  fontSize: 16,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 0.2,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
