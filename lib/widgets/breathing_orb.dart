// breathing_orb.dart
// AmaraAI ("easybirth") — "The Orb" shared signature element.
// Drop into: lib/widgets/breathing_orb.dart
//
// The Orb replaces a standard mic button. It is a living UI presence with
// four states (idle, listening, processing, result) and is connected across
// routes via Hero(tag: 'orb'). See DESIGN SYSTEM notes for full spec.

import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../theme.dart';

enum OrbState { idle, listening, processing, result }

class BreathingOrb extends StatefulWidget {
  final OrbState state;

  /// Required when [state] is [OrbState.result].
  final RiskLevel? riskLevel;

  /// Called on tap. Only wired up when [state] is [OrbState.idle].
  final VoidCallback? onTap;

  const BreathingOrb({
    super.key,
    required this.state,
    this.riskLevel,
    this.onTap,
  }) : assert(
          state != OrbState.result || riskLevel != null,
          'riskLevel is required when state is OrbState.result',
        );

  @override
  State<BreathingOrb> createState() => _BreathingOrbState();
}

class _BreathingOrbState extends State<BreathingOrb>
    with TickerProviderStateMixin {
  // Idle pulse
  AnimationController? _idleController;

  // Listening rings (3 staggered controllers)
  final List<AnimationController> _ringControllers = [];

  // Processing rotation + color morph
  AnimationController? _rotationController;

  // Result entrance pulse
  AnimationController? _resultController;

  // Tap burst (idle only)
  AnimationController? _tapController;

  @override
  void initState() {
    super.initState();

    switch (widget.state) {
      case OrbState.idle:
        _idleController = AnimationController(
          vsync: this,
          duration: const Duration(seconds: 2),
        )..repeat(reverse: true);
        _tapController = AnimationController(
          vsync: this,
          duration: const Duration(milliseconds: 150),
          lowerBound: 1.0,
          upperBound: 1.15,
        )..value = 1.0;
        break;

      case OrbState.listening:
        const durations = [800, 1100, 1400];
        const offsets = [0, 200, 400];
        for (var i = 0; i < 3; i++) {
          final controller = AnimationController(
            vsync: this,
            duration: Duration(milliseconds: durations[i]),
          );
          _ringControllers.add(controller);
          Future.delayed(Duration(milliseconds: offsets[i]), () {
            if (mounted) controller.repeat();
          });
        }
        break;

      case OrbState.processing:
        _rotationController = AnimationController(
          vsync: this,
          duration: const Duration(milliseconds: 1200),
        )..repeat();
        break;

      case OrbState.result:
        _resultController = AnimationController(
          vsync: this,
          duration: const Duration(milliseconds: 600),
        )..forward();
        break;
    }
  }

  @override
  void dispose() {
    _idleController?.dispose();
    _tapController?.dispose();
    for (final c in _ringControllers) {
      c.dispose();
    }
    _rotationController?.dispose();
    _resultController?.dispose();
    super.dispose();
  }

  void _handleTap() async {
    if (widget.onTap == null) return;
    await _tapController?.forward();
    await _tapController?.reverse();
    widget.onTap!();
  }

  @override
  Widget build(BuildContext context) {
    Widget orb;
    switch (widget.state) {
      case OrbState.idle:
        orb = _buildIdle();
        break;
      case OrbState.listening:
        orb = _buildListening();
        break;
      case OrbState.processing:
        orb = _buildProcessing();
        break;
      case OrbState.result:
        orb = _buildResult();
        break;
    }

    return Hero(
      tag: 'orb',
      child: Material(
        type: MaterialType.transparency,
        child: orb,
      ),
    );
  }

  // ---- Idle: 180dp, primary color, radial glow, breathing scale/opacity ----
  Widget _buildIdle() {
    return GestureDetector(
      onTap: _handleTap,
      child: AnimatedBuilder(
        animation: Listenable.merge([_idleController!, _tapController!]),
        builder: (context, child) {
          final breathe = 0.97 + (_idleController!.value * 0.06); // .97-1.03
          final opacity = 0.85 + (_idleController!.value * 0.15); // .85-1.0
          final tapScale = _tapController?.value ?? 1.0;
          return Transform.scale(
            scale: breathe * tapScale,
            child: Opacity(
              opacity: opacity,
              child: child,
            ),
          );
        },
        child: Container(
          width: 180,
          height: 180,
          decoration: const BoxDecoration(
            shape: BoxShape.circle,
            color: AppColors.primary,
            boxShadow: [
              BoxShadow(
                color: AppColors.primaryContainer,
                blurRadius: 80,
                spreadRadius: 20,
              ),
            ],
          ),
          child: const Icon(Icons.mic, color: Colors.white, size: 56),
        ),
      ),
    );
  }

  // ---- Listening: 240dp white orb + 3 staggered expanding rings ----
  Widget _buildListening() {
    return SizedBox(
      width: 360,
      height: 360,
      child: Stack(
        alignment: Alignment.center,
        children: [
          for (final controller in _ringControllers)
            AnimatedBuilder(
              animation: controller,
              builder: (context, child) {
                final scale = 1.0 + controller.value * 0.5;
                final opacity = (1.0 - controller.value).clamp(0.0, 1.0);
                return Opacity(
                  opacity: opacity * 0.5,
                  child: Transform.scale(
                    scale: scale,
                    child: Container(
                      width: 240,
                      height: 240,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(
                          color: AppColors.primaryContainer,
                          width: 2,
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          Container(
            width: 240,
            height: 240,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: Colors.white.withOpacity(0.9),
              boxShadow: [
                BoxShadow(
                  color: AppColors.primaryContainer.withOpacity(0.6),
                  blurRadius: 60,
                  spreadRadius: 10,
                ),
              ],
            ),
            child: Icon(Icons.mic, color: AppColors.primary, size: 64),
          ),
        ],
      ),
    );
  }

  // ---- Processing: 200dp gradient morph + rotating conic ring ----
  Widget _buildProcessing() {
    return SizedBox(
      width: 260,
      height: 260,
      child: Stack(
        alignment: Alignment.center,
        children: [
          AnimatedBuilder(
            animation: _rotationController!,
            builder: (context, child) {
              return Transform.rotate(
                angle: _rotationController!.value * 2 * math.pi,
                child: Container(
                  width: 260,
                  height: 260,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: SweepGradient(
                      colors: const [
                        AppColors.primary,
                        AppColors.secondary,
                        AppColors.primary,
                      ],
                      stops: const [0.0, 0.5, 1.0],
                      startAngle: 0,
                      endAngle: 2 * math.pi,
                    ),
                  ),
                ),
              );
            },
          ),
          TweenAnimationBuilder<Color?>(
            tween: ColorTween(
              begin: AppColors.primary,
              end: AppColors.secondary,
            ),
            duration: const Duration(milliseconds: 400),
            builder: (context, color, child) {
              return Container(
                width: 200,
                height: 200,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(
                    colors: [
                      color ?? AppColors.primary,
                      AppColors.secondary,
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  // ---- Result: 180dp, snaps to semantic risk color, elastic pulse ----
  Widget _buildResult() {
    final color = widget.riskLevel!.color;
    return AnimatedBuilder(
      animation: _resultController!,
      builder: (context, child) {
        final scale = Curves.elasticOut.transform(_resultController!.value);
        return Transform.scale(scale: scale, child: child);
      },
      child: Container(
        width: 180,
        height: 180,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: color,
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.35),
              blurRadius: 40,
              spreadRadius: 8,
            ),
          ],
        ),
        child: Center(
          child: Text(
            widget.riskLevel!.icon,
            style: const TextStyle(fontSize: 56),
          ),
        ),
      ),
    );
  }
}