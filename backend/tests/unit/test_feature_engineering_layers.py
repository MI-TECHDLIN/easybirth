"""Comprehensive tests for feature engineering pipeline and all layers."""
from __future__ import annotations

import pandas as pd
import pytest

from ml.feature_engineering import (
    calculators,
    encoders,
    transformers,
    validators,
)
from ml.feature_engineering.feature_pipeline import engineer_features


class TestCalculators:
    """Test calculator functions (pure math)."""

    def test_bmi_calculation_normal(self) -> None:
        """BMI calculation for normal values."""
        bmi = calculators.calculate_bmi(70, 170)
        assert 24.0 < bmi < 24.5

    def test_bmi_calculation_edge_cases(self) -> None:
        """BMI calculation with edge case values."""
        assert calculators.calculate_bmi(50, 150) > 20  # Underweight
        assert calculators.calculate_bmi(100, 170) > 30  # Overweight

    def test_bmi_invalid_height_raises_error(self) -> None:
        """Invalid height raises ValueError."""
        with pytest.raises(ValueError):
            calculators.calculate_bmi(70, 0)  # Zero height

    def test_bmi_invalid_weight_raises_error(self) -> None:
        """Invalid weight raises ValueError."""
        with pytest.raises(ValueError):
            calculators.calculate_bmi(0, 170)  # Zero weight

    def test_map_calculation_normal(self) -> None:
        """MAP calculation for normal blood pressure."""
        map_val = calculators.calculate_map(120, 80)
        assert 93 < map_val < 94

    def test_map_calculation_elevated(self) -> None:
        """MAP calculation for elevated blood pressure."""
        map_val = calculators.calculate_map(140, 90)
        assert 106 < map_val < 107

    def test_pulse_pressure_calculation(self) -> None:
        """Pulse pressure calculation."""
        pp = calculators.calculate_pulse_pressure(120, 80)
        assert pp == 40

    def test_trimester_first(self) -> None:
        """Gestational trimester for first trimester."""
        assert calculators.calculate_gestational_trimester(8) == 0
        assert calculators.calculate_gestational_trimester(13) == 0

    def test_trimester_second(self) -> None:
        """Gestational trimester for second trimester."""
        assert calculators.calculate_gestational_trimester(20) == 1
        assert calculators.calculate_gestational_trimester(26) == 1

    def test_trimester_third(self) -> None:
        """Gestational trimester for third trimester."""
        assert calculators.calculate_gestational_trimester(32) == 2
        assert calculators.calculate_gestational_trimester(40) == 2

    def test_age_group_teen(self) -> None:
        """Age group for teen pregnancy."""
        assert calculators.compute_age_group(16) == 0

    def test_age_group_optimal(self) -> None:
        """Age group for optimal age."""
        assert calculators.compute_age_group(28) == 1

    def test_age_group_advanced(self) -> None:
        """Age group for advanced maternal age."""
        assert calculators.compute_age_group(38) == 2

    def test_bmi_category_underweight(self) -> None:
        """BMI category for underweight."""
        assert calculators.compute_bmi_category(18.0) == 0

    def test_bmi_category_normal(self) -> None:
        """BMI category for normal weight."""
        assert calculators.compute_bmi_category(23.0) == 1

    def test_bmi_category_overweight(self) -> None:
        """BMI category for overweight."""
        assert calculators.compute_bmi_category(26.0) == 2

    def test_bmi_category_obese(self) -> None:
        """BMI category for obese."""
        assert calculators.compute_bmi_category(32.0) == 3

    def test_bp_category_normal(self) -> None:
        """BP category for normal blood pressure."""
        assert calculators.compute_bp_category(110, 70) == 0

    def test_bp_category_elevated(self) -> None:
        """BP category for elevated blood pressure."""
        assert calculators.compute_bp_category(120, 80) == 1

    def test_bp_category_stage1_hypertension(self) -> None:
        """BP category for stage 1 hypertension."""
        assert calculators.compute_bp_category(130, 85) == 2

    def test_bp_category_stage2_hypertension(self) -> None:
        """BP category for stage 2 hypertension."""
        assert calculators.compute_bp_category(150, 100) == 3

    def test_count_symptoms_zero(self) -> None:
        """Count symptoms with no symptoms."""
        count = calculators.count_symptoms()
        assert count == 0

    def test_count_symptoms_multiple(self) -> None:
        """Count symptoms with multiple symptoms."""
        count = calculators.count_symptoms(headache=1, fever=1, bleeding=1)
        assert count >= 3

    def test_high_risk_age_teen(self) -> None:
        """High risk age for teen."""
        assert calculators.is_high_risk_age(16) == 1

    def test_high_risk_age_advanced(self) -> None:
        """High risk age for advanced maternal age."""
        assert calculators.is_high_risk_age(42) == 1

    def test_high_risk_age_optimal(self) -> None:
        """High risk age for optimal age."""
        assert calculators.is_high_risk_age(28) == 0

    def test_emergency_flag_with_bleeding(self) -> None:
        """Emergency flag set with bleeding."""
        flag = calculators.has_emergency_flag(
            bleeding=1,
            difficulty_breathing=0
        )
        assert flag == 1

    def test_emergency_flag_no_symptoms(self) -> None:
        """Emergency flag not set without symptoms."""
        flag = calculators.has_emergency_flag(
            bleeding=0,
            difficulty_breathing=0
        )
        assert flag == 0


class TestTransformers:
    """Test transformer functions (category → label)."""

    def test_transform_bmi_category_underweight(self) -> None:
        """Transform BMI category 0."""
        assert transformers.transform_bmi_category(0) == "Underweight"

    def test_transform_bmi_category_obese(self) -> None:
        """Transform BMI category 3."""
        assert transformers.transform_bmi_category(3) == "Obese"

    def test_transform_bp_category_normal(self) -> None:
        """Transform BP category 0."""
        assert transformers.transform_bp_category(0) == "Normal"

    def test_transform_bp_category_stage2(self) -> None:
        """Transform BP category 3."""
        assert transformers.transform_bp_category(3) == "Stage 2 Hypertension"

    def test_transform_age_group_teen(self) -> None:
        """Transform age group 0."""
        assert "Teen" in transformers.transform_age_group_label(0)

    def test_transform_trimester_third(self) -> None:
        """Transform trimester 2."""
        assert "Third" in transformers.transform_trimester_label(2)


class TestValidators:
    """Test validator functions (input validation)."""

    def test_validate_valid_input_passes(self) -> None:
        """Valid input passes validation."""
        data = {
            "age": 28,
            "weeks_pregnant": 32,
            "height_cm": 165.0,
            "weight_kg": 70.0,
            "systolic_bp": 130,
            "diastolic_bp": 85,
        }
        result = validators.validate_input(data)
        assert result == data

    def test_validate_invalid_age_raises_error(self) -> None:
        """Invalid age raises ValidationError."""
        with pytest.raises(validators.ValidationError):
            validators.validate_input({"age": 12})  # Too young

    def test_validate_invalid_weeks_raises_error(self) -> None:
        """Invalid weeks raises ValidationError."""
        with pytest.raises(validators.ValidationError):
            validators.validate_input({"weeks_pregnant": 50})  # Too many weeks

    def test_validate_invalid_height_raises_error(self) -> None:
        """Invalid height raises ValidationError."""
        with pytest.raises(validators.ValidationError):
            validators.validate_input({"height_cm": 50})  # Too short

    def test_validate_invalid_weight_raises_error(self) -> None:
        """Invalid weight raises ValidationError."""
        with pytest.raises(validators.ValidationError):
            validators.validate_input({"weight_kg": 350})  # Too heavy

    def test_validate_invalid_bp_raises_error(self) -> None:
        """Invalid blood pressure raises ValidationError."""
        with pytest.raises(validators.ValidationError):
            validators.validate_input({"systolic_bp": 300})  # Too high

    def test_validate_multiple_errors_collected(self) -> None:
        """Multiple validation errors are reported."""
        with pytest.raises(validators.ValidationError) as exc_info:
            validators.validate_input({
                "age": 12,  # Invalid
                "weeks_pregnant": 50,  # Invalid
            })
        error_message = str(exc_info.value)
        assert "age" in error_message.lower()

    def test_validate_converts_blood_sugar_mmol_to_mgdl(self) -> None:
        """Blood sugar values in mmol/L are normalized to mg/dL."""
        data = {
            "age": 28,
            "weeks_pregnant": 32,
            "height_cm": 165.0,
            "weight_kg": 70.0,
            "systolic_bp": 130,
            "diastolic_bp": 85,
            "heart_rate": 80,
            "body_temperature": 103.26,
            "blood_sugar": 12.76,
            "oxygen_saturation": 98.0,
            "hemoglobin": 12.0,
            "distance_to_hospital": 10,
            "travel_time_minutes": 20,
        }
        result = validators.validate_input(data)
        assert result["blood_sugar"] == 229.68
        assert result["body_temperature"] == 39.59

    def test_validate_clamps_spo2_noise_above_100(self) -> None:
        """Slightly noisy SpO2 readings above 100% are clamped."""
        data = {
            "age": 28,
            "weeks_pregnant": 32,
            "height_cm": 165.0,
            "weight_kg": 70.0,
            "systolic_bp": 130,
            "diastolic_bp": 85,
            "heart_rate": 80,
            "body_temperature": 36.8,
            "blood_sugar": 95.0,
            "oxygen_saturation": 102.75,
            "hemoglobin": 12.0,
            "distance_to_hospital": 10,
            "travel_time_minutes": 20,
        }
        result = validators.validate_input(data)
        assert result["oxygen_saturation"] == 100.0

    def test_validate_accepts_high_synthetic_blood_sugar(self) -> None:
        """Synthetic mg/dL blood sugar values above 500 are accepted."""
        data = {
            "age": 30,
            "weeks_pregnant": 29,
            "height_cm": 160.0,
            "weight_kg": 65.0,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "heart_rate": 78,
            "body_temperature": 37.0,
            "blood_sugar": 606.96,
            "oxygen_saturation": 97.0,
            "hemoglobin": 12.5,
            "distance_to_hospital": 15,
            "travel_time_minutes": 20,
        }
        result = validators.validate_input(data)
        assert result["blood_sugar"] == 606.96

    def test_validate_normalizes_synthetic_row_with_fahrenheit_and_mmol(self) -> None:
        """Synthetic rows using Fahrenheit and mmol/L are normalized."""
        row = {
            "age": 29,
            "weeks_pregnant": 37,
            "height_cm": 163.1,
            "weight_kg": 58.2,
            "systolic_bp": 118,
            "diastolic_bp": 67,
            "heart_rate": 68,
            "body_temperature": 102.1,
            "blood_sugar": 9.86,
            "oxygen_saturation": 98.5,
            "hemoglobin": 12.34,
            "distance_to_hospital": 9,
            "travel_time_minutes": 2,
        }
        result = validators.validate_input(row)
        assert result["body_temperature"] == 38.94
        assert result["blood_sugar"] == 177.48
        assert result["oxygen_saturation"] == 98.5


class TestEncoders:
    """Test encoder functions (category → numeric code)."""

    def test_encode_bmi_category_int(self) -> None:
        """Encode BMI category from int."""
        assert encoders.encode_bmi_category(2) == 2

    def test_encode_bmi_category_string(self) -> None:
        """Encode BMI category from string."""
        assert encoders.encode_bmi_category("Obese") == 3

    def test_encode_trimester_int(self) -> None:
        """Encode trimester from int."""
        assert encoders.encode_trimester(1) == 1

    def test_encode_trimester_string(self) -> None:
        """Encode trimester from string."""
        assert encoders.encode_trimester("Third Trimester") == 2

    def test_encode_urban_rural_int(self) -> None:
        """Encode urban/rural from int."""
        assert encoders.encode_urban_rural(1) == 1

    def test_encode_urban_rural_string_urban(self) -> None:
        """Encode 'Urban' to 1."""
        assert encoders.encode_urban_rural("Urban") == 1

    def test_encode_urban_rural_string_rural(self) -> None:
        """Encode 'Rural' to 0."""
        assert encoders.encode_urban_rural("Rural") == 0


class TestFeatureEngineeringPipeline:
    """Test end-to-end feature engineering pipeline."""

    @pytest.fixture
    def sample_input(self) -> dict:
        """Create sample patient data."""
        return {
            "age": 28,
            "weeks_pregnant": 32,
            "height_cm": 165.0,
            "weight_kg": 70.0,
            "systolic_bp": 130,
            "diastolic_bp": 85,
            "heart_rate": 82,
            "body_temperature": 36.8,
            "blood_sugar": 95.0,
            "oxygen_saturation": 97.5,
            "hemoglobin": 12.1,
            "previous_pregnancies": 1,
            "previous_c_section": 0,
            "previous_miscarriages": 0,
            "multiple_pregnancy": 0,
            "history_hypertension": 0,
            "history_diabetes": 0,
            "history_pre_eclampsia": 0,
            "headache": 0,
            "blurred_vision": 0,
            "swollen_feet": 0,
            "bleeding": 0,
            "abdominal_pain": 0,
            "fever": 0,
            "reduced_fetal_movement": 0,
            "severe_vomiting": 0,
            "difficulty_breathing": 0,
            "smoker": 0,
            "alcohol": 0,
            "nutrition_score": 7,
            "water_intake": 3,
            "distance_to_hospital": 20,
            "travel_time_minutes": 25,
            "urban_rural": 1,
        }

    def test_pipeline_returns_dataframe(self, sample_input: dict) -> None:
        """Pipeline returns pandas DataFrame."""
        result = engineer_features(sample_input)
        assert isinstance(result, pd.DataFrame)

    def test_pipeline_returns_single_row(self, sample_input: dict) -> None:
        """Pipeline returns single-row DataFrame."""
        result = engineer_features(sample_input)
        assert result.shape[0] == 1

    def test_pipeline_produces_multiple_features(self, sample_input: dict) -> None:
        """Pipeline produces 45+ features."""
        result = engineer_features(sample_input)
        assert result.shape[1] >= 45

    def test_pipeline_includes_key_features(self, sample_input: dict) -> None:
        """Pipeline includes key computed features."""
        result = engineer_features(sample_input)
        key_features = [
            "bmi",
            "map",
            "pulse_pressure",
            "trimester",
            "age_group",
            "emergency_flag",
            "symptom_count",
        ]
        for feat in key_features:
            assert feat in result.columns

    def test_pipeline_rejects_invalid_input(self) -> None:
        """Pipeline rejects invalid input."""
        invalid_input = {"age": 12}  # Too young
        with pytest.raises(validators.ValidationError):
            engineer_features(invalid_input)

    def test_pipeline_feature_values_reasonable(self, sample_input: dict) -> None:
        """Generated features have reasonable values."""
        result = engineer_features(sample_input)

        # BMI should be ~25
        assert 24 < result["bmi"].iloc[0] < 26

        # MAP should be ~100 for BP 130/85
        assert 99 < result["map"].iloc[0] < 101

        # Pulse pressure should be 45
        assert result["pulse_pressure"].iloc[0] == 45

        # Trimester should be 2 (third)
        assert result["trimester"].iloc[0] == 2

    def test_pipeline_deterministic(self, sample_input: dict) -> None:
        """Same input always produces same output."""
        result1 = engineer_features(sample_input)
        result2 = engineer_features(sample_input)

        pd.testing.assert_frame_equal(result1, result2)

    def test_pipeline_with_high_risk_profile(self) -> None:
        """Pipeline handles high-risk profile."""
        high_risk_input = {
            "age": 42,  # Advanced maternal age
            "weeks_pregnant": 30,
            "height_cm": 160.0,
            "weight_kg": 85.0,  # Overweight
            "systolic_bp": 150,  # Stage 2 hypertension
            "diastolic_bp": 100,
            "heart_rate": 95,
            "body_temperature": 37.2,
            "blood_sugar": 140.0,  # Elevated
            "oxygen_saturation": 96.0,  # Slightly low
            "hemoglobin": 11.5,  # Low
            "previous_pregnancies": 2,
            "previous_c_section": 1,
            "previous_miscarriages": 1,
            "multiple_pregnancy": 0,
            "history_hypertension": 1,
            "history_diabetes": 1,
            "history_pre_eclampsia": 1,
            "headache": 1,
            "blurred_vision": 1,
            "swollen_feet": 1,
            "bleeding": 1,
            "abdominal_pain": 1,
            "fever": 0,
            "reduced_fetal_movement": 0,
            "severe_vomiting": 1,
            "difficulty_breathing": 1,
            "smoker": 1,
            "alcohol": 1,
            "nutrition_score": 3,
            "water_intake": 1,
            "distance_to_hospital": 80,
            "travel_time_minutes": 60,
            "urban_rural": 0,
        }

        result = engineer_features(high_risk_input)

        # Should have high-risk indicators
        assert result["high_risk_age"].iloc[0] == 1
        assert result["hypertension_risk"].iloc[0] == 1
        assert result["diabetes_risk"].iloc[0] == 1
        assert result["emergency_flag"].iloc[0] == 1

    def test_pipeline_consistency_across_inputs(self) -> None:
        """Different inputs produce different (but reasonable) outputs."""
        input1 = {
            "age": 25,
            "weeks_pregnant": 20,
            "height_cm": 160.0,
            "weight_kg": 60.0,
            "systolic_bp": 110,
            "diastolic_bp": 70,
            "heart_rate": 75,
            "body_temperature": 36.5,
            "blood_sugar": 85.0,
            "oxygen_saturation": 98.0,
            "hemoglobin": 13.0,
            "previous_pregnancies": 0,
            "previous_c_section": 0,
            "previous_miscarriages": 0,
            "multiple_pregnancy": 0,
            "history_hypertension": 0,
            "history_diabetes": 0,
            "history_pre_eclampsia": 0,
            "headache": 0,
            "blurred_vision": 0,
            "swollen_feet": 0,
            "bleeding": 0,
            "abdominal_pain": 0,
            "fever": 0,
            "reduced_fetal_movement": 0,
            "severe_vomiting": 0,
            "difficulty_breathing": 0,
            "smoker": 0,
            "alcohol": 0,
            "nutrition_score": 8,
            "water_intake": 4,
            "distance_to_hospital": 10,
            "travel_time_minutes": 15,
            "urban_rural": 1,
        }

        input2 = {
            "age": 40,
            "weeks_pregnant": 36,
            "height_cm": 170.0,
            "weight_kg": 90.0,
            "systolic_bp": 140,
            "diastolic_bp": 90,
            "heart_rate": 90,
            "body_temperature": 37.0,
            "blood_sugar": 110.0,
            "oxygen_saturation": 97.0,
            "hemoglobin": 11.5,
            "previous_pregnancies": 3,
            "previous_c_section": 1,
            "previous_miscarriages": 1,
            "multiple_pregnancy": 1,
            "history_hypertension": 1,
            "history_diabetes": 1,
            "history_pre_eclampsia": 0,
            "headache": 1,
            "blurred_vision": 0,
            "swollen_feet": 1,
            "bleeding": 0,
            "abdominal_pain": 0,
            "fever": 1,
            "reduced_fetal_movement": 0,
            "severe_vomiting": 0,
            "difficulty_breathing": 0,
            "smoker": 1,
            "alcohol": 0,
            "nutrition_score": 4,
            "water_intake": 2,
            "distance_to_hospital": 50,
            "travel_time_minutes": 40,
            "urban_rural": 0,
        }

        result1 = engineer_features(input1)
        result2 = engineer_features(input2)

        # Different inputs should produce different features
        assert result1["bmi"].iloc[0] != result2["bmi"].iloc[0]
        assert result1["age_group"].iloc[0] != result2["age_group"].iloc[0]
        assert result1["emergency_flag"].iloc[0] != result2["emergency_flag"].iloc[0]
