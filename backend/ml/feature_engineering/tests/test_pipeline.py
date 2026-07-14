"""Integration tests for the feature engineering pipeline."""

import pytest
import pandas as pd
from ..feature_pipeline import engineer_features
from ..validators import ValidationError


class TestFeatureEngineeringPipeline:
    """Test the complete feature engineering pipeline."""

    def get_valid_input(self):
        """Get a valid sample input."""
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

    def test_pipeline_produces_dataframe(self):
        """Test that pipeline produces DataFrame."""
        data = self.get_valid_input()
        result = engineer_features(data)

        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == 1  # Single row
        assert result.shape[1] > 20  # Many features

    def test_pipeline_includes_key_features(self):
        """Test that pipeline includes key engineered features."""
        data = self.get_valid_input()
        result = engineer_features(data)

        expected_features = [
            "bmi",
            "map",
            "pulse_pressure",
            "trimester",
            "age_group",
            "bmi_category",
            "bp_category",
            "symptom_count",
            "high_risk_age",
            "hypertension_risk",
            "diabetes_risk",
            "emergency_flag",
        ]

        for feature in expected_features:
            assert feature in result.columns, f"Missing feature: {feature}"

    def test_pipeline_preserves_original_vitals(self):
        """Test that pipeline preserves original vital measurements."""
        data = self.get_valid_input()
        result = engineer_features(data)

        assert result["age"].iloc[0] == 28
        assert result["systolic_bp"].iloc[0] == 130
        assert result["diastolic_bp"].iloc[0] == 85
        assert result["heart_rate"].iloc[0] == 82

    def test_pipeline_calculates_bmi_correctly(self):
        """Test BMI calculation through pipeline."""
        data = self.get_valid_input()
        result = engineer_features(data)

        # BMI = 70 / (1.65^2) = 25.71
        expected_bmi = round(70.0 / (1.65 ** 2), 2)
        assert result["bmi"].iloc[0] == expected_bmi

    def test_pipeline_computes_trimester_correctly(self):
        """Test trimester computation through pipeline."""
        data = self.get_valid_input()
        data["weeks_pregnant"] = 32  # Third trimester
        result = engineer_features(data)

        assert result["trimester"].iloc[0] == 2  # Third trimester

    def test_pipeline_computes_map_correctly(self):
        """Test MAP computation through pipeline."""
        data = self.get_valid_input()
        data["systolic_bp"] = 120
        data["diastolic_bp"] = 80
        result = engineer_features(data)

        # MAP = (120 + 2*80) / 3 = 93.33
        expected_map = round((120 + 2 * 80) / 3, 2)
        assert result["map"].iloc[0] == expected_map

    def test_pipeline_encodes_categories(self):
        """Test that categories are properly encoded."""
        data = self.get_valid_input()
        result = engineer_features(data)

        # Check encoded features exist
        assert "trimester_encoded" in result.columns
        assert "age_group_encoded" in result.columns
        assert "bmi_category_encoded" in result.columns
        assert "bp_category_encoded" in result.columns

        # Check encoded values are numeric
        assert isinstance(result["trimester_encoded"].iloc[0], (int, float))
        assert 0 <= result["trimester_encoded"].iloc[0] <= 2

    def test_pipeline_with_minimal_input(self):
        """Test pipeline with only required fields."""
        minimal_data = {
            "age": 28,
            "weeks_pregnant": 28,
            "height_cm": 165.0,
            "weight_kg": 70.0,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "heart_rate": 75,
            "body_temperature": 36.8,
            "blood_sugar": 90.0,
            "oxygen_saturation": 98.0,
            "hemoglobin": 12.0,
            "distance_to_hospital": 10,
            "travel_time_minutes": 15,
        }

        result = engineer_features(minimal_data)
        assert result.shape[0] == 1

    def test_pipeline_with_high_risk_profile(self):
        """Test pipeline with high-risk patient profile."""
        data = self.get_valid_input()
        data["age"] = 42  # High-risk age
        data["systolic_bp"] = 150  # Stage 2 hypertension
        data["diastolic_bp"] = 95
        data["history_hypertension"] = 1
        data["bleeding"] = 1
        data["difficulty_breathing"] = 1

        result = engineer_features(data)

        assert result["high_risk_age"].iloc[0] == 1
        assert result["hypertension_risk"].iloc[0] == 1
        assert result["emergency_flag"].iloc[0] == 1

    def test_pipeline_with_many_symptoms(self):
        """Test pipeline with multiple symptoms."""
        data = self.get_valid_input()
        data["headache"] = 1
        data["blurred_vision"] = 1
        data["swollen_feet"] = 1
        data["bleeding"] = 1
        data["abdominal_pain"] = 1

        result = engineer_features(data)

        assert result["symptom_count"].iloc[0] == 5

    def test_pipeline_rejects_invalid_age(self):
        """Test pipeline rejects invalid age."""
        data = self.get_valid_input()
        data["age"] = 12  # Too young

        with pytest.raises(ValidationError):
            engineer_features(data)

    def test_pipeline_rejects_invalid_pregnancy_weeks(self):
        """Test pipeline rejects invalid pregnancy weeks."""
        data = self.get_valid_input()
        data["weeks_pregnant"] = 50  # Too many

        with pytest.raises(ValidationError):
            engineer_features(data)

    def test_pipeline_rejects_invalid_bp(self):
        """Test pipeline rejects invalid blood pressure."""
        data = self.get_valid_input()
        data["systolic_bp"] = 250  # Too high

        with pytest.raises(ValidationError):
            engineer_features(data)

    def test_pipeline_rejects_invalid_temperature(self):
        """Test pipeline rejects invalid temperature."""
        data = self.get_valid_input()
        data["body_temperature"] = 45  # Too high

        with pytest.raises(ValidationError):
            engineer_features(data)

    def test_pipeline_rejects_impossible_weight(self):
        """Test pipeline rejects impossible weight."""
        data = self.get_valid_input()
        data["weight_kg"] = 250  # Too high

        with pytest.raises(ValidationError):
            engineer_features(data)

    def test_pipeline_computes_accessibility(self):
        """Test accessibility computation through pipeline."""
        data = self.get_valid_input()
        data["distance_to_hospital"] = 80
        data["travel_time_minutes"] = 90

        result = engineer_features(data)

        # This should be "Poor Access"
        assert result["accessibility_index"].iloc[0] == 2
        assert result["accessibility_encoded"].iloc[0] == 2

    def test_pipeline_with_different_trimesters(self):
        """Test pipeline produces different features for different trimesters."""
        # First trimester
        data_t1 = self.get_valid_input()
        data_t1["weeks_pregnant"] = 10
        result_t1 = engineer_features(data_t1)

        # Third trimester
        data_t3 = self.get_valid_input()
        data_t3["weeks_pregnant"] = 35
        result_t3 = engineer_features(data_t3)

        # Trimesters should be different
        assert result_t1["trimester"].iloc[0] == 0
        assert result_t3["trimester"].iloc[0] == 2

    def test_pipeline_feature_consistency(self):
        """Test that same input produces same output."""
        data = self.get_valid_input()

        result1 = engineer_features(data.copy())
        result2 = engineer_features(data.copy())

        pd.testing.assert_frame_equal(result1, result2)

    def test_pipeline_with_teen_pregnancy(self):
        """Test pipeline with teen pregnancy."""
        data = self.get_valid_input()
        data["age"] = 16

        result = engineer_features(data)

        assert result["age_group"].iloc[0] == 0  # Teen
        assert result["high_risk_age"].iloc[0] == 1

    def test_pipeline_with_advanced_maternal_age(self):
        """Test pipeline with advanced maternal age."""
        data = self.get_valid_input()
        data["age"] = 38

        result = engineer_features(data)

        assert result["age_group"].iloc[0] == 2  # Advanced
        assert result["age_group_encoded"].iloc[0] == 2

    def test_pipeline_symptom_severity_levels(self):
        """Test symptom severity scoring across pipeline."""
        # No symptoms
        data_none = self.get_valid_input()
        result_none = engineer_features(data_none)
        assert result_none["symptom_severity"].iloc[0] == 0

        # Mild symptoms
        data_mild = self.get_valid_input()
        data_mild["headache"] = 1
        result_mild = engineer_features(data_mild)
        assert result_mild["symptom_severity"].iloc[0] == 1

        # Moderate symptoms
        data_moderate = self.get_valid_input()
        data_moderate["headache"] = 1
        data_moderate["fever"] = 1
        data_moderate["abdominal_pain"] = 1
        result_moderate = engineer_features(data_moderate)
        assert result_moderate["symptom_severity"].iloc[0] == 2

        # Severe symptoms
        data_severe = self.get_valid_input()
        for field in [
            "headache",
            "blurred_vision",
            "swollen_feet",
            "bleeding",
            "fever",
        ]:
            data_severe[field] = 1
        result_severe = engineer_features(data_severe)
        assert result_severe["symptom_severity"].iloc[0] == 3
