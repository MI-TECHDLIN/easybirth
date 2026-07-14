"""Unit tests for feature_engineering.calculators module."""

import pytest
from ..calculators import (
    calculate_bmi,
    calculate_map,
    calculate_pulse_pressure,
    calculate_gestational_trimester,
    count_symptoms,
    compute_age_group,
    compute_bmi_category,
    compute_bp_category,
    is_high_risk_age,
    compute_hypertension_risk,
    compute_diabetes_risk,
    compute_accessibility_index,
    compute_symptom_severity_score,
    has_emergency_flag,
)


class TestBMICalculation:
    """Test BMI calculation."""

    def test_bmi_normal_case(self):
        """Test BMI calculation with typical values."""
        # 70 kg, 170 cm → BMI ≈ 24.22
        assert calculate_bmi(70, 170) == 24.22

    def test_bmi_obese(self):
        """Test BMI for obese individual."""
        # 100 kg, 160 cm → BMI ≈ 39.06
        assert calculate_bmi(100, 160) == 39.06

    def test_bmi_underweight(self):
        """Test BMI for underweight individual."""
        # 50 kg, 170 cm → BMI ≈ 17.24
        assert calculate_bmi(50, 170) == 17.24

    def test_bmi_invalid_weight(self):
        """Test BMI rejects invalid weight."""
        with pytest.raises(ValueError, match="Weight must be positive"):
            calculate_bmi(-10, 170)
        with pytest.raises(ValueError, match="Weight must be positive"):
            calculate_bmi(0, 170)

    def test_bmi_invalid_height(self):
        """Test BMI rejects invalid height."""
        with pytest.raises(ValueError, match="Height must be positive"):
            calculate_bmi(70, -170)
        with pytest.raises(ValueError, match="Height must be positive"):
            calculate_bmi(70, 0)


class TestMAPCalculation:
    """Test Mean Arterial Pressure calculation."""

    def test_map_normal_case(self):
        """Test MAP with typical values."""
        # 120/80 → (120 + 2*80)/3 = 93.33
        assert calculate_map(120, 80) == 93.33

    def test_map_elevated(self):
        """Test MAP with elevated BP."""
        # 160/100 → (160 + 2*100)/3 = 120
        assert calculate_map(160, 100) == 120.0

    def test_map_low(self):
        """Test MAP with low BP."""
        # 90/60 → (90 + 2*60)/3 = 70
        assert calculate_map(90, 60) == 70.0

    def test_map_invalid_systolic(self):
        """Test MAP rejects invalid systolic BP."""
        with pytest.raises(ValueError, match="Systolic BP must be positive"):
            calculate_map(-10, 80)

    def test_map_invalid_diastolic(self):
        """Test MAP rejects invalid diastolic BP."""
        with pytest.raises(ValueError, match="Diastolic BP must be positive"):
            calculate_map(120, -10)


class TestPulsePressureCalculation:
    """Test Pulse Pressure calculation."""

    def test_pulse_pressure_normal(self):
        """Test pulse pressure with normal BP."""
        # 120/80 → 120 - 80 = 40
        assert calculate_pulse_pressure(120, 80) == 40

    def test_pulse_pressure_elevated(self):
        """Test pulse pressure with elevated BP."""
        # 160/90 → 160 - 90 = 70
        assert calculate_pulse_pressure(160, 90) == 70

    def test_pulse_pressure_low(self):
        """Test pulse pressure with low BP."""
        # 100/70 → 100 - 70 = 30
        assert calculate_pulse_pressure(100, 70) == 30

    def test_pulse_pressure_invalid_order(self):
        """Test pulse pressure rejects systolic <= diastolic."""
        with pytest.raises(ValueError, match="Systolic.*must be > Diastolic"):
            calculate_pulse_pressure(80, 120)
        with pytest.raises(ValueError, match="Systolic.*must be > Diastolic"):
            calculate_pulse_pressure(80, 80)


class TestTrimesteCalculation:
    """Test gestational trimester calculation."""

    def test_first_trimester(self):
        """Test weeks 1-13 → First trimester."""
        assert calculate_gestational_trimester(1) == 0
        assert calculate_gestational_trimester(7) == 0
        assert calculate_gestational_trimester(13) == 0

    def test_second_trimester(self):
        """Test weeks 14-26 → Second trimester."""
        assert calculate_gestational_trimester(14) == 1
        assert calculate_gestational_trimester(20) == 1
        assert calculate_gestational_trimester(26) == 1

    def test_third_trimester(self):
        """Test weeks 27-42 → Third trimester."""
        assert calculate_gestational_trimester(27) == 2
        assert calculate_gestational_trimester(35) == 2
        assert calculate_gestational_trimester(42) == 2

    def test_invalid_weeks(self):
        """Test invalid pregnancy weeks."""
        with pytest.raises(ValueError, match="1-42"):
            calculate_gestational_trimester(0)
        with pytest.raises(ValueError, match="1-42"):
            calculate_gestational_trimester(43)

    def test_non_integer_weeks(self):
        """Test non-integer weeks."""
        with pytest.raises(ValueError, match="must be integer"):
            calculate_gestational_trimester(20.5)


class TestSymptomCounting:
    """Test symptom counting."""

    def test_no_symptoms(self):
        """Test with no symptoms."""
        assert count_symptoms() == 0
        assert count_symptoms(
            headache=0,
            blurred_vision=0,
            swollen_feet=0,
            bleeding=0,
            abdominal_pain=0,
            fever=0,
            reduced_fetal_movement=0,
            severe_vomiting=0,
            difficulty_breathing=0,
        ) == 0

    def test_single_symptom(self):
        """Test with single symptom."""
        assert count_symptoms(headache=1) == 1
        assert count_symptoms(bleeding=1) == 1

    def test_multiple_symptoms(self):
        """Test with multiple symptoms."""
        assert count_symptoms(headache=1, fever=1, bleeding=1) == 3
        assert count_symptoms(
            headache=1,
            blurred_vision=1,
            swollen_feet=1,
            bleeding=1,
            abdominal_pain=1,
        ) == 5

    def test_all_symptoms(self):
        """Test with all symptoms present."""
        assert count_symptoms(
            headache=1,
            blurred_vision=1,
            swollen_feet=1,
            bleeding=1,
            abdominal_pain=1,
            fever=1,
            reduced_fetal_movement=1,
            severe_vomiting=1,
            difficulty_breathing=1,
        ) == 9

    def test_invalid_symptom_value(self):
        """Test invalid symptom value."""
        with pytest.raises(ValueError, match="must be 0 or 1"):
            count_symptoms(headache=2)


class TestAgeGroupComputation:
    """Test age group computation."""

    def test_teen_pregnancy(self):
        """Test age < 18 → teen pregnancy."""
        assert compute_age_group(15) == 0
        assert compute_age_group(17) == 0

    def test_optimal_age(self):
        """Test age 18-34 → optimal."""
        assert compute_age_group(18) == 1
        assert compute_age_group(25) == 1
        assert compute_age_group(34) == 1

    def test_advanced_maternal_age(self):
        """Test age 35-39 → advanced maternal age."""
        assert compute_age_group(35) == 2
        assert compute_age_group(37) == 2
        assert compute_age_group(39) == 2

    def test_high_risk_advanced_age(self):
        """Test age 40+ → high-risk advanced age."""
        assert compute_age_group(40) == 3
        assert compute_age_group(45) == 3
        assert compute_age_group(49) == 3

    def test_invalid_age(self):
        """Test invalid ages."""
        with pytest.raises(ValueError, match="15-49"):
            compute_age_group(14)
        with pytest.raises(ValueError, match="15-49"):
            compute_age_group(50)


class TestBMICategoryComputation:
    """Test BMI category computation."""

    def test_underweight(self):
        """Test BMI < 18.5 → Underweight."""
        assert compute_bmi_category(18.4) == 0

    def test_normal_weight(self):
        """Test BMI 18.5-24.9 → Normal."""
        assert compute_bmi_category(18.5) == 1
        assert compute_bmi_category(24.9) == 1

    def test_overweight(self):
        """Test BMI 25.0-29.9 → Overweight."""
        assert compute_bmi_category(25.0) == 2
        assert compute_bmi_category(29.9) == 2

    def test_obese(self):
        """Test BMI >= 30.0 → Obese."""
        assert compute_bmi_category(30.0) == 3
        assert compute_bmi_category(40.0) == 3

    def test_invalid_bmi(self):
        """Test invalid BMI values."""
        with pytest.raises(ValueError, match="10-60"):
            compute_bmi_category(9)
        with pytest.raises(ValueError, match="10-60"):
            compute_bmi_category(61)


class TestBPCategoryComputation:
    """Test blood pressure category computation."""

    def test_normal_bp(self):
        """Test SBP < 120 AND DBP < 80 → Normal."""
        assert compute_bp_category(119, 79) == 0
        assert compute_bp_category(110, 70) == 0

    def test_elevated_bp(self):
        """Test SBP 120-129 AND DBP < 80 → Elevated."""
        assert compute_bp_category(120, 79) == 1
        assert compute_bp_category(129, 79) == 1

    def test_stage_1_hypertension(self):
        """Test SBP 130-139 OR DBP 80-89 → Stage 1."""
        assert compute_bp_category(130, 79) == 2
        assert compute_bp_category(139, 89) == 2

    def test_stage_2_hypertension(self):
        """Test SBP >= 140 OR DBP >= 90 → Stage 2."""
        assert compute_bp_category(140, 89) == 3
        assert compute_bp_category(160, 100) == 3

    def test_invalid_bp(self):
        """Test invalid BP values."""
        with pytest.raises(ValueError, match="Systolic BP must be 60-220"):
            compute_bp_category(50, 80)
        with pytest.raises(ValueError, match="Diastolic BP must be 40-140"):
            compute_bp_category(120, 150)


class TestHighRiskAge:
    """Test high-risk age detection."""

    def test_high_risk_teen(self):
        """Test age < 18 → high risk."""
        assert is_high_risk_age(15) == 1
        assert is_high_risk_age(17) == 1

    def test_high_risk_advanced(self):
        """Test age > 35 → high risk."""
        assert is_high_risk_age(36) == 1
        assert is_high_risk_age(40) == 1
        assert is_high_risk_age(49) == 1

    def test_low_risk_optimal(self):
        """Test optimal age 18-35 → low risk."""
        assert is_high_risk_age(18) == 0
        assert is_high_risk_age(25) == 0
        assert is_high_risk_age(35) == 0


class TestHypertensionRisk:
    """Test hypertension risk computation."""

    def test_no_history_normal_bp(self):
        """Test no history and normal BP → no risk."""
        assert compute_hypertension_risk(0, 120, 80) == 0

    def test_history_no_stage2_bp(self):
        """Test history but not Stage 2 BP → risk."""
        assert compute_hypertension_risk(1, 130, 85) == 1

    def test_no_history_stage2_bp(self):
        """Test no history but Stage 2 BP → risk."""
        assert compute_hypertension_risk(0, 145, 95) == 1

    def test_history_and_stage2_bp(self):
        """Test history AND Stage 2 BP → high risk."""
        assert compute_hypertension_risk(1, 160, 100) == 1


class TestDiabetesRisk:
    """Test diabetes risk computation."""

    def test_no_history_normal_glucose(self):
        """Test no history and normal glucose → no risk."""
        assert compute_diabetes_risk(0, 95) == 0

    def test_history_normal_glucose(self):
        """Test history but normal glucose → risk."""
        assert compute_diabetes_risk(1, 100) == 1

    def test_no_history_elevated_glucose(self):
        """Test no history but elevated glucose (>140) → risk."""
        assert compute_diabetes_risk(0, 150) == 1

    def test_borderline_glucose(self):
        """Test glucose at threshold."""
        assert compute_diabetes_risk(0, 140) == 1
        assert compute_diabetes_risk(0, 139.9) == 0


class TestAccessibilityIndex:
    """Test accessibility index computation."""

    def test_good_access(self):
        """Test < 10km and < 20min → good."""
        assert compute_accessibility_index(5, 15) == 0
        assert compute_accessibility_index(9, 19) == 0

    def test_moderate_access(self):
        """Test 10-50km and 20-60min → moderate."""
        assert compute_accessibility_index(25, 30) == 1
        assert compute_accessibility_index(50, 60) == 1

    def test_poor_access(self):
        """Test > 50km and > 60min → poor."""
        assert compute_accessibility_index(75, 90) == 2
        assert compute_accessibility_index(100, 120) == 2


class TestSymptomSeverityScore:
    """Test symptom severity score computation."""

    def test_no_symptoms(self):
        """Test 0 symptoms → severity 0."""
        assert compute_symptom_severity_score(0) == 0

    def test_mild_symptoms(self):
        """Test 1-2 symptoms → severity 1."""
        assert compute_symptom_severity_score(1) == 1
        assert compute_symptom_severity_score(2) == 1

    def test_moderate_symptoms(self):
        """Test 3-5 symptoms → severity 2."""
        assert compute_symptom_severity_score(3) == 2
        assert compute_symptom_severity_score(5) == 2

    def test_severe_symptoms(self):
        """Test 6+ symptoms → severity 3."""
        assert compute_symptom_severity_score(6) == 3
        assert compute_symptom_severity_score(9) == 3


class TestEmergencyFlag:
    """Test emergency flag detection."""

    def test_no_emergency(self):
        """Test no emergency symptoms → flag 0."""
        assert has_emergency_flag(0, 0, 0, 0) == 0

    def test_bleeding_emergency(self):
        """Test bleeding alone → emergency."""
        assert has_emergency_flag(bleeding=1) == 1

    def test_breathing_emergency(self):
        """Test difficulty breathing alone → emergency."""
        assert has_emergency_flag(difficulty_breathing=1) == 1

    def test_vomiting_not_emergency(self):
        """Test vomiting alone → NOT emergency."""
        assert has_emergency_flag(severe_vomiting=1) == 0

    def test_reduced_fetal_movement_not_emergency(self):
        """Test reduced fetal movement alone → NOT emergency."""
        assert has_emergency_flag(reduced_fetal_movement=1) == 0
