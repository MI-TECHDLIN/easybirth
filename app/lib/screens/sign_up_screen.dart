// sign_up_screen.dart
// Sign Up — phone-only account creation (UI prototype, no backend wired)
// Drop into: lib/screens/sign_up_screen.dart

import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';
import '../theme.dart';
import '../models/pregnancy_profile.dart';
import '../models/vaccine_schedule.dart';
import '../services/storage_service.dart';
import 'otp_verification_screen.dart';

/// Minimal country-code list for the prototype. Swap for the
/// `country_code_picker` package if you need the full country list.
class _CountryCode {
  final String flag;
  final String dialCode;
  final String name;
  const _CountryCode(this.flag, this.dialCode, this.name);
}

const List<_CountryCode> _countryCodes = [
  _CountryCode('🇳🇬', '+234', 'Nigeria'),
  _CountryCode('🇬🇭', '+233', 'Ghana'),
  _CountryCode('🇰🇪', '+254', 'Kenya'),
  _CountryCode('🇬🇧', '+44', 'United Kingdom'),
  _CountryCode('🇺🇸', '+1', 'United States'),
];

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();

  _CountryCode _selectedCountry = _countryCodes.first;
  late DateTime _selectedLmp;
  bool _agreedToTerms = false;
  bool _submitting = false;

  @override
  void initState() {
    super.initState();
    _selectedLmp = DateTime.now().subtract(const Duration(days: 90));
  }

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    super.dispose();
  }

  void _pickCountryCode() {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.surface,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) {
        return SafeArea(
          child: ListView(
            shrinkWrap: true,
            children: [
              const SizedBox(height: 8),
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: AppColors.outline.withValues(alpha: 0.4),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              for (final country in _countryCodes)
                ListTile(
                  leading: Text(
                    country.flag,
                    style: const TextStyle(fontSize: 22),
                  ),
                  title: Text(country.name, style: AppTextStyles.bodyMedium),
                  trailing: Text(country.dialCode, style: AppTextStyles.label),
                  onTap: () {
                    setState(() => _selectedCountry = country);
                    Navigator.of(context).pop();
                  },
                ),
              const SizedBox(height: 8),
            ],
          ),
        );
      },
    );
  }

  void _pickLmpDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedLmp,
      firstDate: DateTime.now().subtract(const Duration(days: 280)),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() => _selectedLmp = picked);
    }
  }

  Future<void> _handleCreateAccount() async {
    if (!_formKey.currentState!.validate()) return;
    if (!_agreedToTerms) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Please agree to the Terms of Service and Privacy Policy',
          ),
        ),
      );
      return;
    }

    setState(() => _submitting = true);

    final profile = PregnancyProfile(
      patientId: const Uuid().v4(),
      patientName: _nameController.text.trim(),
      phoneNumber:
          '${_selectedCountry.dialCode} ${_phoneController.text.trim()}',
      lastMenstrualPeriod: _selectedLmp,
    );

    await StorageService.saveProfile(profile);
    await StorageService.saveScheduleEntries(defaultSchedule);

    // Simulated network delay before "sending" the OTP.
    // Replace with a real phone-auth call when a backend is wired up.
    await Future.delayed(const Duration(milliseconds: 700));

    if (!mounted) return;
    setState(() => _submitting = false);

    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) =>
            OtpVerificationScreen(fullPhoneNumber: profile.phoneNumber),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    _RoundIconButton(
                      icon: Icons.arrow_back,
                      // SignUpScreen is shown as the app's root screen right
                      // after onboarding (see main.dart), so there may be
                      // nothing to pop back to. maybePop() is a safe no-op
                      // in that case instead of throwing/asserting.
                      onTap: () => Navigator.of(context).maybePop(),
                    ),
                    Text('Create Account', style: AppTextStyles.title),
                    Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        color: AppColors.primary,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.eco,
                        color: Colors.white,
                        size: 20,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                Text.rich(
                  TextSpan(
                    style: AppTextStyles.bodyMedium.copyWith(
                      color: AppColors.textSecondary,
                    ),
                    children: [
                      const TextSpan(text: 'Join thousands of mothers on '),
                      TextSpan(
                        text: 'easybirth',
                        style: AppTextStyles.bodyMedium.copyWith(
                          color: AppColors.primary,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                const _StepIndicator(step: 1, totalSteps: 2),
                const SizedBox(height: 28),

                _FieldLabel('Full Name'),
                const SizedBox(height: 8),
                TextFormField(
                  controller: _nameController,
                  style: AppTextStyles.bodyMedium,
                  decoration: _inputDecoration(
                    hint: 'e.g. Amina Yusuf',
                    icon: Icons.person_outline,
                  ),
                  validator: (value) => (value == null || value.trim().isEmpty)
                      ? 'Enter your full name'
                      : null,
                ),
                const SizedBox(height: 20),

                _FieldLabel('Phone Number'),
                const SizedBox(height: 8),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    InkWell(
                      onTap: _pickCountryCode,
                      borderRadius: BorderRadius.circular(16),
                      child: Container(
                        height: 56,
                        padding: const EdgeInsets.symmetric(horizontal: 12),
                        decoration: BoxDecoration(
                          color: AppColors.surfaceVariant,
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              _selectedCountry.flag,
                              style: const TextStyle(fontSize: 18),
                            ),
                            const SizedBox(width: 6),
                            Text(
                              _selectedCountry.dialCode,
                              style: AppTextStyles.label,
                            ),
                            const SizedBox(width: 4),
                            const Icon(
                              Icons.keyboard_arrow_down,
                              size: 18,
                              color: AppColors.outline,
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: TextFormField(
                        controller: _phoneController,
                        keyboardType: TextInputType.phone,
                        style: AppTextStyles.bodyMedium,
                        decoration: _inputDecoration(
                          hint: 'e.g. 801 234 5678',
                          icon: Icons.phone_outlined,
                        ),
                        validator: (value) =>
                            (value == null || value.trim().length < 7)
                            ? 'Enter a valid phone number'
                            : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                _FieldLabel('Last menstrual period'),
                const SizedBox(height: 8),
                GestureDetector(
                  onTap: _pickLmpDate,
                  child: Container(
                    height: 56,
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceVariant,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '${_selectedLmp.day.toString().padLeft(2, '0')}/${_selectedLmp.month.toString().padLeft(2, '0')}/${_selectedLmp.year}',
                          style: AppTextStyles.bodyMedium,
                        ),
                        const Icon(
                          Icons.calendar_month,
                          color: AppColors.outline,
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Checkbox(
                      value: _agreedToTerms,
                      activeColor: AppColors.primary,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(4),
                      ),
                      onChanged: (value) =>
                          setState(() => _agreedToTerms = value ?? false),
                    ),
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.only(top: 14),
                        child: Text.rich(
                          TextSpan(
                            style: AppTextStyles.bodyMedium.copyWith(
                              color: AppColors.textSecondary,
                              fontSize: 13,
                            ),
                            children: [
                              const TextSpan(text: "I agree to easybirth's "),
                              TextSpan(
                                text: 'Terms of Service',
                                style: TextStyle(
                                  color: AppColors.primary,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              const TextSpan(text: ' and '),
                              TextSpan(
                                text: 'Privacy Policy',
                                style: TextStyle(
                                  color: AppColors.primary,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),

                FilledButton(
                  onPressed: _submitting ? null : _handleCreateAccount,
                  child: _submitting
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Text('Create Account  →'),
                ),
                const SizedBox(height: 16),
                Center(
                  child: Text.rich(
                    TextSpan(
                      style: AppTextStyles.bodyMedium.copyWith(
                        color: AppColors.textSecondary,
                      ),
                      children: [
                        const TextSpan(text: 'Already have an account?  '),
                        TextSpan(
                          text: 'Sign In',
                          style: TextStyle(
                            color: AppColors.primary,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 12),
              ],
            ),
          ),
        ),
      ),
    );
  }

  InputDecoration _inputDecoration({
    required String hint,
    required IconData icon,
  }) {
    return InputDecoration(
      hintText: hint,
      hintStyle: AppTextStyles.bodyMedium.copyWith(color: AppColors.outline),
      filled: true,
      fillColor: AppColors.surfaceVariant,
      prefixIcon: Container(
        margin: const EdgeInsets.all(12),
        width: 24,
        height: 24,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: AppColors.primaryContainer,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Icon(icon, size: 14, color: AppColors.primary),
      ),
      prefixIconConstraints: const BoxConstraints(minWidth: 0, minHeight: 0),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(16),
        borderSide: BorderSide.none,
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(16),
        borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(16),
        borderSide: const BorderSide(color: AppColors.highRisk, width: 1.5),
      ),
      contentPadding: const EdgeInsets.symmetric(vertical: 16),
    );
  }
}

class _FieldLabel extends StatelessWidget {
  final String text;
  const _FieldLabel(this.text);

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: AppTextStyles.label.copyWith(color: AppColors.textSecondary),
    );
  }
}

class _RoundIconButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;
  const _RoundIconButton({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          color: AppColors.surfaceVariant,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Icon(icon, size: 18, color: AppColors.textPrimary),
      ),
    );
  }
}

class _StepIndicator extends StatelessWidget {
  final int step;
  final int totalSteps;
  const _StepIndicator({required this.step, required this.totalSteps});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        for (var i = 0; i < totalSteps; i++)
          Padding(
            padding: EdgeInsets.only(right: i == totalSteps - 1 ? 0 : 6),
            child: Container(
              width: 28,
              height: 6,
              decoration: BoxDecoration(
                color: i < step ? AppColors.primary : AppColors.surfaceVariant,
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
        const SizedBox(width: 10),
        Text(
          'STEP $step / $totalSteps',
          style: AppTextStyles.caption.copyWith(letterSpacing: 0.4),
        ),
      ],
    );
  }
}
