"""Feature engineering pipeline orchestration.

This module provides the single entry point for all feature engineering.
It coordinates validation, calculation, transformation, and encoding.
"""

from typing import Dict, Any, List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from . import calculators
from . import transformers
from . import validators
from . import encoders


class FeatureEngineeringPipeline(BaseEstimator, TransformerMixin):
    """Orchestrates the complete feature engineering process.
    
    This class implements the sklearn transformer interface, allowing it to be
    used in sklearn pipelines for consistent preprocessing across training,
    validation, and test sets.
    
    Example:
        >>> from sklearn.pipeline import Pipeline
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> from ml.feature_engineering.feature_pipeline import FeatureEngineeringPipeline
        >>>
        >>> pipeline = Pipeline([
        ...     ("features", FeatureEngineeringPipeline()),
        ...     ("model", RandomForestClassifier())
        ... ])
        >>> pipeline.fit(X_train, y_train)
        >>> predictions = pipeline.predict(X_test)
    """

    def __init__(self):
        """Initialize the feature engineering pipeline."""
        self.validation_errors: List[str] = []
        self.feature_vector: Dict[str, Any] = {}
    
    def fit(self, X, y=None):
        """
        Fit the transformer (no-op, as feature engineering has no learnable parameters).
        
        Feature engineering is deterministic and does not require fitting on training data.
        This method exists only for sklearn compatibility.
        
        Args:
            X: Feature data (ignored)
            y: Target variable (ignored)
            
        Returns:
            self
        """
        return self
    
    def transform(self, X) -> pd.DataFrame:
        """
        Apply feature engineering to raw data.
        
        Works with both DataFrame input (from sklearn pipelines) and dict input
        (for direct API calls). When used in sklearn pipelines, input will be
        a DataFrame where each row is a patient record.
        
        Args:
            X: Input data as either:
               - pandas.DataFrame where each row is a raw patient dict
               - list of dicts
               - single dict (for backward compatibility)
        
        Returns:
            DataFrame with engineered features (one row per input sample)
        """
        if isinstance(X, dict):
            # Single record (backward compatibility)
            return self.engineer_features(X)
        elif isinstance(X, pd.DataFrame):
            # DataFrame - apply feature engineering to each row
            results = []
            for _, row in X.iterrows():
                row_dict = row.to_dict()
                engineered = self.engineer_features(row_dict)
                results.append(engineered)
            return pd.concat(results, ignore_index=True)
        elif isinstance(X, list):
            # List of dicts
            results = []
            for record in X:
                engineered = self.engineer_features(record)
                results.append(engineered)
            return pd.concat(results, ignore_index=True)
        else:
            raise TypeError(f"Expected DataFrame, list, or dict, got {type(X)}")

    def engineer_features(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Transform raw patient data into ML-ready feature vector.

        Pipeline stages:
        1. Validation - reject impossible values
        2. Cleaning - handle missing data (if present)
        3. Calculations - compute derived numerical features
        4. Transformations - convert to clinical categories
        5. Encoding - convert categories to numeric codes

        Args:
            raw_data: Dictionary of raw patient health data

        Returns:
            Single-row DataFrame with engineered features

        Raises:
            validators.ValidationError: If input validation fails
        """
        # Stage 1: Validation
        validated_data = validators.validate_input(raw_data)

        # Stage 2: Initialize feature vector
        features = {}

        # ============================================================
        # Stage 3: Calculations (Derive numerical features)
        # ============================================================

        # Demographics features
        features["age"] = validated_data["age"]
        features["weeks_pregnant"] = validated_data["weeks_pregnant"]

        # BMI Calculation
        features["bmi"] = calculators.calculate_bmi(
            validated_data["weight_kg"], validated_data["height_cm"]
        )

        # Blood Pressure derived features
        features["map"] = calculators.calculate_map(
            validated_data["systolic_bp"], validated_data["diastolic_bp"]
        )
        features["pulse_pressure"] = calculators.calculate_pulse_pressure(
            validated_data["systolic_bp"], validated_data["diastolic_bp"]
        )

        # Clinical groupings
        features["trimester"] = calculators.calculate_gestational_trimester(
            validated_data["weeks_pregnant"]
        )
        features["age_group"] = calculators.compute_age_group(
            validated_data["age"]
        )
        features["bmi_category"] = calculators.compute_bmi_category(
            features["bmi"]
        )
        features["bp_category"] = calculators.compute_bp_category(
            validated_data["systolic_bp"], validated_data["diastolic_bp"]
        )

        # Symptom and risk aggregations
        features["symptom_count"] = calculators.count_symptoms(
            headache=validated_data.get("headache", 0),
            blurred_vision=validated_data.get("blurred_vision", 0),
            swollen_feet=validated_data.get("swollen_feet", 0),
            bleeding=validated_data.get("bleeding", 0),
            abdominal_pain=validated_data.get("abdominal_pain", 0),
            fever=validated_data.get("fever", 0),
            reduced_fetal_movement=validated_data.get(
                "reduced_fetal_movement", 0
            ),
            severe_vomiting=validated_data.get("severe_vomiting", 0),
            difficulty_breathing=validated_data.get("difficulty_breathing", 0),
        )

        features["symptom_severity"] = (
            calculators.compute_symptom_severity_score(features["symptom_count"])
        )

        # Risk aggregations
        features["high_risk_age"] = calculators.is_high_risk_age(
            validated_data["age"]
        )
        features["hypertension_risk"] = calculators.compute_hypertension_risk(
            validated_data.get("history_hypertension", 0),
            validated_data["systolic_bp"],
            validated_data["diastolic_bp"],
        )
        features["diabetes_risk"] = calculators.compute_diabetes_risk(
            validated_data.get("history_diabetes", 0),
            validated_data["blood_sugar"],
        )

        # Accessibility
        features["accessibility_index"] = (
            calculators.compute_accessibility_index(
                validated_data["distance_to_hospital"],
                validated_data["travel_time_minutes"],
            )
        )

        # Emergency flags: combine explicit emergency symptoms with
        # systemic hypertension risk (Stage 2 or history-driven risk).
        explicit_emergency = calculators.has_emergency_flag(
            bleeding=validated_data.get("bleeding", 0),
            difficulty_breathing=validated_data.get("difficulty_breathing", 0),
            severe_vomiting=validated_data.get("severe_vomiting", 0),
            reduced_fetal_movement=validated_data.get(
                "reduced_fetal_movement", 0
            ),
        )
        features["emergency_flag"] = 1 if (explicit_emergency or features.get("hypertension_risk", 0)) else 0

        # ============================================================
        # Stage 4: Keep original vitals (for model input)
        # ============================================================
        features["systolic_bp"] = validated_data["systolic_bp"]
        features["diastolic_bp"] = validated_data["diastolic_bp"]
        features["heart_rate"] = validated_data["heart_rate"]
        features["body_temperature"] = validated_data["body_temperature"]
        features["blood_sugar"] = validated_data["blood_sugar"]
        features["oxygen_saturation"] = validated_data["oxygen_saturation"]
        features["hemoglobin"] = validated_data["hemoglobin"]

        # Keep relevant medical history
        for field in [
            "previous_pregnancies",
            "previous_c_section",
            "previous_miscarriages",
            "multiple_pregnancy",
            "history_hypertension",
            "history_diabetes",
            "history_pre_eclampsia",
        ]:
            if field in validated_data:
                features[field] = validated_data[field]

        # Keep symptoms
        for field in [
            "headache",
            "blurred_vision",
            "swollen_feet",
            "bleeding",
            "abdominal_pain",
            "fever",
            "reduced_fetal_movement",
            "severe_vomiting",
            "difficulty_breathing",
        ]:
            if field in validated_data:
                features[field] = validated_data[field]

        # Lifestyle
        for field in ["smoker", "alcohol", "nutrition_score", "water_intake"]:
            if field in validated_data:
                features[field] = validated_data[field]

        # Environment
        features["urban_rural"] = validated_data.get("urban_rural", 1)

        # ============================================================
        # Stage 5: Encode categorical features for ML
        # ============================================================
        features["trimester_encoded"] = encoders.encode_trimester(
            features["trimester"]
        )
        features["age_group_encoded"] = encoders.encode_age_group(
            features["age_group"]
        )
        features["bmi_category_encoded"] = encoders.encode_bmi_category(
            features["bmi_category"]
        )
        features["bp_category_encoded"] = encoders.encode_bp_category(
            features["bp_category"]
        )
        features["accessibility_encoded"] = encoders.encode_accessibility(
            features["accessibility_index"]
        )
        features["severity_encoded"] = encoders.encode_severity(
            features["symptom_severity"]
        )
        features["urban_rural_encoded"] = encoders.encode_urban_rural(
            features["urban_rural"]
        )

        # ============================================================
        # Convert to DataFrame (single row)
        # ============================================================
        self.feature_vector = features
        return pd.DataFrame([features])

    def get_feature_names(self) -> List[str]:
        """Get list of all feature column names."""
        if not self.feature_vector:
            return []
        return list(self.feature_vector.keys())

    def get_feature_statistics(self) -> Dict[str, Any]:
        """Get statistics about generated features."""
        if not self.feature_vector:
            return {}

        return {
            "total_features": len(self.feature_vector),
            "feature_names": self.get_feature_names(),
            "has_emergency_flag": self.feature_vector.get("emergency_flag", 0),
            "high_risk_age": self.feature_vector.get("high_risk_age", 0),
            "hypertension_risk": self.feature_vector.get("hypertension_risk", 0),
            "diabetes_risk": self.feature_vector.get("diabetes_risk", 0),
            "symptom_count": self.feature_vector.get("symptom_count", 0),
        }


# Module-level instance
_pipeline = FeatureEngineeringPipeline()


def engineer_features(raw_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Convenience function to engineer features from raw patient data.

    This is the main entry point for the feature engineering pipeline.

    Args:
        raw_data: Dictionary of raw patient health data

    Returns:
        Single-row DataFrame with engineered features

    Example:
        >>> raw_input = {
        ...     "age": 28,
        ...     "weeks_pregnant": 32,
        ...     "height_cm": 165.0,
        ...     "weight_kg": 70.0,
        ...     "systolic_bp": 130,
        ...     "diastolic_bp": 85,
        ...     "heart_rate": 82,
        ...     "body_temperature": 36.8,
        ...     "blood_sugar": 95.0,
        ...     "oxygen_saturation": 97.5,
        ...     "hemoglobin": 12.1,
        ...     "distance_to_hospital": 15,
        ...     "travel_time_minutes": 20,
        ... }
        >>> df = engineer_features(raw_input)
        >>> df.shape
        (1, 40+)
    """
    return _pipeline.engineer_features(raw_data)
